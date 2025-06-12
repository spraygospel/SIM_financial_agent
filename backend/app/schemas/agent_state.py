# backend/app/schemas/agent_state.py
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict, total=False):
    # Input awal
    user_query: str
    
    # Riwayat pesan manual kita dalam format dict
    chat_history: List[Dict[str, Any]]
    
    # Output dari LLM yang perlu dieksekusi
    tool_calls: List[Dict[str, Any]]
    
    # Konten respons akhir dari LLM
    final_response: str