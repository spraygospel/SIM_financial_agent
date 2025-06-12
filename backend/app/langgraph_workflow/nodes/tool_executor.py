# backend/app/langgraph_workflow/nodes/tool_executor.py
import json
import asyncio
from typing import Dict, Any, List

from backend.app.schemas.agent_state import AgentState
from backend.app.tools import database_tools, graphiti_tools

available_tools = {
    "execute_database_plan": database_tools.execute_database_plan,
    "get_relevant_schema": graphiti_tools.get_relevant_schema,
}

async def tool_executor_node(state: AgentState) -> Dict[str, Any]:
    print("--- Executing Tools ---")
    
    last_message = state["chat_history"][-1]
    tool_calls = last_message.get("tool_calls", [])
    
    new_messages_to_add = []

    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        tool_args_str = tool_call["function"]["arguments"]
        tool_call_id = tool_call["id"]
        
        print(f"  -> Preparing to call tool: {tool_name}")
        
        # --- LOGGING DITAMBAHKAN DI SINI ---
        print(f"  -> [DEBUG] Argumen mentah dari LLM (string):")
        print(tool_args_str)
        # ------------------------------------

        tool_to_call = available_tools.get(tool_name)
        
        if not tool_to_call:
            tool_output = f"Error: Tool '{tool_name}' is not a valid tool."
        else:
            try:
                # Ini adalah titik rawan error
                tool_args = json.loads(tool_args_str)
                
                # --- LOGGING DITAMBAHKAN DI SINI ---
                print("  -> [DEBUG] Argumen setelah json.loads() berhasil:")
                print(tool_args)
                # ------------------------------------

                if asyncio.iscoroutinefunction(tool_to_call):
                    tool_output = await tool_to_call(**tool_args)
                else:
                    tool_output = tool_to_call(**tool_args)

            except Exception as e:
                # --- LOGGING DITAMBAHKAN DI SINI ---
                print(f"  🔥 [ERROR] GAGAL saat memproses tool '{tool_name}': {type(e).__name__}: {e}")
                # ------------------------------------
                tool_output = f"Error executing tool '{tool_name}': {type(e).__name__}: {e}"
        
        new_messages_to_add.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": tool_name,
            "content": json.dumps(tool_output, default=str) # default=str untuk handle objek datetime, dll
        })
        
    new_history = state["chat_history"] + new_messages_to_add

    return {"chat_history": new_history}