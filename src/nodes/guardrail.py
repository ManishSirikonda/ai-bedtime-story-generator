from langchain_core.messages import SystemMessage
from src.state import AgentState, SafetyCheck
from src.utils.tools import model

safety_model = model.with_structured_output(SafetyCheck, method="function_calling")

def guardrail_node(state: AgentState):
    print("--- [GUARDRAIL] CHECKING SAFETY... ---")
    prompt = (
        "Check if the following story beat or theme is appropriate for kids aged 5-10. "
        "Strictly refuse topics related to: sex, murder, harassment, or extreme violence. "
        "Also, decide if we need real-world facts to make the story great. "
        "User Input: " + state["user_input"]
    )
    check = safety_model.invoke(prompt)
    if not check.is_safe:
        print(f"--- [REJECTED] {check.reason} ---")
        return {
            "status": "rejected",
            "rejection_reason": check.reason
        }
    return {
        "status": "research" if check.needs_search else "retry_writer",
        "needs_search": check.needs_search
    }
