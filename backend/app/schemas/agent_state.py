# backend/app/schemas/agent_state.py
from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict, total=False):
    # --- BAGIAN INPUT DAN KONTEKS ---
    user_query: str
    chat_history: List[Dict[str, Any]]
    
    # --- PERGANTIAN NAMA DI SINI ---
    # Menampung info sesi, termasuk thread_id (session_id)
    session_info: Dict[str, Any]

    # --- BAGIAN ALUR KERJA ---
    tool_calls: Optional[List[Dict[str, Any]]]
    workflow_status: str

    # --- BAGIAN LOGGING & ERROR ---
    performance_trace: Dict[str, float]
    error_details: Optional[str]
    error_source_node: Optional[str]
    
    # Field lama (bisa dihapus nanti)
    plan_validation_result: Optional[str] 
    repair_attempts: int