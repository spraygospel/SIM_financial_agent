# backend/app/langgraph_workflow/nodes/llm_caller.py
import json
from typing import Dict, Any
from openai import AsyncOpenAI

from backend.app.schemas.agent_state import AgentState
from backend.app.core.config import settings
from .tool_definitions import tools_definition

async def llm_caller_node(state: AgentState) -> Dict[str, Any]:
    """
    Satu fungsi untuk semua interaksi dengan LLM.
    Tugasnya adalah melanjutkan percakapan berdasarkan state saat ini.
    """
    print(f"--- Calling LLM with {len(state['chat_history'])} messages ---")
    
    client = AsyncOpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_API_BASE_URL)
    
    # Deteksi intent HANYA jika ini adalah pesan pertama dari pengguna dalam siklus ini
    last_message = state['chat_history'][-1]
    is_user_message = last_message.get("role") == "user"

    if is_user_message:
        # Panggilan pertama untuk deteksi intent
        intent_detection_tool = {
            "type": "function",
            "function": {
                "name": "categorize_user_intent",
                "description": "Categorizes the user's intent based on their latest message.",
                "parameters": {
                    "type": "object",
                    "properties": { "intent": { "type": "string", "enum": ["EXECUTE_QUERY", "ACKNOWLEDGE", "UNKNOWN"] } },
                    "required": ["intent"]
                }
            }
        }
        try:
            intent_response = await client.chat.completions.create(
                model=settings.LLM_MODEL_NAME,
                messages=state['chat_history'],
                tools=[intent_detection_tool],
                tool_choice={"type": "function", "function": {"name": "categorize_user_intent"}}
            )
            intent_tool_call = intent_response.choices[0].message.tool_calls[0]
            args = json.loads(intent_tool_call.function.arguments)
            detected_intent = args.get("intent", "UNKNOWN")
            
            if detected_intent == "ACKNOWLEDGE":
                # Jika basa-basi, langsung buat respons akhir dan selesai
                ack_response_content = "Sama-sama! Ada lagi yang bisa saya bantu?"
                return {
                    "chat_history": state['chat_history'] + [{"role": "assistant", "content": ack_response_content}],
                    "intent": "ACKNOWLEDGE"
                }
        except Exception as e:
            print(f"[!] Gagal mendeteksi intent, melanjutkan dengan alur standar. Error: {e}")
            detected_intent = "EXECUTE_QUERY" # Fallback
    else:
        # Jika pesan terakhir bukan dari user (misal, dari tool), berarti kita sedang dalam proses.
        detected_intent = "EXECUTE_QUERY"

    # Lanjutkan dengan panggilan LLM normal untuk merespons atau memanggil tool
    response = await client.chat.completions.create(
        model=settings.LLM_MODEL_NAME,
        messages=state['chat_history'],
        tools=tools_definition,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    response_dict = response_message.model_dump(exclude_none=True)
    
    new_history = state["chat_history"] + [response_dict]
    
    output_state = {"chat_history": new_history, "intent": detected_intent}
    
    if response_message.tool_calls:
        output_state["tool_calls"] = response_message.tool_calls
    else:
        output_state["tool_calls"] = None
        
    return output_state