# backend/app/services/agent_service.py
import asyncio
import time
import json
import traceback
from backend.app.core.session_manager import session_manager
from backend.app.langgraph_workflow.graph import app as langgraph_app
from backend.app.langgraph_workflow.nodes.log_analytics import log_analytics_node
from backend.app.langgraph_workflow.prompts import SYSTEM_PROMPT
from typing import Dict, List, Any

conversation_memory: Dict[str, List[Dict[str, Any]]] = {}

class AgentService:
    async def process_query_and_stream_updates(self, session_id: str, user_query: str):
        
        async def send_event(event_type: str, data: Dict):
            if session_id in session_manager.sessions:
                await session_manager.send_to_queue(session_id, {"event_type": event_type, "data": data})

        try:
            start_time = time.time()
            planning_steps = [
                {"text": "Memahami permintaan...", "status": "pending"},
                {"text": "Mengkonsultasikan peta data...", "status": "pending"},
                {"text": "Merencanakan pengambilan data...", "status": "pending"},
                {"text": "Mengambil data dari database...", "status": "pending"},
                {"text": "Menyusun laporan akhir...", "status": "pending"},
            ]

            async def send_plan_update(active_index: int):
                steps = [
                    {**s, "status": "completed" if i < active_index else ("active" if i == active_index else "pending")}
                    for i, s in enumerate(planning_steps)
                ]
                await send_event("PLANNING_UPDATE", {"steps": steps})

            # Langkah 0: Agent mulai berpikir
            await send_plan_update(0)

            # Persiapan untuk memanggil LangGraph
            chat_history = conversation_memory.get(session_id, [])
            if not chat_history:
                chat_history.append({"role": "system", "content": SYSTEM_PROMPT})
            chat_history.append({"role": "user", "content": user_query})
            
            config = {"configurable": {"thread_id": session_id}}
            inputs = {"chat_history": chat_history, "user_query": user_query}
            
            final_state = None
            async for event in langgraph_app.astream_events(inputs, config=config, version="v2"):
                kind = event["event"]
                # Selalu tangkap state terakhir yang valid
                if "agent_state" in event.get("data", {}): final_state = event["data"]["agent_state"]
                elif "output" in event.get("data", {}) and isinstance(event["data"]["output"], dict): final_state = event["data"]["output"]

                if kind == "on_tool_start" and event["name"] == "get_relevant_schema":
                    await send_plan_update(1) # Langkah 1: Mengkonsultasikan...
                
                elif kind == "on_tool_end" and event["name"] == "get_relevant_schema":
                    await send_plan_update(2) # Langkah 2: Merencanakan...

                elif kind == "on_tool_start" and event["name"] == "search_read":
                    await send_plan_update(3) # Langkah 3: Mengambil data...
            
            # Setelah loop selesai, kita sudah memiliki final_state
            if not final_state: raise ValueError("Gagal mendapatkan state akhir.")

            await send_plan_update(4) # Langkah 4: Menyusun laporan...

            # Format dan kirim hasil akhir
            final_assistant_message = next(
                (msg for msg in reversed(final_state.get("chat_history", [])) if msg.get("role") == "assistant"),
                None
            )

            if final_assistant_message and final_assistant_message.get("content"):
                content_str = final_assistant_message.get("content", "{}")
                try:
                    response_data = json.loads(content_str.strip().strip("```json").strip())
                except (json.JSONDecodeError, AttributeError):
                    response_data = {"final_narrative": content_str}
            else:
                # Fallback jika tidak ada respons dari asisten (seharusnya tidak terjadi)
                response_data = {"final_narrative": "Maaf, saya tidak dapat memberikan respons saat ini."}
            
            await send_event("FINAL_RESULT", response_data)

            # Logging
            end_time = time.time()
            final_state.setdefault("performance_trace", {})["total_duration_ms"] = (end_time - start_time) * 1000
            final_state["workflow_status"] = "completed"
            log_analytics_node(final_state)
            conversation_memory[session_id] = final_state.get("chat_history", [])

        except Exception as e:
            await send_event("WORKFLOW_ERROR", {"user_message": "Terjadi kesalahan."})
        finally:
            await send_event("STREAM_END", {})

agent_service = AgentService()