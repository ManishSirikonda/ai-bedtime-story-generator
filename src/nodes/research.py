from src.state import AgentState
from src.utils.tools import tavily_tool

def research_node(state: AgentState):
    print("--- [RESEARCH] QUICK FACT FINDING... ---")
    try:
        results = tavily_tool.invoke(state["user_input"])
        if isinstance(results, list):
            facts = "\n".join([r.get("content", str(r)) for r in results])
        else:
            facts = str(results)
        return {
            "research_data": facts,
            "status": "retry_writer"
        }
    except Exception as e:
        print(f"--- [RESEARCH FAILED] {e} ---")
        return {
            "research_data": f"Warning: Research failed ({e}). Proceeding with internal knowledge.",
            "status": "retry_writer"
        }
