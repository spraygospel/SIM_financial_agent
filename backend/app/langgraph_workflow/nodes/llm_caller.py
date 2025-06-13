# backend/app/langgraph_workflow/nodes/llm_caller.py
import json
from typing import Dict, Any
from openai import AsyncOpenAI

from backend.app.schemas.agent_state import AgentState
from backend.app.core.config import settings
from .tool_definitions import tools_definition # Mengimpor dari file baru

async def llm_caller_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Calling LLM with {len(state['chat_history'])} messages ---")
    
    client = AsyncOpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_API_BASE_URL)
    messages_to_send = state["chat_history"]

    # Definisikan tool khusus untuk deteksi intent
    intent_detection_tool = {
        "type": "function",
        "function": {
            "name": "categorize_user_intent",
            "description": "Categorizes the user's intent based on their latest message and conversation history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "intent": {
                        "type": "string",
                        "description": "The user's primary intent.",
                        "enum": ["EXECUTE_QUERY", "REQUEST_MODIFICATION", "ACKNOWLEDGE", "UNKNOWN"]
                    },
                    "final_response_for_acknowledge": {
                        "type": "string",
                        "description": "A ready-to-use friendly response if the intent is ACKNOWLEDGE. Example: 'Sama-sama! Senang bisa membantu.'"
                    }
                },
                "required": ["intent"]
            }
        }
    }

    # Gabungkan dengan tools yang sudah ada
    all_tools = tools_definition + [intent_detection_tool]
    
    # Paksa LLM untuk selalu memanggil tool deteksi intent
    response = await client.chat.completions.create(
        model=settings.LLM_MODEL_NAME,
        messages=messages_to_send,
        tools=all_tools,
        tool_choice={"type": "function", "function": {"name": "categorize_user_intent"}}
    )
    
    response_message = response.choices[0].message
    
    # Inisialisasi output state
    output_state = {"tool_calls": None, "intent": "UNKNOWN"}
    
    # Proses tool call untuk intent
    if response_message.tool_calls:
        intent_tool_call = response_message.tool_calls[0]
        if intent_tool_call.function.name == "categorize_user_intent":
            try:
                args = json.loads(intent_tool_call.function.arguments)
                detected_intent = args.get("intent", "UNKNOWN")
                output_state["intent"] = detected_intent
                
                # Jika intentnya ACKNOWLEDGE, langsung siapkan respons akhir
                if detected_intent == "ACKNOWLEDGE":
                    ack_response = args.get("final_response_for_acknowledge", "Baik, sama-sama.")
                    # Buat pesan "pura-pura" dari asisten agar alur bisa selesai
                    assistant_response = {"role": "assistant", "content": ack_response}
                    output_state["chat_history"] = messages_to_send + [assistant_response]
                    return output_state # Langsung keluar, tidak perlu panggil LLM lagi

            except json.JSONDecodeError:
                print("[!] ERROR: Gagal mem-parsing argumen intent.")
                output_state["intent"] = "UNKNOWN"

    # Jika intent BUKAN ACKNOWLEDGE, panggil LLM lagi untuk tool calling biasa
    response_for_tools = await client.chat.completions.create(
        model=settings.LLM_MODEL_NAME,
        messages=messages_to_send,
        tools=tools_definition, # Hanya tools asli, tanpa intent detector
        tool_choice="auto"
    )

    tool_response_message = response_for_tools.choices[0].message
    response_dict = tool_response_message.model_dump(exclude_none=True)
    
    output_state["chat_history"] = messages_to_send + [response_dict]
    
    if tool_response_message.tool_calls:
        output_state["tool_calls"] = tool_response_message.tool_calls
        
    return output_state