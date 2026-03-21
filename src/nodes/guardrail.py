from langchain_core.messages import SystemMessage
from src.state import AgentState, SafetyCheck
from src.utils.tools import model

safety_model = model.with_structured_output(SafetyCheck, method="function_calling")

# Keywords that indicate the user is asking about something time-sensitive
SEARCH_KEYWORDS = [
    "recently", "latest", "new release", "launched", "just came out",
    "announced", "current", "today", "this year", "2025", "2026"
]

def guardrail_node(state: AgentState):
    print("--- [GUARDRAIL] CHECKING SAFETY... ---")
    prompt = (
        "Check if the following story beat or theme is appropriate for kids aged 5-10. "
        "SAFETY RULES: Refuse topics involving: sex, murder, killing, death, suicide, harassment, extreme violence, or graphic content. "
        "Also decide if the topic would benefit from a web search for real-world facts. "
        "User Input: " + state["user_input"]
    )
    check = safety_model.invoke(prompt)
    if not check.is_safe:
        print(f"--- [REJECTED] {check.reason} ---")
        return {
            "status": "rejected",
            "rejection_reason": check.reason
        }
    
    # Code-level override: force search if input contains time-sensitive keywords
    user_lower = state["user_input"].lower()
    force_search = any(kw in user_lower for kw in SEARCH_KEYWORDS)
    needs_search = check.needs_search or force_search
    
    if force_search and not check.needs_search:
        print("--- [GUARDRAIL] Detected time-sensitive keyword, forcing research. ---")

    return {
        "status": "research" if needs_search else "retry_writer",
        "needs_search": needs_search
    }
