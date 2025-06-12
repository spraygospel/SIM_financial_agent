# backend/app/services/agent_service.py
import time # Impor time
from backend.app.langgraph_workflow.graph import app as langgraph_app
from backend.app.langgraph_workflow.nodes.log_analytics import log_analytics_node
from backend.app.langgraph_workflow.prompts import SYSTEM_PROMPT
from typing import Dict, List, Any

conversation_memory: Dict[str, List[Dict[str, Any]]] = {}

class AgentService:
    async def process_query(self, user_query: str, session_id: str):
        start_time = time.time()
        chat_history = conversation_memory.get(session_id, [])
        
        if not chat_history:
            chat_history.append({"role": "system", "content": SYSTEM_PROMPT})

        chat_history.append({"role": "user", "content": user_query})

        config = {"configurable": {"thread_id": session_id}}
        
        # --- PERGANTIAN NAMA DI SINI ---
        inputs = {
            "chat_history": chat_history,
            "user_query": user_query,
            "performance_trace": {},
            "session_info": {"thread_id": session_id} # Ganti nama dari 'configurable'
        }
        # -------------------------------
        
        final_state = await langgraph_app.ainvoke(inputs, config=config)
        
        end_time = time.time()
        total_duration_ms = (end_time - start_time) * 1000
        
        if final_state:
            # Panggil logger secara manual
            if "performance_trace" not in final_state:
                final_state["performance_trace"] = {}
            final_state["performance_trace"]["total_duration_ms"] = total_duration_ms
            log_analytics_node(final_state)
        
        updated_history = final_state.get("chat_history", [])
        conversation_memory[session_id] = updated_history
        
        final_response_content = "Maaf, terjadi kesalahan dan saya tidak dapat memberikan respons."
        if updated_history:
            for i in range(len(updated_history) - 1, -1, -1):
                message = updated_history[i]
                if message.get("role") == "assistant" and not message.get("tool_calls"):
                    final_response_content = message.get("content", "")
                    break
        
        return {"response": final_response_content}
agent_service = AgentService()