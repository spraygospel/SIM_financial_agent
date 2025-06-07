# backend/app/langgraph_workflow/graph.py
from langgraph.graph import StateGraph, END
from backend.app.schemas.agent_state import AgentState 
from .nodes.understand_query import understand_query_node
from .nodes.consult_schema import consult_schema_node
from .nodes.plan_execution import plan_execution_node
from .nodes.execute_query import execute_query_node
from .nodes.validate_results import validate_results_node # BARU
from .nodes.replace_placeholders import replace_placeholders_node # BARU
from .nodes.generate_error_response import generate_error_response_node # BARU

workflow = StateGraph(AgentState)

# Tambahkan node-node ke dalam graph
workflow.add_node("understand_query", understand_query_node)
workflow.add_node("consult_schema", consult_schema_node)
workflow.add_node("plan_execution", plan_execution_node)
workflow.add_node("execute_query", execute_query_node)
workflow.add_node("validate_results", validate_results_node) # BARU
workflow.add_node("replace_placeholders", replace_placeholders_node) # BARU
workflow.add_node("generate_error_response", generate_error_response_node) # BARU


# Tentukan titik awal (entry point) graph
workflow.set_entry_point("understand_query")

# Tentukan alur (edges) antar node
workflow.add_edge("understand_query", "consult_schema")
workflow.add_edge("consult_schema", "plan_execution")
workflow.add_edge("plan_execution", "execute_query")
workflow.add_edge("execute_query", "validate_results") # BARU: execute_query -> validate_results

# Edge kondisional setelah validasi
def decide_after_validation(state: AgentState) -> str:
    validation_status = state.get("validation_status")
    if validation_status == "passed" or validation_status == "passed_with_warnings" or validation_status == "passed_with_notes":
        return "proceed_to_format"
    # Mencakup 'failed_critical', 'failed_no_data', atau status gagal lainnya
    else: 
        return "handle_error"

workflow.add_conditional_edges(
    "validate_results",
    decide_after_validation,
    {
        "proceed_to_format": "replace_placeholders",
        "handle_error": "generate_error_response" 
    }
)

# Alur dari node sukses terakhir dan node error ke END
workflow.add_edge("replace_placeholders", END)
workflow.add_edge("generate_error_response", END)


app_graph = workflow.compile()