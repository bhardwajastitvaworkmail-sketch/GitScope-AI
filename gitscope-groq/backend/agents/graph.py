"""
GitScope AI - LangGraph Multi-Agent Pipeline (Groq Edition)
Graph: fetch_repo → analyze_code → [flowchart, tech_stack, issue_detector, summarizer] → merge
Uses Groq API for ultra-fast free inference.
"""

import json
import asyncio
import os
from typing import TypedDict
from dotenv import load_dotenv

# Load .env FIRST before anything else
load_dotenv()

from langgraph.graph import StateGraph, END
from agents.prompts import ANALYZER_PROMPT, FLOWCHART_PROMPT, ISSUE_DETECTOR_PROMPT, SUMMARIZER_PROMPT
from utils.github import fetch_repo_data
from utils.groq_client import groq_chat, parse_json_response


# ─── State Schema ─────────────────────────────────────────────────────────────

class RepoState(TypedDict):
    repo_url: str
    repo_data: dict
    analysis: dict
    flowchart: str
    tech_stack: list
    issues: list
    summary: dict
    score: str
    error: str


# ─── Node 1: Fetch Repo ───────────────────────────────────────────────────────

async def fetch_repo_node(state: RepoState) -> RepoState:
    """Fetch repository data from GitHub API."""
    try:
        repo_data = await fetch_repo_data(state["repo_url"])
        return {**state, "repo_data": repo_data}
    except Exception as e:
        return {**state, "error": f"Failed to fetch repo: {str(e)}"}


# ─── Node 2: Analyze Code ─────────────────────────────────────────────────────

async def analyze_code_node(state: RepoState) -> RepoState:
    """Primary analysis: detect project type, architecture, tech stack."""
    if state.get("error"):
        return state

    repo = state["repo_data"]
    context = f"""
Repository: {repo['metadata']['full_name']}
Description: {repo['metadata']['description']}
Primary Language: {repo['metadata']['language']}
Topics: {', '.join(repo['metadata']['topics'])}
Stars: {repo['metadata']['stars']} | Forks: {repo['metadata']['forks']}
License: {repo['metadata']['license']}

File Tree (first 100 files):
{chr(10).join(repo['file_tree'][:100])}

Key Files Content:
{json.dumps({k: v[:500] for k, v in repo['key_files'].items()}, indent=2)}
"""
    try:
        # Run in thread pool since Groq client is sync
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: groq_chat(ANALYZER_PROMPT, context, temperature=0.3)
        )
        analysis = parse_json_response(response)
        return {**state, "analysis": analysis}
    except Exception as e:
        return {**state, "error": f"Analysis failed: {str(e)}"}


# ─── Node 3a: Flowchart ───────────────────────────────────────────────────────

async def flowchart_node(state: RepoState) -> RepoState:
    """Generate Mermaid.js architecture flowchart."""
    if state.get("error"):
        return state

    repo = state["repo_data"]
    analysis = state.get("analysis", {})
    context = f"""
Repository: {repo['metadata']['full_name']}
Architecture: {analysis.get('architecture', 'unknown')}
Project Type: {analysis.get('project_type', 'unknown')}
Main Components: {json.dumps(analysis.get('main_components', []))}
File Tree:
{chr(10).join(repo['file_tree'][:80])}
"""
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: groq_chat(FLOWCHART_PROMPT, context, temperature=0.2)
        )
        # Extract mermaid block
        if "```mermaid" in response:
            start = response.index("```mermaid") + len("```mermaid")
            end = response.index("```", start)
            flowchart = response[start:end].strip()
        elif "graph " in response:
            flowchart = response.strip()
        else:
            flowchart = "graph TD\n    A[Repository] --> B[Could not generate diagram]"
        return {**state, "flowchart": flowchart}
    except Exception as e:
        return {**state, "flowchart": "graph TD\n    A[Error generating flowchart]"}


# ─── Node 3b: Tech Stack ──────────────────────────────────────────────────────

async def tech_stack_node(state: RepoState) -> RepoState:
    """Extract detailed tech stack from analysis."""
    if state.get("error"):
        return state

    analysis = state.get("analysis", {})
    tech_stack = analysis.get("tech_stack", [])

    # File-based detection as fallback/supplement
    file_tree = state["repo_data"]["file_tree"]
    key_files = state["repo_data"]["key_files"]

    detected_extra = []
    infra_files = {
        "docker-compose.yml": {"name": "Docker Compose", "category": "infrastructure", "icon": "🐳"},
        "dockerfile": {"name": "Docker", "category": "infrastructure", "icon": "🐳"},
        ".github/workflows": {"name": "GitHub Actions", "category": "ci_cd", "icon": "⚙️"},
        "kubernetes": {"name": "Kubernetes", "category": "infrastructure", "icon": "☸️"},
        "terraform": {"name": "Terraform", "category": "infrastructure", "icon": "🏗️"},
        ".eslintrc": {"name": "ESLint", "category": "tooling", "icon": "🔍"},
        "jest.config": {"name": "Jest", "category": "testing", "icon": "🧪"},
        "pytest": {"name": "Pytest", "category": "testing", "icon": "🧪"},
    }

    existing_names = {t["name"].lower() for t in tech_stack}
    for f in file_tree:
        for key, tech in infra_files.items():
            if key in f.lower() and tech["name"].lower() not in existing_names:
                detected_extra.append(tech)
                existing_names.add(tech["name"].lower())

    return {**state, "tech_stack": tech_stack + detected_extra}


# ─── Node 3c: Issue Detector ─────────────────────────────────────────────────

async def issue_detector_node(state: RepoState) -> RepoState:
    """Detect structural issues, missing files, bad practices."""
    if state.get("error"):
        return state

    repo = state["repo_data"]
    file_tree = repo["file_tree"]
    key_files = repo["key_files"]

    context = f"""
Repository: {repo['metadata']['full_name']}
File Tree: {json.dumps(file_tree[:100])}
Has README: {any('readme' in f.lower() for f in file_tree)}
Has Tests: {any('test' in f.lower() or 'spec' in f.lower() for f in file_tree)}
Has CI/CD: {any('.github/workflows' in f or '.gitlab-ci' in f for f in file_tree)}
Has LICENSE: {any('license' in f.lower() for f in file_tree)}
Has CONTRIBUTING: {any('contributing' in f.lower() for f in file_tree)}
Has Docker: {any('dockerfile' in f.lower() for f in file_tree)}
Open Issues Count: {repo['metadata']['open_issues']}
README Content (if present): {key_files.get('README.md', 'NOT FOUND')[:800]}
"""
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: groq_chat(ISSUE_DETECTOR_PROMPT, context, temperature=0.1)
        )
        result = parse_json_response(response)
        if isinstance(result, dict):
            return {**state, "issues": result.get("issues", []), "score": result.get("score", "7/10")}
        return {**state, "issues": [], "score": "7/10"}
    except Exception as e:
        return {**state, "issues": [], "score": "N/A"}


# ─── Node 3d: Summarizer ─────────────────────────────────────────────────────

async def summarizer_node(state: RepoState) -> RepoState:
    """Generate beginner and expert summaries."""
    if state.get("error"):
        return state

    repo = state["repo_data"]
    analysis = state.get("analysis", {})
    readme_content = list(repo["key_files"].values())[0][:2000] if repo["key_files"] else "No README"

    context = f"""
Repository: {repo['metadata']['full_name']}
Description: {repo['metadata']['description']}
Stars: {repo['metadata']['stars']} | Language: {repo['metadata']['language']}
Project Type: {analysis.get('project_type', 'unknown')}
Architecture: {analysis.get('architecture', 'unknown')}
Purpose: {analysis.get('purpose', '')}
README: {readme_content}
"""
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: groq_chat(SUMMARIZER_PROMPT, context, temperature=0.5)
        )
        summary = parse_json_response(response)
        return {**state, "summary": summary}
    except Exception as e:
        return {**state, "summary": {
            "one_liner": repo['metadata'].get('description') or "A GitHub repository.",
            "beginner": "Could not generate summary. Please try again.",
            "expert": "",
            "use_cases": [],
            "getting_started": ""
        }}


# ─── Node 4: Merge ────────────────────────────────────────────────────────────

async def merge_node(state: RepoState) -> RepoState:
    """Final merge node - all results already in state."""
    return state


# ─── Build LangGraph ─────────────────────────────────────────────────────────

def build_graph():
    graph = StateGraph(RepoState)

    graph.add_node("fetch_repo", fetch_repo_node)
    graph.add_node("analyze_code", analyze_code_node)
    graph.add_node("flowchart", flowchart_node)
    graph.add_node("tech_stack", tech_stack_node)
    graph.add_node("issue_detector", issue_detector_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("merge", merge_node)

    graph.set_entry_point("fetch_repo")
    graph.add_edge("fetch_repo", "analyze_code")

    # Parallel branch
    graph.add_edge("analyze_code", "flowchart")
    graph.add_edge("analyze_code", "tech_stack")
    graph.add_edge("analyze_code", "issue_detector")
    graph.add_edge("analyze_code", "summarizer")

    # Converge
    graph.add_edge("flowchart", "merge")
    graph.add_edge("tech_stack", "merge")
    graph.add_edge("issue_detector", "merge")
    graph.add_edge("summarizer", "merge")
    graph.add_edge("merge", END)

    return graph.compile()


_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


async def run_analysis(repo_url: str) -> dict:
    """Run the full LangGraph analysis pipeline."""
    graph = get_graph()

    initial_state: RepoState = {
        "repo_url": repo_url,
        "repo_data": {},
        "analysis": {},
        "flowchart": "",
        "tech_stack": [],
        "issues": [],
        "summary": {},
        "score": "",
        "error": "",
    }

    final_state = await graph.ainvoke(initial_state)

    if final_state.get("error"):
        raise ValueError(final_state["error"])

    return {
        "summary": final_state.get("summary", {}),
        "flowchart": final_state.get("flowchart", ""),
        "tech_stack": final_state.get("tech_stack", []),
        "issues": final_state.get("issues", []),
        "score": final_state.get("score", "N/A"),
        "metadata": final_state.get("repo_data", {}).get("metadata", {}),
    }
