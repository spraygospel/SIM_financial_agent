# backend/app/langgraph_workflow/nodes/tool_executor.py
import json
from typing import Dict, Any
import asyncio
from backend.app.schemas.agent_state import AgentState
from backend.app.tools import database_tools, graphiti_tools

# Hanya ada satu tool sekarang
available_tools = {
    "search_read": database_tools.search_read,
    "get_relevant_schema": graphiti_tools.get_relevant_schema,
}

# Fungsi tool_executor_node tidak perlu diubah, karena ia generik

async def tool_executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Mengeksekusi tool yang diminta oleh LLM.
    Sekarang bisa menangani fungsi sinkron dan asinkron (async).
    """
    print("--- Executing Tools ---")
    
    last_message = state["chat_history"][-1]
    tool_calls = last_message.get("tool_calls", [])
    
    new_messages_to_add = []

    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        tool_args_str = tool_call["function"]["arguments"]
        tool_call_id = tool_call["id"]
        
        print(f"  -> Preparing to call tool: {tool_name}")
        print(f"  -> [DEBUG] Argumen mentah dari LLM (string):\n{tool_args_str}")

        tool_to_call = available_tools.get(tool_name)
        
        if not tool_to_call:
            tool_output = f"Error: Tool '{tool_name}' is not a valid tool."
        else:
            try:
                tool_args = json.loads(tool_args_str)
                
                # --- PERBAIKAN UTAMA DI SINI ---
                # Cek apakah tool yang akan dipanggil adalah fungsi async
                if asyncio.iscoroutinefunction(tool_to_call):
                    # Jika ya, gunakan await
                    tool_output = await tool_to_call(**tool_args)
                else:
                    # Jika tidak, panggil seperti biasa
                    tool_output = tool_to_call(**tool_args)
                # -------------------------------

            except Exception as e:
                print(f"  🔥 [ERROR] GAGAL saat memproses tool '{tool_name}': {type(e).__name__}: {e}")
                tool_output = f"Error executing tool '{tool_name}': {type(e).__name__}: {e}"
        
        new_messages_to_add.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": json.dumps(tool_output, default=str)
        })
        
    new_history = state["chat_history"] + new_messages_to_add
    return {"chat_history": new_history}