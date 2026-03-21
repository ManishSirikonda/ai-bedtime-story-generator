from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import AgentState
from src.nodes.guardrail import guardrail_node
from src.nodes.research import research_node
from src.nodes.writer import writer_node
from src.nodes.judge import judge_node

# 1. Initialize the Graph
builder = StateGraph(AgentState)

# 2. Add our Nodes
builder.add_node("guardrail", guardrail_node)
builder.add_node("research", research_node)
builder.add_node("writer", writer_node)
builder.add_node("judge", judge_node)

# 3. Define the START
builder.add_edge(START, "guardrail")

# 4. Define Logic after Guardrail
def route_after_guardrail(state: AgentState):
    if state["status"] == "rejected":
        return END
    if state["status"] == "research":
        return "research"
    return "writer"

builder.add_conditional_edges("guardrail", route_after_guardrail)

# 5. Fixed connections
builder.add_edge("research", "writer")
builder.add_edge("writer", "judge")

# 6. Define Logic after Judge
def route_after_judge(state: AgentState):
    if state["status"] == "approved":
        return END
    return "writer"

builder.add_conditional_edges("judge", route_after_judge)

# 7. Compile the Graph
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
