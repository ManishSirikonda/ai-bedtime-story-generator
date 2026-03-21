# 🌙 AI Bedtime Storyteller

An AI-powered bedtime story generator for children aged 5–10, featuring a **React/TypeScript** frontend and a **FastAPI/LangGraph** backend. The application orchestrates multiple AI agents in a structured workflow to create safe, educational, and imaginative stories, presented in a magical, premium dark-themed UI.

## ✨ Features

- **Beautiful Web Interface** — A premium, glassmorphism-inspired UI with glowing animations and chapter-by-chapter story continuity.
- **Content Guardrails** — Automatically screens user input for age-inappropriate topics before any story is generated.
- **Smart Research** — Optionally enriches stories with real-world facts via [Tavily](https://tavily.com/) web search when the topic benefits from factual context.
- **Iterative Quality Control** — A judge agent reviews each draft for safety, tone, and length, sending it back for rewrites if needed (up to 3 attempts).
- **Multi-Turn Storytelling** — Continue the story by adding new "story beats" across turns, building an evolving narrative with full conversational memory.

## 🏗️ Architecture

The application is split into a decoupled **Frontend (React)** and **Backend (FastAPI/LangGraph)**:

### Backend Workflow (LangGraph)
Uses a **StateGraph** to orchestrate specialized nodes:
```text
User Input → 🛡️ Guardrail → 📚 Research (optional) → ✍️ Writer ⇄ ⚖️ Judge → Story Output
```

## 📁 Project Structure

```text
├── backend/
│   ├── server.py         # Entry point — FastAPI Server
│   ├── requirements.txt  # Python dependencies
│   ├── .env              # API keys (not tracked in git)
│   └── src/
│       ├── state.py      # State schema & Pydantic models
│       ├── graph.py      # LangGraph workflow definition
│       ├── nodes/        # AI Agents (guardrail, research, writer, judge)
│       └── utils/        # Shared LLM & tool instances
└── frontend/             # React SPA Frontend
    ├── package.json      # Node dependencies
    ├── vite.config.ts    # Vite Configuration
    └── src/
        ├── App.tsx       # Main React Component & State Management
        ├── api.ts        # API client for FastAPI backend
        └── components/   # Modular UI Components
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Tavily API key](https://app.tavily.com/)

### 1. Set up the Backend (FastAPI)

1. Open a terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables locally by creating a `.env` file in the `backend/` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```
5. Run the server:
   ```bash
   uvicorn server:app --reload --port 8000
   ```
   *The backend will be running at `http://localhost:8000`*

### 2. Set up the Frontend (React / Vite)

1. Open a **new** terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the provided local URL (usually `http://localhost:5173`) in your browser to experience the magic!

## 🛠️ Tech Stack

**Frontend:**
- [React](https://react.dev/) — User Interface
- [TypeScript](https://www.typescriptlang.org/) — Type Safety
- [Vite](https://vitejs.dev/) — Build Tool & Dev Server

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) — High-performance Python API Framework
- [LangGraph](https://github.com/langchain-ai/langgraph) — Agent orchestration & state management
- [LangChain](https://github.com/langchain-ai/langchain) — LLM interface
- [OpenAI GPT-3.5/4](https://platform.openai.com/) — Core language models
- [Tavily](https://tavily.com/) — AI-optimized web search for fact-finding

## 📄 License
MIT
