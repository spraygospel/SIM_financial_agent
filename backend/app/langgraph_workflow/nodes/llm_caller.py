# backend/app/langgraph_workflow/nodes/llm_caller.py
from typing import Dict, Any
from openai import AsyncOpenAI

from backend.app.schemas.agent_state import AgentState
from backend.app.core.config import settings
from .tool_definitions import tools_definition # Mengimpor dari file baru

async def llm_caller_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Calling LLM with {len(state['chat_history'])} messages ---")
    debug_key = settings.LLM_API_KEY
    if debug_key:
        print(f"[*] DEBUG: API Key yang akan digunakan: '{debug_key[:4]}...{debug_key[-4:]}'")
    else:
        print("[!] DEBUG: API Key KOSONG!")
    client = AsyncOpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_API_BASE_URL)

    # Pastikan history yang dikirim adalah list of dicts yang valid
    messages_to_send = state["chat_history"]

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL_NAME,
        messages=messages_to_send,
        tools=tools_definition,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    response_dict = response_message.model_dump(exclude_none=True)
    
    # Tambahkan respons dari LLM ke dalam history
    new_history = messages_to_send + [response_dict]
    
    # Siapkan output untuk state berikutnya
    output_state = {"chat_history": new_history}
    
    if response_message.tool_calls:
        output_state["tool_calls"] = response_message.tool_calls
    else:
        # Jika tidak ada tool_calls, ini adalah respons final untuk pengguna.
        # Kita tidak lagi butuh 'final_response', karena service akan mencarinya di history.
        output_state["tool_calls"] = None
        
    return output_state