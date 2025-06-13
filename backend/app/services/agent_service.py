# backend/app/services/agent_service.py
import asyncio
import time
import json
import traceback
from backend.app.langgraph_workflow.graph import app as langgraph_app
from backend.app.langgraph_workflow.nodes.log_analytics import log_analytics_node
from backend.app.langgraph_workflow.prompts import SYSTEM_PROMPT
from typing import Dict, List, Any

# Pindahkan ini ke level modul, bukan di dalam kelas
conversation_memory: Dict[str, List[Dict[str, Any]]] = {}

class AgentService:

    async def _run_agent_and_get_response(self, session_id: str, user_query: str) -> dict:
        """Menjalankan proses LangGraph dan mengembalikan state akhir."""
        chat_history = conversation_memory.get(session_id, [])
        if not chat_history:
            chat_history.append({"role": "system", "content": SYSTEM_PROMPT})
        chat_history.append({"role": "user", "content": user_query})

        config = {"configurable": {"thread_id": session_id}}
        inputs = {
            "chat_history": chat_history,
            "user_query": user_query,
            "performance_trace": {},
            "session_info": {"thread_id": session_id}
        }

        final_state = await langgraph_app.ainvoke(inputs, config=config)
        if not final_state:
            raise ValueError("Gagal mendapatkan state akhir dari proses agent.")
        return final_state

    def _format_response(self, final_state: dict) -> dict:
        """Memformat state akhir menjadi JSON yang akan dikirim ke frontend."""
        last_message = final_state.get("chat_history", [])[-1]
        content_str = last_message.get("content", "{}")
        
        try:
            if content_str.strip().startswith("```json"):
                content_str = content_str.strip()[7:-3]
            response_data = json.loads(content_str)
        except json.JSONDecodeError:
            response_data = {"final_narrative": content_str}
        
        return response_data
    
    # --- KEMBALIKAN METODE process_query ---
    async def process_query(self, user_query: str, session_id: str) -> dict:
        start_time = time.time()
        try:
            final_state = await self._run_agent_and_get_response(session_id, user_query)
            
            response_data = self._format_response(final_state)

            # Lakukan logging
            end_time = time.time()
            final_state.setdefault("performance_trace", {})["total_duration_ms"] = (end_time - start_time) * 1000
            final_state["workflow_status"] = "completed"
            log_analytics_node(final_state)
            conversation_memory[session_id] = final_state.get("chat_history", [])

            return {"response": response_data}
        
        except Exception as e:
            traceback.print_exc()
            raise

# Buat satu instance untuk digunakan di seluruh aplikasi
agent_service = AgentService()