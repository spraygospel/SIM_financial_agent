# backend/app/langgraph_workflow/nodes/understand_query.py
from typing import Dict, Any, List, Optional
import sys
import json # Untuk parsing output JSON dari LLM
from openai import OpenAI # Menggunakan library OpenAI untuk API yang kompatibel

from backend.app.schemas.agent_state import AgentState, TimePeriod 
from backend.app.core.config import settings # Untuk mengambil konfigurasi LLM

# Inisialisasi OpenAI client (atau client lain yang kompatibel)
# Ini akan menggunakan variabel lingkungan OPENAI_API_KEY dan OPENAI_BASE_URL jika diset,
# atau kita bisa pass secara eksplisit.
# Sesuai config.py, kita akan menggunakan settings.LLM_API_KEY dan settings.LLM_API_BASE_URL

# Periksa apakah konfigurasi LLM ada
if not settings.LLM_API_KEY or not settings.LLM_API_BASE_URL or not settings.LLM_MODEL_NAME:
    print("ERROR: Konfigurasi LLM (API Key, Base URL, Model Name) tidak lengkap. Node understand_query tidak dapat berfungsi penuh.", file=sys.stderr)
    # Kita bisa raise error di sini atau biarkan client dibuat dan gagal saat API call.
    # Untuk development, mungkin lebih baik biarkan dibuat agar bisa di-mock.
    # Namun, untuk fungsi nyata, ini adalah error.
    # Untuk sekarang, kita akan membiarkannya dan berharap ada mock atau config diisi saat runtime.
    
llm_client = None
if settings.LLM_API_KEY and settings.LLM_API_BASE_URL:
    try:
        llm_client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE_URL
        )
        print(f"LLM Client initialized for understand_query_node. Base URL: {settings.LLM_API_BASE_URL}, Model: {settings.LLM_MODEL_NAME}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Gagal menginisialisasi LLM Client: {e}", file=sys.stderr)
        llm_client = None # Pastikan client adalah None jika gagal
else:
    print("WARNING: LLM_API_KEY atau LLM_API_BASE_URL tidak diset. LLM NLU tidak akan berfungsi.", file=sys.stderr)


def parse_llm_nlu_response(response_content: str) -> Dict[str, Any]:
    """
    Mencoba mem-parse string respons dari LLM yang diharapkan berupa JSON.
    """
    try:
        # Coba bersihkan jika ada ```json ... ``` markdown
        if response_content.strip().startswith("```json"):
            response_content = response_content.strip()[7:-3].strip()
        elif response_content.strip().startswith("```"): # Hanya ``` di awal dan akhir
             response_content = response_content.strip()[3:-3].strip()

        parsed_json = json.loads(response_content)
        # Validasi dasar struktur JSON yang diharapkan
        required_keys = ["intent", "entities_mentioned", "time_period", "requested_metrics", "query_complexity"]
        for key in required_keys:
            if key not in parsed_json:
                # Isi dengan default jika key tidak ada, tapi log warning
                print(f"WARNING: Key '{key}' tidak ada dalam respons LLM NLU. Menggunakan default.", file=sys.stderr)
                if key == "entities_mentioned" or key == "requested_metrics":
                    parsed_json[key] = []
                elif key == "time_period":
                    parsed_json[key] = {"start_date": None, "end_date": None, "period_label": None}
                elif key == "intent":
                    parsed_json[key] = "unknown_intent"
                elif key == "query_complexity":
                    parsed_json[key] = "simple"
        
        # Pastikan time_period memiliki struktur yang benar jika ada
        if "time_period" in parsed_json and isinstance(parsed_json["time_period"], dict):
            tp = parsed_json["time_period"]
            tp_keys = ["start_date", "end_date", "period_label"]
            for tp_key in tp_keys:
                if tp_key not in tp:
                    tp[tp_key] = None # Default ke None jika sub-key tidak ada
        elif "time_period" not in parsed_json : # Jika time_period sama sekali tidak ada
             parsed_json["time_period"] = {"start_date": None, "end_date": None, "period_label": None}


        return parsed_json
    except json.JSONDecodeError as e:
        print(f"ERROR: Gagal mem-parse respons JSON dari LLM untuk NLU: {e}", file=sys.stderr)
        print(f"Raw LLM response content: {response_content}", file=sys.stderr)
        # Kembalikan struktur default jika parsing gagal total
        return {
            "intent": "nlu_parse_error",
            "entities_mentioned": [],
            "time_period": {"start_date": None, "end_date": None, "period_label": None},
            "requested_metrics": [],
            "query_complexity": "unknown",
            "error_message": f"Gagal mem-parse respons LLM: {str(e)}"
        }
    except Exception as e_gen: # Tangkap error umum lainnya
        print(f"ERROR: Kesalahan tidak terduga saat parsing NLU LLM response: {e_gen}", file=sys.stderr)
        print(f"Raw LLM response content: {response_content}", file=sys.stderr)
        return {
            "intent": "nlu_processing_error",
            "entities_mentioned": [],
            "time_period": {"start_date": None, "end_date": None, "period_label": None},
            "requested_metrics": [],
            "query_complexity": "unknown",
            "error_message": f"Kesalahan pemrosesan NLU: {str(e_gen)}"
        }

def get_nlu_prompt_template() -> str:
    # Definisikan template prompt untuk NLU di sini.
    # Ini bisa lebih kompleks, termasuk contoh few-shot jika diperlukan.
    # Untuk sekarang, kita buat template dasar.
    # TODO: Anda mungkin ingin memindahkan ini ke file/modul terpisah jika menjadi sangat besar.
    # Untuk sekarang, kita akan merujuk tanggal hari ini sebagai "TODAY_DATE" jika diperlukan dalam prompt.
    # Format tanggal adalah YYYY-MM-DD.
    from datetime import date
    today_str = date.today().isoformat()

    return f"""
Anda adalah asisten AI yang ahli dalam memahami pertanyaan pengguna terkait analisis data bisnis dan mengubahnya menjadi struktur JSON yang terdefinisi.
Tugas Anda adalah menganalisis pertanyaan pengguna berikut dan mengekstrak informasi ke dalam format JSON.
Tanggal hari ini adalah: {today_str}. Jika pengguna menyebutkan periode relatif seperti "bulan ini", "bulan lalu", "kemarin", "hari ini", "tahun ini", "kuartal ini", "kuartal lalu", hitung tanggal absolutnya berdasarkan tanggal hari ini.

Format JSON Output yang Diharapkan:
{{
  "intent": "string (contoh: 'sales_analysis', 'customer_report', 'inventory_status', 'employee_performance', 'unknown_intent')",
  "entities_mentioned": ["string (daftar nama tabel atau kolom yang disebutkan atau relevan, contoh: 'sales_orders', 'customers', 'order_date', 'total_amount')"],
  "time_period": {{
    "start_date": "string (YYYY-MM-DD, atau null jika tidak spesifik)",
    "end_date": "string (YYYY-MM-DD, atau null jika tidak spesifik)",
    "period_label": "string (deskripsi periode, contoh: 'Januari 2023', 'Minggu Lalu', 'Q1 2024', atau null)"
  }},
  "requested_metrics": ["string (daftar metrik yang diminta, contoh: 'total_sales', 'average_order_value', 'customer_count', 'product_stock_level')"],
  "query_complexity": "string (estimasi kompleksitas: 'simple', 'medium', 'complex', 'unknown')"
}}

Beberapa Aturan Penting:
1.  **Intent**: Tentukan maksud utama pengguna. Jika tidak jelas, gunakan "unknown_intent".
2.  **Entities Mentioned**: Identifikasi entitas utama yang disebutkan pengguna. Cobalah untuk memetakan ini ke nama tabel database yang umum jika relevan (misalnya, jika pengguna bilang 'penjualan', Anda bisa sertakan 'sales_orders' atau 'salesinvoiceh'; jika 'pelanggan', sertakan 'customers' atau 'mastercustomer'). Jika tidak yakin, sertakan saja kata kunci dari pengguna. Jika tidak ada entitas yang jelas, kembalikan list kosong. Contoh entitas: 'sales_orders', 'mastercustomer', 'order_date', 'total_amount'.
3.  **Time Period**: Ekstrak periode waktu.
    *   Jika pengguna menyebutkan periode spesifik (misal "Januari 2023", "15 Maret 2024", "antara 1 Jan dan 15 Jan 2023"), gunakan itu.
    *   Jika periode tidak disebutkan atau tidak jelas, `start_date`, `end_date`, dan `period_label` harus `null`. Jangan berasumsi periode jika tidak diminta.
    *   Jika periode relatif disebutkan (misal "bulan lalu"), hitung tanggal absolutnya. "Bulan ini" berarti dari tanggal 1 bulan ini hingga akhir bulan ini. "Bulan lalu" berarti dari tanggal 1 bulan sebelumnya hingga akhir bulan sebelumnya.
    *   "Kemarin" berarti tanggal kemarin (start_date = end_date = kemarin). "Hari ini" berarti tanggal hari ini.
    *   "Tahun ini" berarti dari 1 Januari tahun ini hingga 31 Desember tahun ini.
    *   "Kuartal ini": Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Okt-Des). Hitung berdasarkan tanggal hari ini.
    *   "Kuartal lalu": Kuartal sebelum kuartal saat ini.
4.  **Requested Metrics**: Identifikasi metrik atau data spesifik yang ingin dilihat pengguna (misal "total penjualan", "jumlah pelanggan", "rata-rata harga"). Jika hanya meminta "data" atau "laporan" umum, list bisa kosong atau berisi item generik seperti "general_data_retrieval".
5.  **Query Complexity**: Berikan estimasi kasar. "simple" untuk lookup dasar, "medium" untuk agregasi dengan filter, "complex" untuk join multi-tabel atau analisis tren.

Contoh Pertanyaan dan Output yang Diharapkan:
Pertanyaan Pengguna: "Berapa total penjualan kita di bulan Januari 2023?"
Output JSON:
{{
  "intent": "sales_analysis",
  "entities_mentioned": ["sales_orders", "total_amount", "order_date"],
  "time_period": {{
    "start_date": "2023-01-01",
    "end_date": "2023-01-31",
    "period_label": "Januari 2023"
  }},
  "requested_metrics": ["total_sales"],
  "query_complexity": "medium"
}}

Pertanyaan Pengguna: "Tampilkan data pelanggan dari Jakarta"
Output JSON:
{{
  "intent": "customer_report",
  "entities_mentioned": ["customers", "city"],
  "time_period": {{
    "start_date": null,
    "end_date": null,
    "period_label": null
  }},
  "requested_metrics": ["customer_data"],
  "query_complexity": "simple"
}}

Pertanyaan Pengguna: "Laporan penjualan produk elektronik bulan lalu"
Output JSON (asumsi hari ini adalah 15 April 2024):
{{
  "intent": "sales_analysis",
  "entities_mentioned": ["sales_orders", "products", "electronics_category", "order_date"],
  "time_period": {{
    "start_date": "2024-03-01",
    "end_date": "2024-03-31",
    "period_label": "Maret 2024"
  }},
  "requested_metrics": ["sales_report"],
  "query_complexity": "medium"
}}

Sekarang, analisis pertanyaan pengguna berikut:
"""

def understand_query_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: understand_query_node (LLM Integrated) ---", file=sys.stderr)
    user_query = state.get("user_query", "")
    
    if not user_query:
        print("WARNING: User query is empty in understand_query_node.", file=sys.stderr)
        return {
            "intent": "empty_query_error",
            "entities_mentioned": [],
            "time_period": {"start_date": None, "end_date": None, "period_label": None},
            "requested_metrics": [],
            "query_complexity": "unknown",
            "current_node_name": "understand_query",
            "error_message_for_user": "Pertanyaan tidak boleh kosong."
        }

    if not llm_client:
        print("ERROR: LLM Client not initialized. Falling back to simple NLU.", file=sys.stderr)
        # Fallback ke NLU sederhana jika LLM client gagal diinisialisasi
        # (Ini adalah NLU placeholder dari versi sebelumnya)
        intent = "fallback_nlu"
        entities_mentioned: List[str] = []
        time_period: TimePeriod = {"start_date": None, "end_date": None, "period_label": None}
        requested_metrics: List[str] = []
        query_complexity = "simple"
        if "penjualan" in user_query.lower() or "sales" in user_query.lower():
            intent = "sales_analysis_fallback"
            entities_mentioned.append("sales_orders")
            if "januari" in user_query.lower():
                time_period = {"start_date": "2023-01-01", "end_date": "2023-01-31", "period_label": "Januari 2023"}
        
        return {
            "intent": intent, "entities_mentioned": entities_mentioned, "time_period": time_period,
            "requested_metrics": requested_metrics, "query_complexity": query_complexity,
            "current_node_name": "understand_query",
            "error_message_for_user": "Menggunakan pemahaman query sederhana karena ada masalah dengan NLU utama."
        }

    # Gabungkan histori percakapan jika ada, untuk konteks LLM
    # Untuk sekarang, kita fokus pada user_query terakhir saja.
    # conversation_history = state.get("conversation_history", [])
    # full_prompt_context = ""
    # for msg in conversation_history:
    #    full_prompt_context += f"{msg['role']}: {msg['content']}\n"
    # full_prompt_context += f"user: {user_query}"
    
    system_prompt_template = get_nlu_prompt_template()
    # Kita hanya akan mengirim user_query terakhir ke LLM untuk NLU saat ini.
    # Untuk multi-turn conversation, prompt perlu disesuaikan.
    
    # Prompt yang akan dikirim ke LLM
    # LLM diharapkan merespons hanya dengan JSON string.
    prompt_for_llm = f"{system_prompt_template}\n\nPertanyaan Pengguna: \"{user_query}\"\nOutput JSON:"

    print(f"Sending to LLM for NLU. Model: {settings.LLM_MODEL_NAME}", file=sys.stderr)
    # print(f"Prompt for LLM:\n{prompt_for_llm}", file=sys.stderr) # Bisa sangat panjang, nonaktifkan jika perlu

    try:
        response = llm_client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                # Tidak menggunakan system role di sini karena prompt utama sudah sangat direktif
                # dan beberapa model mungkin lebih baik dengan satu pesan user yang berisi semua instruksi.
                # Jika model Anda lebih baik dengan system role, sesuaikan.
                # {"role": "system", "content": system_prompt_template},
                {"role": "user", "content": prompt_for_llm}
            ],
            temperature=0.1, # Suhu rendah untuk output yang lebih deterministik (JSON)
            max_tokens=500, # Sesuaikan dengan perkiraan ukuran output JSON
            # response_format={"type": "json_object"} # Jika model mendukung JSON mode, ini sangat membantu!
            # DeepSeek mungkin belum mendukung ini via API OpenAI-compatible. Perlu dicek.
            # Jika tidak, kita perlu parse manual dan berharap LLM patuh.
        )
        
        llm_response_content = response.choices[0].message.content
        print(f"LLM NLU Raw Response Content:\n{llm_response_content}", file=sys.stderr)

        parsed_nlu_result = parse_llm_nlu_response(llm_response_content)
        
        # Tambahkan hasil parsing ke state yang akan di-return untuk update AgentState
        # dan tambahkan current_node_name
        parsed_nlu_result["current_node_name"] = "understand_query"
        
        if "error_message" in parsed_nlu_result: # Jika ada error saat parsing
             parsed_nlu_result["error_message_for_user"] = parsed_nlu_result["error_message"]
             # Kita bisa juga set workflow_status ke error di sini atau biarkan API layer yang handle
        
        print(f"Understand Query Node LLM Output (Parsed): {parsed_nlu_result}", file=sys.stderr)
        return parsed_nlu_result

    except Exception as e:
        print(f"ERROR: Gagal saat memanggil LLM API atau memproses respons NLU: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {
            "intent": "nlu_api_error",
            "entities_mentioned": [],
            "time_period": {"start_date": None, "end_date": None, "period_label": None},
            "requested_metrics": [],
            "query_complexity": "unknown",
            "current_node_name": "understand_query",
            "error_message_for_user": f"Terjadi kesalahan saat mencoba memahami pertanyaan Anda: {str(e)}"
        }