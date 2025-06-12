# backend/app/langgraph_workflow/graph.py (Manual State)
from langgraph.graph import StateGraph, END
from backend.app.schemas.agent_state import AgentState
from .nodes.tool_executor import tool_executor_node
from .nodes.llm_caller import llm_caller_node

workflow = StateGraph(AgentState)

workflow.add_node("agent", llm_caller_node)
workflow.add_node("action", tool_executor_node)

workflow.set_entry_point("agent")

def should_continue(state: AgentState):
    if state.get("tool_calls"):
        return "action"
    return END

workflow.add_conditional_edges("agent", should_continue, {"action": "action", END: END})
workflow.add_edge("action", "agent")

app = workflow.compile()