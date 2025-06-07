# backend/app/langgraph_workflow/nodes/plan_execution.py
from typing import Dict, Any, List, Optional, Union 
import sys
import json
from openai import OpenAI

from backend.app.langgraph_workflow.nodes.planning_prompts.customer_report_plan_prompt import get_customer_report_prompt_parts
from backend.app.langgraph_workflow.nodes.planning_prompts.default_plan_prompt import get_default_prompt_parts

from backend.app.schemas.agent_state import AgentState, TimePeriod, TableSchemaFromMCP, RelationshipFromMCP, DatabaseOperation 
from backend.app.core.config import settings

llm_client_planner = None
if settings.LLM_API_KEY and settings.LLM_API_BASE_URL:
    try:
        llm_client_planner = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE_URL
        )
        print(f"LLM Client initialized for plan_execution_node. Base URL: {settings.LLM_API_BASE_URL}, Model: {settings.LLM_MODEL_NAME}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: Gagal menginisialisasi LLM Client untuk planner: {e}", file=sys.stderr)
        llm_client_planner = None
else:
    print("WARNING: LLM_API_KEY atau LLM_API_BASE_URL tidak diset. LLM Planner tidak akan berfungsi optimal.", file=sys.stderr)

def get_planning_prompt_template(
    intent: str,
    entities_mentioned: List[str],
    time_period: Optional[TimePeriod], 
    requested_metrics: List[str],
    relevant_tables_from_state: List[TableSchemaFromMCP], 
    table_relationships_from_state: List[RelationshipFromMCP], 
    user_query_for_context: str
) -> str:

    schema_description = "\nSkema Database yang Relevan dan BOLEH DIGUNAKAN:\n"
    # ... (logika schema_description tetap sama seperti sebelumnya) ...
    if not relevant_tables_from_state:
        schema_description += ("Tidak ada tabel relevan yang ditemukan dari konsultasi skema. "
                               "Anda TIDAK BISA membuat rencana operasi database. "
                               "Hasilkan 'database_operations_plan' sebagai list kosong `[]` dan 'response_template' "
                               "yang menjelaskan bahwa data tidak dapat diambil karena skema tidak ditemukan.\n")
    else:
        for table_data in relevant_tables_from_state: 
            schema_description += f"Tabel: {table_data.get('table_name', 'N/A')}\n"
            schema_description += f"  Tujuan: {table_data.get('purpose', 'N/A')}\n"
            schema_description += f"  Kategori Bisnis: {table_data.get('business_category', 'N/A')}\n" 
            schema_description += f"  Kolom:\n"
            for col_dict in table_data.get('columns', []):
                col_desc = f"    - {col_dict.get('name', 'N/A')} (Tipe DB: {col_dict.get('type_from_db', col_dict.get('type', 'N/A'))}"
                if col_dict.get('classification'):
                    col_desc += f", Klasifikasi Semantik: {col_dict.get('classification')}"
                if col_dict.get('is_aggregatable') is not None: 
                    col_desc += f", Bisa Agregasi: {'Ya' if col_dict.get('is_aggregatable') else 'Tidak'}"
                col_desc += ")\n"
                schema_description += col_desc
        schema_description += "\nRelasi Antar Tabel (Foreign Keys) yang BOLEH DIGUNAKAN:\n"
        if table_relationships_from_state:
            for rel_data in table_relationships_from_state: 
                schema_description += (f"- Dari tabel '{rel_data.get('from_table')}' kolom '{rel_data.get('from_column')}' "
                                       f"mereferensi tabel '{rel_data.get('to_table')}' kolom '{rel_data.get('to_column')}' "
                                       f"(Tipe Relasi: {rel_data.get('relationship_type', 'FOREIGN_KEY')}).\n")
        else:
            schema_description += "- Tidak ada relasi antar tabel yang teridentifikasi dalam konteks ini (atau tidak relevan untuk tabel yang dipilih).\n"

    # --- Logika untuk memilih dan memuat template prompt spesifik-intent ---
    time_period_display_str_for_prompt = "Tidak ada periode waktu spesifik."
    if time_period and isinstance(time_period, dict):
        label = time_period.get("period_label")
        start_date_str = time_period.get("start_date", "N/A")
        end_date_str = time_period.get("end_date", "N/A")
        if label and isinstance(label, str):
            time_period_display_str_for_prompt = f"{label}"
            if start_date_str != "N/A":
                 time_period_display_str_for_prompt += f" (dari {start_date_str}"
                 if end_date_str != "N/A":
                     time_period_display_str_for_prompt += f" hingga {end_date_str}"
                 time_period_display_str_for_prompt += ")"
        elif start_date_str != "N/A" or end_date_str != "N/A":
            time_period_display_str_for_prompt = f"Dari {start_date_str} hingga {end_date_str}"

    intent_specific_parts = {"intent_specific_json_example": "{}", "intent_specific_rules": "Tidak ada aturan spesifik intent."}

    if intent == "customer_report": 
        intent_specific_parts = get_customer_report_prompt_parts(intent, time_period_display_str_for_prompt)
    else:
        print(f"Intent '{intent}' tidak memiliki template prompt spesifik, menggunakan default.", file=sys.stderr)
        intent_specific_parts = get_default_prompt_parts(intent, time_period_display_str_for_prompt)

    json_output_structure_example = intent_specific_parts["intent_specific_json_example"]
    intent_specific_rules_text = intent_specific_parts["intent_specific_rules"]
    # --- Akhir logika pemilih template ---

    prompt = f"""
Anda adalah AI ahli database MySQL yang bertugas merencanakan operasi database dan template respons.
BERDASARKAN PERMINTAAN PENGGUNA DAN SKEMA YANG DISEDIAKAN, buat rencana dalam format JSON.
JANGAN menghasilkan query SQL secara langsung. Sebaliknya, definisikan operasi dan parameternya.

Permintaan Pengguna (Hasil NLU):
- Intent: {intent}
- Entitas yang Disebutkan Awal oleh NLU: {', '.join(entities_mentioned) if entities_mentioned else 'Tidak ada'}
- Periode Waktu: {time_period_display_str_for_prompt}
- Metrik yang Diminta: {', '.join(requested_metrics) if requested_metrics else 'Data umum'}

{schema_description}

{intent_specific_rules_text}

Tugas Anda adalah menghasilkan output JSON dengan struktur persis seperti contoh di bawah ini.
Isi "field_name" di "select_columns" dengan nama tabel dan kolom (misal, "nama_tabel.nama_kolom").
Untuk "joins", "on_conditions" juga harus menggunakan format "nama_tabel_kiri.nama_kolom_kiri" dan "nama_tabel_kanan.nama_kolom_kanan".
Pastikan "result_key" unik untuk setiap operasi di "database_operations_plan".
"raw_data_operation_plan" harus selalu ada jika ada tabel yang relevan, dengan "limit: 50".
Untuk "filters" dan "having_conditions", gunakan struktur `LogicalFilterGroup` yang memiliki `logical_operator` ("AND" atau "OR") dan list `conditions`. Setiap `condition` bisa berupa `FilterCondition` lain atau `LogicalFilterGroup` lagi untuk nesting.

Format JSON Output yang Diharapkan dan Contoh Struktur (INI ADALAH CONTOH STRUKTUR UMUM, LIHAT ATURAN SPESIFIK INTENT DI ATAS UNTUK CONTOH YANG LEBIH DETAIL):
{json_output_structure_example}

Aturan Penting Umum untuk Output JSON (DatabaseOperation):
1.  **`operation_type`**: Pilih dari 'fetch_records', 'aggregate_data', 'count_distinct_value'.
2.  **`select_columns`**: `field_name` harus "nama_tabel.nama_kolom" atau ekspresi AMAN.
3.  **`joins`**: Tentukan `target_table`, `type`, dan `on_conditions`.
4.  **`filters` & `having_conditions`**: Gunakan `LogicalFilterGroup`.
5.  **`group_by_columns`**: Jika ada agregasi, semua kolom non-agregasi di `select_columns` harus ada di sini.
6.  **`result_key`**: UPPERCASE_SNAKE_CASE dan unik.
7.  **`expected_result_format`**: 'single_value', 'list_of_dicts', atau 'raw_table_data'.
8.  **Skema**: HANYA gunakan tabel dan kolom dari skema yang diberikan. Jika tidak bisa, `database_operations_plan: []`.
9.  **Tanggal**: Nilai tanggal di filter harus 'YYYY-MM-DD'. `time_period_object_from_nlu` adalah: `{time_period if time_period else "Tidak ada periode spesifik"}`.

Sekarang, buat rencana JSON berdasarkan Permintaan Pengguna dan Skema Database yang Relevan di atas, dengan MENGUTAMAKAN ATURAN SPESIFIK INTENT jika ada.
User Query (untuk konteks Anda, jangan diulang di JSON): "{user_query_for_context}"
Hasilkan HANYA output JSON yang valid.
"""
    return prompt

# Fungsi parse_llm_plan_response tetap sama seperti yang sudah kita buat sebelumnya
def parse_llm_plan_response(response_content: str) -> Dict[str, Any]:
    try:
        print(f"Attempting to parse LLM plan response:\n{response_content[:1000]}...", file=sys.stderr)
        if response_content.strip().startswith("```json"):
            response_content = response_content.strip()[7:-3].strip()
        elif response_content.strip().startswith("```"):
            response_content = response_content.strip()[3:-3].strip()

        parsed_json = json.loads(response_content)

        if "database_operations_plan" not in parsed_json or not isinstance(parsed_json["database_operations_plan"], list):
            print("WARNING: 'database_operations_plan' tidak ada atau bukan list. Menggunakan list kosong.", file=sys.stderr)
            parsed_json["database_operations_plan"] = []
        else:
            valid_ops = []
            for i, op_plan_dict in enumerate(parsed_json["database_operations_plan"]):
                if isinstance(op_plan_dict, dict):
                    if not all(k in op_plan_dict for k in ["operation_id", "operation_type", "purpose", "main_table", "select_columns", "result_key"]):
                        print(f"WARNING: Item ke-{i} di 'database_operations_plan' tidak memiliki field wajib. Dilewati: {op_plan_dict}", file=sys.stderr)
                        continue
                    if not isinstance(op_plan_dict["select_columns"], list) or not op_plan_dict["select_columns"]:
                         print(f"WARNING: Item ke-{i} 'select_columns' bukan list atau kosong. Dilewati: {op_plan_dict}", file=sys.stderr)
                         continue
                    valid_ops.append(op_plan_dict)
                else:
                    print(f"WARNING: Item ke-{i} di 'database_operations_plan' bukan dict. Dilewati.", file=sys.stderr)
            parsed_json["database_operations_plan"] = valid_ops

        rdop = parsed_json.get("raw_data_operation_plan")
        if rdop:
            if not (isinstance(rdop, dict) and
                    all(k in rdop for k in ["operation_id", "operation_type", "purpose", "main_table", "select_columns", "result_key", "limit"]) and
                    isinstance(rdop["select_columns"], list) and rdop["select_columns"] and
                    rdop["result_key"] == "RAW_DATA_TABLE"):
                print(f"WARNING: 'raw_data_operation_plan' tidak valid. Dibuat default None: {rdop}", file=sys.stderr)
                parsed_json["raw_data_operation_plan"] = None
        else: 
            parsed_json["raw_data_operation_plan"] = None
            if parsed_json.get("database_operations_plan"): 
                 print("INFO: 'raw_data_operation_plan' tidak ada dari LLM, padahal ada 'database_operations_plan'.", file=sys.stderr)

        if "response_template" not in parsed_json or not isinstance(parsed_json["response_template"], str):
            parsed_json["response_template"] = "Maaf, saya tidak dapat menghasilkan narasi saat ini."
        
        if "placeholder_mapping" not in parsed_json or not isinstance(parsed_json["placeholder_mapping"], dict):
            parsed_json["placeholder_mapping"] = {}

        if "data_source_info" not in parsed_json or not isinstance(parsed_json["data_source_info"], dict):
            parsed_json["data_source_info"] = {"description": "Informasi sumber data tidak dapat dihasilkan."}
            
        print("LLM plan response parsed successfully.", file=sys.stderr)
        return parsed_json

    except json.JSONDecodeError as e:
        print(f"ERROR: Gagal mem-parse respons JSON dari LLM untuk PLAN: {e}", file=sys.stderr)
        print(f"Raw LLM plan response content:\n{response_content}", file=sys.stderr)
        return {
            "database_operations_plan": [],
            "raw_data_operation_plan": None,
            "response_template": "Maaf, terjadi kesalahan saat merencanakan respons (format JSON tidak valid).",
            "placeholder_mapping": {},
            "data_source_info": {"description": "Gagal mem-parse rencana dari LLM."},
            "error_message": f"Gagal mem-parse rencana LLM: {str(e)}"
        }
    except Exception as e_gen:
        print(f"ERROR: Kesalahan tidak terduga saat parsing PLAN LLM response: {e_gen}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {
            "database_operations_plan": [],
            "raw_data_operation_plan": None,
            "response_template": "Maaf, terjadi kesalahan internal saat merencanakan respons.",
            "placeholder_mapping": {},
            "data_source_info": {"description": f"Kesalahan pemrosesan rencana: {str(e_gen)}"},
            "error_message": f"Kesalahan pemrosesan rencana: {str(e_gen)}"
        }

# Fungsi plan_execution_node tetap sama, karena logika pemanggilan dan parsingnya
# akan menggunakan prompt yang sudah dimodifikasi oleh get_planning_prompt_template
def plan_execution_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: plan_execution_node (Refactored for DatabaseOperationPlan with Intent-Specific Prompts) ---", file=sys.stderr)
    
    intent = state.get("intent")
    entities_nlu = state.get("entities_mentioned", []) 
    time_period: Optional[TimePeriod] = state.get("time_period") 
    requested_metrics = state.get("requested_metrics", [])
    
    relevant_tables_from_state: List[TableSchemaFromMCP] = state.get("relevant_tables", [])
    table_relationships_from_state: List[RelationshipFromMCP] = state.get("table_relationships", [])

    schema_consult_warnings = state.get("schema_consultation_warnings", [])

    if not intent:
        warning_msg = "Intent tidak jelas, tidak dapat membuat rencana eksekusi."
        print(f"WARNING in plan_execution_node: {warning_msg}", file=sys.stderr)
        return {
            "database_operations_plan": [], 
            "raw_data_operation_plan": None, 
            "response_template": "Maaf, maksud permintaan Anda tidak cukup jelas untuk saya proses.",
            "placeholder_mapping": {},
            "data_source_info": {"description": warning_msg},
            "current_node_name": "plan_execution",
            "error_message_for_user": warning_msg
        }

    if not relevant_tables_from_state and schema_consult_warnings:
        combined_warnings = " ".join(schema_consult_warnings)
        print(f"WARNING in plan_execution_node due to schema issues: {combined_warnings}", file=sys.stderr)
        return {
            "database_operations_plan": [],
            "raw_data_operation_plan": None,
            "response_template": f"Maaf, saya tidak dapat membuat rencana query: {combined_warnings}",
            "placeholder_mapping": {},
            "data_source_info": {"description": combined_warnings},
            "current_node_name": "plan_execution",
            "error_message_for_user": combined_warnings
        }
    
    if not llm_client_planner:
        print("ERROR: LLM Planner Client not initialized. Tidak dapat membuat rencana eksekusi.", file=sys.stderr)
        return {
            "database_operations_plan": [],
            "raw_data_operation_plan": None,
            "response_template": "Maaf, layanan perencanaan AI sedang tidak tersedia.",
            "placeholder_mapping": {}, 
            "data_source_info": {"description": "LLM Planner tidak aktif."},
            "current_node_name": "plan_execution",
            "error_message_for_user": "Layanan AI untuk perencanaan query sedang bermasalah."
        }
        
    # Memanggil get_planning_prompt_template yang sudah dimodifikasi untuk memilih template intent
    prompt_for_llm_planner = get_planning_prompt_template(
        intent=intent, # type: ignore
        entities_mentioned=entities_nlu if entities_nlu is not None else [],
        time_period=time_period, 
        requested_metrics=requested_metrics if requested_metrics is not None else [], 
        relevant_tables_from_state=relevant_tables_from_state if relevant_tables_from_state is not None else [], 
        table_relationships_from_state=table_relationships_from_state if table_relationships_from_state is not None else [],
        user_query_for_context=state.get("user_query", "")
    )

    print(f"Sending to LLM for Planning (DatabaseOperationPlan - Intent: {intent}). Model: {settings.LLM_MODEL_NAME}", file=sys.stderr)

    try:
        response = llm_client_planner.chat.completions.create(
            model=settings.LLM_MODEL_NAME, # type: ignore
            messages=[
                {"role": "user", "content": prompt_for_llm_planner}
            ],
            temperature=0.1, 
            max_tokens=3000, 
        )
        
        llm_response_content = response.choices[0].message.content
        if not llm_response_content:
            raise ValueError("LLM response content is empty.")

        print(f"LLM Planner Raw Response Content (Intent: {intent}):\n{llm_response_content}", file=sys.stderr)

        parsed_plan_result = parse_llm_plan_response(llm_response_content)
        
        update_dict: Dict[str, Any] = {
            "database_operations_plan": parsed_plan_result.get("database_operations_plan", []),
            "raw_data_operation_plan": parsed_plan_result.get("raw_data_operation_plan"),
            "response_template": parsed_plan_result.get("response_template", "Template error."),
            "placeholder_mapping": parsed_plan_result.get("placeholder_mapping", {}),
            "data_source_info": parsed_plan_result.get("data_source_info", {}),
            "current_node_name": "plan_execution"
        }
        
        if "error_message" in parsed_plan_result:
             update_dict["error_message_for_user"] = parsed_plan_result["error_message"]
             update_dict["technical_error_details"] = f"LLM Plan Parsing: {parsed_plan_result['error_message']}"

        print(f"Plan Execution Node Output (Intent: {intent}): {update_dict}", file=sys.stderr)
        return update_dict

    except Exception as e:
        print(f"ERROR: Gagal saat memanggil LLM API atau memproses respons PLANNER (Intent: {intent}): {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        user_err_msg = f"Terjadi kesalahan pada layanan AI saat merencanakan query."
        # if hasattr(e, 'message'): # Error ini mungkin tidak selalu punya attribute 'message'
        #     if isinstance(e.message, str) and "context_length_exceeded" in e.message.lower():
        #         user_err_msg = "Permintaan Anda terlalu kompleks atau membutuhkan terlalu banyak informasi skema untuk diproses sekaligus. Coba sederhanakan."
        
        return {
            "database_operations_plan": [],
            "raw_data_operation_plan": None,
            "response_template": "Maaf, terjadi kesalahan internal saat merencanakan pengambilan data.",
            "placeholder_mapping": {},
            "data_source_info": {"description": f"Kesalahan API LLM Planner: {str(e)}"},
            "current_node_name": "plan_execution",
            "error_message_for_user": user_err_msg,
            "technical_error_details": f"LLM API Call Failed: {str(e)}"
        }