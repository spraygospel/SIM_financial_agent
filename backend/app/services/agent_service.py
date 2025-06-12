# backend/app/services/agent_service.py
from backend.app.langgraph_workflow.graph import app as langgraph_app
from typing import Dict, List, Any

# Ini akan berfungsi sebagai "memori" in-memory kita.
# Di produksi, ini bisa diganti dengan Redis atau database lain.
conversation_memory: Dict[str, List[Dict[str, Any]]] = {}

class AgentService:
    async def process_query(self, user_query: str, session_id: str):
        # 1. Ambil riwayat percakapan dari memori
        chat_history = conversation_memory.get(session_id, [])
        
        # 2. Tambahkan pesan baru dari pengguna ke riwayat
        chat_history.append({"role": "user", "content": user_query})

        # 3. Siapkan input untuk LangGraph
        config = {"configurable": {"thread_id": session_id}}
        inputs = {
            "chat_history": chat_history,
            "user_query": user_query, # Tetap simpan query asli untuk referensi
        }
        
        # 4. Panggil alur kerja LangGraph
        final_state = await langgraph_app.ainvoke(inputs, config=config)
        
        # 5. Simpan riwayat percakapan yang sudah diperbarui kembali ke memori
        updated_history = final_state.get("chat_history", [])
        conversation_memory[session_id] = updated_history
        
        # 6. Logika cerdas untuk mengekstrak respons akhir
        # Cari pesan 'assistant' terakhir yang TIDAK memiliki 'tool_calls'.
        # Itulah respons yang ditujukan untuk pengguna.
        final_response_content = "Maaf, terjadi kesalahan dan saya tidak dapat memberikan respons."
        if updated_history:
            for i in range(len(updated_history) - 1, -1, -1):
                message = updated_history[i]
                if message.get("role") == "assistant" and not message.get("tool_calls"):
                    final_response_content = message.get("content", "")
                    break
        
        return {"response": final_response_content}

agent_service = AgentService()