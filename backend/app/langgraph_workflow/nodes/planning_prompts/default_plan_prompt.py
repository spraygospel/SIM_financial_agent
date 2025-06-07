# backend/app/langgraph_workflow/nodes/planning_prompts/default_plan_prompt.py
from typing import Optional, List, Dict, Any

def get_default_prompt_parts(
    intent: str,
    time_period_display_str: str,
) -> Dict[str, str]:
    
    # Contoh JSON umum, mungkin lebih sederhana
    default_json_example = f"""
{{
  "database_operations_plan": [
    {{
      "operation_id": "generic_op_1",
      "operation_type": "aggregate_data", // atau fetch_records
      "purpose": "Operasi generik untuk intent: {intent} {time_period_display_str}",
      "main_table": "nama_tabel_utama_dari_skema",
      "select_columns": [
        {{
          "field_name": "nama_tabel.kolom_relevan",
          "aggregation": "SUM", // atau lainnya
          "alias": "hasil_agregasi"
        }}
      ],
      "filters": {{
        "logical_operator": "AND",
        "conditions": [
          // Kondisi filter berdasarkan time_period jika ada kolom tanggal yang cocok
        ]
      }},
      "result_key": "GENERIC_RESULT_KEY",
      "expected_result_format": "single_value" // atau list_of_dicts
    }}
  ],
  "raw_data_operation_plan": {{
      "operation_id": "fetch_raw_data_default",
      "operation_type": "fetch_records",
      "purpose": "mengambil data mentah pendukung untuk intent: {intent}",
      "main_table": "nama_tabel_utama_dari_skema", // Pilih dari skema yang relevan
      "select_columns": [ {{ "field_name": "kolom1" }}, {{ "field_name": "kolom2" }} ], // Ganti dengan kolom relevan
      "filters": {{ /* ... */ }},
      "order_by_clauses": [ {{ "field_or_expression": "kolom_tanggal_atau_id", "direction": "DESC" }} ],
      "limit": 50,
      "result_key": "RAW_DATA_TABLE",
      "expected_result_format": "raw_table_data"
  }},
  "response_template": "Berikut adalah data untuk {{{{GENERIC_RESULT_KEY}}}} terkait {intent}.",
  "placeholder_mapping": {{
    "GENERIC_RESULT_KEY": {{ "type": "general_text", "label": "Hasil ({intent})" }}
  }},
  "data_source_info": {{
    "description": "Data diambil berdasarkan interpretasi umum dari permintaan.",
    "tables_used": ["nama_tabel_yang_digunakan"],
    "join_details": [],
    "filters_applied": ["filter_yang_diterapkan"]
  }}
}}
    """
    default_rules = """
Aturan Umum Perencanaan (Fallback):
1.  Analisis skema yang diberikan dengan seksama.
2.  Cobalah untuk menjawab permintaan pengguna seakurat mungkin menggunakan tabel dan kolom yang tersedia.
3.  Jika permintaan tidak dapat dipenuhi, hasilkan `database_operations_plan` sebagai list kosong dan jelaskan di `response_template`.
"""
    return {
        "intent_specific_json_example": default_json_example,
        "intent_specific_rules": default_rules
    }