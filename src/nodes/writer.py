from langchain_core.messages import SystemMessage
from src.state import AgentState
from src.utils.tools import model

WRITER_PROMPT = """You are a warm, magical bedtime storyteller for kids aged 5 to 10.
This is an ongoing session. Read the full message history carefully.
If previous story sections exist, you MUST continue the story naturally from where it left off.
If research data is provided, incorporate those facts for a more educational but fun story.
Keep it detailed (5-6 paragraphs), safe, and use vivid vocabulary.
"""

def writer_node(state: AgentState):
    print("--- [WRITER] GENERATING STORY... ---")
    messages = [SystemMessage(content=WRITER_PROMPT)] + state["messages"]
    
    if state.get("research_data"):
        messages.append(SystemMessage(content=f"RESEARCH FACTS: {state['research_data']}"))
        
    if state.get("judge_feedback"):
        messages.append(SystemMessage(content=f"JUDGE FEEDBACK: {state['judge_feedback']}"))
        
    response = model.invoke(messages)
    return {
        "draft_story": response.content,
        "messages": [response],
        "status": "retry_writer"
    }
