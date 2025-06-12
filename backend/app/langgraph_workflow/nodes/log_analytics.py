# backend/app/langgraph_workflow/nodes/log_analytics.py
import json
import uuid
import os
from datetime import datetime, timezone
from typing import Dict, Any

from backend.app.schemas.agent_state import AgentState

LOG_FILE_PATH = "logs/analytics.log"

def _ensure_log_dir_exists():
    """Memastikan direktori 'logs' ada."""
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def log_analytics_node(state: AgentState) -> Dict[str, Any]:
    """
    Mencatat telemetri dari sebuah interaksi ke dalam file log.
    """
    print("--- Logging Analytics ---")
    _ensure_log_dir_exists()

    try:
        status = state.get("workflow_status", "completed")
        if state.get("error_details"):
            status = "error"

        # --- PERGANTIAN NAMA DI SINI ---
        session_id = state.get("session_info", {}).get("thread_id")
        # --------------------------

        log_entry = {
            "log_id": str(uuid.uuid4()),
            "session_id": session_id,
            "event_timestamp": datetime.now(timezone.utc).isoformat(),
            "user_query_text": state.get("user_query"),
            # ... sisa field tetap sama ...
            "workflow_status": status,
            "total_duration_ms": state.get("performance_trace", {}).get("total_duration_ms"),
            "llm_calls_count": len([msg for msg in state.get("chat_history", []) if msg.get("role") == "assistant"]),
            "tool_calls_count": len([msg for msg in state.get("chat_history", []) if msg.get("role") == "tool"]),
            "error_source_node": state.get("error_source_node"),
            "error_details": state.get("error_details"),
        }
        
        with open(LOG_FILE_PATH, "a") as f:
            f.write(json.dumps(log_entry, default=str) + "\n")
        
        print(f"  -> Log berhasil ditulis untuk session {log_entry['session_id']}")

    except Exception as e:
        print(f"  🔥 [ERROR] Gagal menulis analytics log: {e}")

    return {}