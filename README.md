# Cognito Hub 🧠: Strategic Research Engine

**Cognito Hub** is a cutting-edge **Autonomous Multi-Agent AI System** that transforms how deep research and strategic analysis are performed. By orchestrating a team of specialized agents, it can crawl the web, validate findings against a knowledge base, and provide future-proof strategic recommendations on any topic.

### 🌐 Live Links
- **Live Demo (Frontend):** [https://multi-agent-dun.vercel.app/](https://multi-agent-dun.vercel.app/)
- **Live API (Backend):** [https://multi-agent-azqa.onrender.com](https://multi-agent-azqa.onrender.com)


## 🚀 The Multi-Agent Architecture

Cognito Hub uses **LangGraph** to manage a sophisticated state-based workflow between three specialized agents:

1.  **Research Scout 🔍**: Executes deep, multi-perspective web searches using the Tavily API to gather real-time data.
2.  **Critical Analyst 📊**: Cross-references findings with internal knowledge bases to identify gaps, contradictions, and key trends.
3.  **Strategy Advisor 💡**: Projects future impacts based on synthesized data and generates actionable strategic roadmaps.

## ✨ Key Features

- **Dynamic Deep Search**: Intelligent web crawling tailored to the specific user query.
- **Real-time Reasoning Stream**: Watch the agents "think" and collaborate in real-time via a glassmorphic terminal.
- **AI Co-pilot**: An interactive chat interface for follow-up questions and granular research.
- **Premium Design**: A state-of-the-art Glassmorphism UI with smooth animations and responsive layout.

## 🛠️ Tech Stack

- **Intelligence**: Groq (Llama 3.3 70B - Ultra High-Speed Reasoning)
- **Orchestration**: LangGraph, LangChain
- **Backend**: Python, FastAPI, Pydantic v2
- **Research Engine**: Tavily Deep Search API
- **Frontend**: Vanilla JS, Modern CSS3 (Grid, Flexbox, Glassmorphism)

## 📂 Project Structure

```text
multi-agent/
├── backend/
│   ├── main.py        # FastAPI Server
│   ├── agents.py      # LangGraph Agent logic
│   ├── state.py       # Pydantic State definitions
│   └── tools.py       # Research & Knowledge tools
├── frontend/
│   ├── index.html     # Dashboard Layout
│   ├── style.css      # Premium Design System
│   └── app.js         # Frontend Logic & API Connect
├── requirements.txt   # Backend Dependencies
└── DEPLOYMENT.md      # Step-by-step Hosting Guide
```

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/your-username/cognito-hub.git
cd cognito-hub
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root:
```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

### 3. Run Servers
**Backend:**
```bash
python -m uvicorn backend.main:app --reload
```
**Frontend:**
```bash
cd frontend
python -m http.server 5173
```
Access the dashboard at `http://localhost:5173`.
