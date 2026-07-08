#Pulse Pulse is a lightweight Streamlit app that analyzes public GitHub repositories and generates a structured technical report using an AI-powered agent.

Subheading: GitHub Repo Analyst https://share.streamlit.io/?utm_source=streamlit&utm_medium=referral&utm_campaign=main&utm_content=-ss-streamlit-io-topright

What this app does
Reads a GitHub repository URL
Uses GitHub API tools to inspect metadata, file structure, and recent commits
Generates a report with architecture, tech stack, health signals, and red flags
Saves the generated report locally in reports/
Team Elite Coders
Name	Role	Email
Astitva Bhardwaj	Team Lead	bastitva0@gmail.com
Vaibhav Singh	Member	vaibhavsingh1448@gmail.com
Kulshreshtha Sharma	Member	ps4338360@gmail.com
Harsh Tripathi	Member	aaharsh11z@gmail.com
LinkedIn: https://www.linkedin.com/in/astitva-bhardwajlu

Gmail ID: bastitva0@gmail.com

Setup
Rename .env.example to .env and fill in your keys locally.
For Streamlit Cloud, set GITHUB_TOKEN, GEMINI_API_KEY, and OPENAI_API_KEY in the app secrets UI.
Do NOT commit .env or .streamlit/secrets.toml. Only commit .env.example or .streamlit/secrets.toml.example.
Deployment
Create a .env file in the project root with:
GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
Install dependencies:
pip install -r requirements.txt
Run the app:
streamlit run app.py
Open the browser at:
http://localhost:8501
Notes
Do not commit .env to GitHub.
The app currently uses Gemini as the LLM backend.
The example placeholder URL in the app input is set to a GitHub repo URL for quick testing.
