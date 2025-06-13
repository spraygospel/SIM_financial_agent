# backend/app/langgraph_workflow/graph.py

from langgraph.graph import StateGraph, END
from backend.app.schemas.agent_state import AgentState
from .nodes.llm_caller import llm_caller_node
from .nodes.tool_executor import tool_executor_node

workflow = StateGraph(AgentState)

# 1. Definisikan node
workflow.add_node("agent", llm_caller_node)
workflow.add_node("action", tool_executor_node)

# 2. Tentukan titik masuk
workflow.set_entry_point("agent")

# 3. Definisikan logika percabangan
def should_continue(state: AgentState):
    """
    Setelah agent (LLM) berjalan, putuskan langkah selanjutnya.
    - Jika intent ACKNOWLEDGE, langsung selesai.
    - Jika ada tool yang dipanggil, eksekusi tool.
    - Jika tidak ada tool call (respons final), selesai.
    """
    if state.get("intent") == "ACKNOWLEDGE":
        return END
    
    if state.get("tool_calls"):
        return "action"
        
    return END

# 4. Tambahkan semua edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "action": "action",
        END: END
    }
)

workflow.add_edge("action", "agent")

# 5. Kompilasi graph
app = workflow.compile()