from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState, StoryScorecard
from src.utils.tools import model

judge_model = model.with_structured_output(StoryScorecard, method="function_calling")

def judge_node(state: AgentState):
    print("--- [JUDGE] REVIEWING STORY... ---")
    count = state.get("retry_count", 0)
    if count >= 3:
        print("--- [SAFETY] MAX RETRIES REACHED. ---")
        return {"status": "approved", "retry_count": count + 1}
    
    story = state.get("draft_story", "")
    system_prompt = (
        "Quickly review this bedtime story for kids 5-10. "
        "It must be safe, happy, and detailed (at least 5 paragraphs). "
        "If it is too short or scary, ask for a 'retry_writer'."
    )
    
    report = judge_model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Review this story: {story}")
    ])
    
    return {
        "judge_feedback": report.reasoning,
        "status": report.action,
        "retry_count": count + 1
    }
