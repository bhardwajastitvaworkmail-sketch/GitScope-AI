🔭 GitScope AI (Groq Edition)
Transform any GitHub repository into visual, interactive analysis — powered by Groq's ultra-fast Llama3 API.

🔗  | 🎥 

🚀 Overview
GitScope AI is a multi-agent framework designed to perform deep, autonomous repository intelligence. By leveraging LangGraph and Groq's Llama3, it acts as a virtual engineering lead—instantly auditing codebases, summarizing architectures, and identifying security vulnerabilities with the fastest inference speeds available today.

✨ Why Groq?
✅ Free Tier: Highly accessible via .

⚡ Ultra-Fast: Sub-second token generation for deep code reviews.

🦙 Llama3 70B: Enterprise-grade logic in an open-source model.

👥 Meet Team EliteCoders
We are a team of passionate developers from the University of Lucknow building the future of automated code intelligence.
Name ;Role; Email Address
1) Astitva Bhardwaj ;Team Lead; bastitva0@gmail.com
2) Vaibhav Singh; Member; vaibhavsingh1448@gmail.com
3)Kulshreshtha Sharma; Member; ps4338360@gmail.com
4)Harsh Tripathi ;Member ;aaharsh11z@gmail.com

🧠 Multi-Agent Architecture
GitScope AI operates using a Directed Cyclic Graph (DCG) orchestrated by LangGraph:

The Scout: Crawls the file tree and identifies core logic files.

The Auditor: Runs security checks and pattern analysis on selected snippets.

The Architect: Summarizes the tech stack and system flow.

The Reporter: Compiles all findings into a clean, interactive dashboard.

🚀 Quick Start
Step 1 — Backend
Configure your .env:

Step 2 — Frontend
⚡ Open: 

📁 Project Structure
backend/: FastAPI + LangGraph + Groq Multi-Agent Logic.

frontend/: React + Tailwind CSS Dashboard.

extension/: Chrome Extension (Manifest v3) for one-click analysis.

prompts/: Standardized AI prompt templates.

🗺️ Roadmap
[ ] Autonomous PRs: Let the agents suggest and open pull requests for fixes.

[ ] Newschain Integration: Immutable blockchain-based audit logs for repositories.

[ ] Multi-Repo Compare: Benchmarking two codebases against each other.

🛡️ License
Distributed under the MIT License. See LICENSE for more information.

Built by EliteCoders for the 2026 AI Innovation Hackathon.
> Transform any GitHub repository into visual, interactive analysis — powered by **Groq's free Llama3 API**.

## ✨ Why Groq?
- ✅ **Free** — generous free tier at console.groq.com
- ⚡ **Ultra-fast** — fastest LLM inference available
- 🦙 **Llama3 70B** — powerful open-source model

## 🚀 Quick Start

### Step 1 — Backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env    # Windows
# cp .env.example .env    # Mac/Linux
```

Edit `.env`:
```env
GROQ_API_KEY=gsk_...your-key...
GITHUB_TOKEN=ghp_...your-token...
GROQ_MODEL=llama3-70b-8192
HOST=0.0.0.0
PORT=8000
```

Start backend:
```bash
python -m uvicorn main:app --reload --port 8000
```

### Step 2 — Frontend
```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

### Step 3 — Get API Keys
- **Groq (free):** https://console.groq.com → API Keys → Create
- **GitHub:** https://github.com/settings/tokens → Generate new token

## 📁 Structure
```
backend/   FastAPI + LangGraph + Groq
frontend/  React + Tailwind
extension/ Chrome Extension (Manifest v3)
prompts/   AI prompt documentation
```

## 🧠 Available Groq Models
| Model | Speed | Quality |
|-------|-------|---------|
| `llama3-70b-8192` | Fast | Best ✅ |
| `llama3-8b-8192` | Fastest | Good |
| `mixtral-8x7b-32768` | Fast | Great |
| `gemma2-9b-it` | Fast | Good |
