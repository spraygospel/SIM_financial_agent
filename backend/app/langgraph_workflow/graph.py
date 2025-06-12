# backend/app/langgraph_workflow/graph.py
from langgraph.graph import StateGraph, END
from backend.app.schemas.agent_state import AgentState
from .nodes.llm_caller import llm_caller_node
from .nodes.tool_executor import tool_executor_node
from .nodes.log_analytics import log_analytics_node # Impor node baru

workflow = StateGraph(AgentState)

# 1. Definisikan semua node
workflow.add_node("agent", llm_caller_node)
workflow.add_node("action", tool_executor_node)
workflow.add_node("analytics_logger", log_analytics_node) # Tambahkan node logger

# 2. Tentukan titik masuk
workflow.set_entry_point("agent")

# 3. Definisikan logika percabangan
def should_continue(state: AgentState):
    """
    Setelah agent (LLM) berjalan, putuskan langkah selanjutnya.
    Apakah ada tool yang dipanggil? Jika ya, eksekusi. Jika tidak, selesai (melalui logger).
    """
    if state.get("tool_calls"):
        return "action"
    # Jika tidak ada tool call, ini adalah respons final.
    # Tandai sebagai selesai dan kirim ke logger.
    state["workflow_status"] = "completed" 
    return "analytics_logger"

# 4. Tambahkan semua edge
# Dari 'agent', putuskan apakah akan ke 'action' atau 'analytics_logger'
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "action": "action",
        "analytics_logger": "analytics_logger" # Arahkan ke logger jika selesai
    }
)

# Dari 'action', selalu kembali ke 'agent'
workflow.add_edge("action", "agent")

# Dari 'analytics_logger', alur kerja benar-benar berakhir
workflow.add_edge("analytics_logger", END)


# 5. Kompilasi graph
app = workflow.compile()