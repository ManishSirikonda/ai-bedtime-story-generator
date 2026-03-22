import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.graph import graph
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow the React frontend to call our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://manishsirikonda.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory session store
sessions: dict = {}

# --- Request Models ---

class GenerateRequest(BaseModel):
    theme: str
    session_id: str | None = None

class ContinueRequest(BaseModel):
    session_id: str
    feedback: str

# --- Endpoints ---

@app.post("/api/generate")
def generate_story(req: GenerateRequest):
    session_id = req.session_id or str(uuid.uuid4())

    state = {
        "user_input": req.theme,
        "messages": [HumanMessage(content=req.theme)],
        "draft_story": "",
        "research_data": None,
        "judge_feedback": None,
        "status": "retry_writer",
        "needs_search": False,
        "retry_count": 0,
    }
    config = {"configurable": {"thread_id": session_id}, "recursion_limit": 20}
    final_state = graph.invoke(state, config=config)
    sessions[session_id] = final_state

    if final_state.get("status") == "rejected":
        return {
            "session_id": session_id,
            "status": "rejected",
            "reason": final_state.get("rejection_reason"),
        }

    return {
        "session_id": session_id,
        "status": "approved",
        "story": final_state.get("draft_story", ""),
    }

@app.post("/api/continue")
def continue_story(req: ContinueRequest):
    prev = sessions.get(req.session_id, {})

    state = {
        "user_input": req.feedback,
        "messages": prev.get("messages", []) + [HumanMessage(content=req.feedback)],
        "draft_story": prev.get("draft_story", ""),
        "research_data": None,
        "judge_feedback": None,
        "status": "retry_writer",
        "needs_search": False,
        "retry_count": 0,
    }
    config = {"configurable": {"thread_id": req.session_id}, "recursion_limit": 20}
    final_state = graph.invoke(state, config=config)
    sessions[req.session_id] = final_state

    if final_state.get("status") == "rejected":
        return {
            "session_id": req.session_id,
            "status": "rejected",
            "reason": final_state.get("rejection_reason"),
        }

    return {
        "session_id": req.session_id,
        "status": "approved",
        "story": final_state.get("draft_story", ""),
    }