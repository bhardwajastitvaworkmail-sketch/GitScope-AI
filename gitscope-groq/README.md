# 🔭 GitScope AI (Groq Edition)

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
