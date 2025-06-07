# backend/app/langgraph_workflow/nodes/generate_error_response.py
from typing import Dict, Any, Optional
import sys
from backend.app.schemas.agent_state import AgentState

def generate_error_response_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: generate_error_response_node ---", file=sys.stderr)
    
    user_message = state.get("error_message_for_user", "Terjadi kesalahan yang tidak diketahui saat memproses permintaan Anda.")
    technical_details = state.get("technical_error_details", "Tidak ada detail teknis tambahan.")
    current_failed_node = state.get("current_node_name", "UNKNOWN_NODE") # Node yang menyebabkan error

    print(f"generate_error_response_node: Handling error from node '{current_failed_node}'. User message: '{user_message}'", file=sys.stderr)

    # State ini akan menjadi output akhir dari graph dalam kasus error
    return {
        "user_query": state.get("user_query"),
        "session_id": state.get("session_id"),
        "workflow_status": "error",
        "error_message_for_user": user_message,
        "technical_error_details": technical_details,
        "current_node_name": "generate_error_response" # Perbarui nama node saat ini
        # Field lain dari AgentState bisa dipertahankan atau dibersihkan sesuai kebutuhan
    }