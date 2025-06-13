# backend/app/langgraph_workflow/nodes/tool_executor.py
import json
import asyncio
from typing import Dict, Any, List
from backend.app.schemas.agent_state import AgentState
from backend.app.tools import database_tools, graphiti_tools

# Daftar tool yang tersedia tidak berubah
available_tools = {
    "search_read": database_tools.search_read,
    "get_relevant_schema": graphiti_tools.get_relevant_schema,
}

async def tool_executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Mengeksekusi SEMUA tool yang diminta oleh LLM secara paralel dan
    mengembalikan hasilnya secara individual.
    """
    print("--- Executing Tools ---")
    
    last_message = state["chat_history"][-1]
    tool_calls = last_message.get("tool_calls", [])
    
    tasks = []
    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        tool_args_str = tool_call["function"]["arguments"]
        
        print(f"  -> Preparing to call tool: {tool_name}")
        
        tool_to_call = available_tools.get(tool_name)
        
        if not tool_to_call:
            # Buat coroutine placeholder untuk tool yang tidak valid
            async def invalid_tool_coro():
                return f"Error: Tool '{tool_name}' is not a valid tool."
            tasks.append(invalid_tool_coro())
            continue

        try:
            tool_args = json.loads(tool_args_str)
            
            if asyncio.iscoroutinefunction(tool_to_call):
                tasks.append(tool_to_call(tool_args.get('payload', tool_args)))
            else:
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, tool_to_call, tool_args.get('payload', tool_args)))

        except Exception as e:
            async def error_coro():
                return f"Error processing tool '{tool_name}': {e}"
            tasks.append(error_coro())

    # Jalankan semua task secara paralel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Siapkan pesan untuk ditambahkan ke history
    new_messages_to_add = []
    for i, tool_call in enumerate(tool_calls):
        tool_output = results[i]
        
        # Tangani jika ada exception saat eksekusi task
        if isinstance(tool_output, Exception):
            tool_output_str = f"Error executing tool {tool_call['function']['name']}: {tool_output}"
        else:
            tool_output_str = json.dumps(tool_output, default=str)

        new_messages_to_add.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "name": tool_call["function"]["name"],
            "content": tool_output_str
        })
        
    new_history = state["chat_history"] + new_messages_to_add
    # Reset tool_calls karena sudah dieksekusi
    return {"chat_history": new_history, "tool_calls": None}