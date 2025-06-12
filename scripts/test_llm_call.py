# scripts/test_llm_call.py (Tanpa LangChain)

import asyncio
import sys
import json
from pathlib import Path
from typing import Literal

# --- Setup Path ---
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# --- Impor yang Diperlukan ---
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError
from backend.app.core.config import settings

# 1. Definisikan Pydantic Model (TETAP SAMA)
class RouteQuery(BaseModel):
    intent: Literal["execute_query", "request_modification", "acknowledge", "ambiguous"]

async def run_direct_llm_test():
    """Menjalankan tes panggilan LLM langsung menggunakan openai SDK."""
    print("--- Memulai Tes Panggilan LLM Langsung (Tanpa LangChain) ---")

    # 2. Inisialisasi Klien OpenAI yang sudah dikonfigurasi untuk DeepSeek
    try:
        client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE_URL,
        )
        print("✅ Klien OpenAI (untuk DeepSeek) berhasil diinisialisasi.")
    except Exception as e:
        print(f"🔥 GAGAL menginisialisasi Klien: {e}")
        return

    # 3. Definisikan Prompt dengan Jelas
    # Kita akan menggabungkan system dan human prompt menjadi satu pesan sistem
    system_prompt = """You are a highly intelligent query intent classifier. Your ONLY task is to analyze the user's request and respond with a single, valid JSON object.

CRITICAL INSTRUCTIONS:
1.  Your entire response MUST be a single, raw JSON object. Do not wrap it in ```json ... ``` or add any other text.
2.  The JSON object MUST have a single key: "intent".
3.  The value for "intent" MUST be one of these exact strings: "execute_query", "request_modification", "acknowledge", "ambiguous".

Analyze the user's request below and provide the JSON output.
---
User Request: "tampilkan daftar customer yang masih punya hutang"
"""
    print("✅ Prompt telah dibuat.")
    
    # 4. Panggil API secara langsung
    print("\n🔄 Memanggil client.chat.completions.create...")
    try:
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that only speaks JSON."}, # Pancingan untuk mode JSON
                {"role": "user", "content": system_prompt},
            ],
            response_format={"type": "json_object"}, # Meminta mode JSON secara eksplisit
            temperature=0,
        )
        
        raw_response_content = response.choices[0].message.content
        print(f"✅ Respons mentah dari LLM diterima:\n{raw_response_content}")

        # 5. Validasi dan Parsing dengan Pydantic
        print("\n🔄 Mem-parsing respons JSON dengan Pydantic...")
        if raw_response_content:
            json_data = json.loads(raw_response_content)
            parsed_result = RouteQuery.model_validate(json_data)
            print("✅ Parsing Pydantic berhasil!")
            print(f"   -> Intent yang terdeteksi: {parsed_result.intent}")
            
            assert parsed_result.intent == "execute_query"
            print("\n🎉 Tes Panggilan Langsung BERHASIL! 🎉")
        else:
            print("🔥 GAGAL: Respons dari LLM kosong.")

    except ValidationError as e:
        print(f"\n🔥 GAGAL Validasi Pydantic: LLM mengembalikan format yang salah.")
        print(e)
    except Exception as e:
        print(f"\n🔥 GAGAL saat memanggil API: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_direct_llm_test())