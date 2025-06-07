# backend/app/langgraph_workflow/nodes/replace_placeholders.py
from typing import Dict, Any, List, Optional
import sys
from datetime import datetime, date
import re # Untuk mengganti placeholder

from backend.app.schemas.agent_state import AgentState
from backend.app.schemas.api_models import ExecutiveSummaryItem 
from backend.app.core.config import settings # Mungkin tidak dibutuhkan di sini, tapi jaga-jaga

# --- Fungsi Helper Pemformatan (mirip dengan yang ada di contoh atau MCP) ---
def format_value(value: Any, formatting_rule: Optional[Dict[str, Any]]) -> str:
    if isinstance(value, str) and value.startswith("ERROR:"): 
        return value
    if value is None:
        return "N/A"

    if not formatting_rule: # Jika tidak ada aturan, kembalikan sebagai string
        return str(value)

    rule_type = formatting_rule.get("type", "string")
    precision = formatting_rule.get("precision") # Bisa None

    try:
        if rule_type == "currency_IDR":
            # Pemformatan mata uang Rupiah sederhana
            num_value = float(value)
            return f"Rp {num_value:,.{precision if precision is not None else 2}f}".replace(",", "#").replace(".", ",").replace("#", ".")
        elif rule_type == "currency": # Generik, bisa disesuaikan
            num_value = float(value)
            return f"{num_value:,.{precision if precision is not None else 2}f}"
        elif rule_type == "number_with_separator":
            num_value = float(value)
            if precision is not None:
                 return f"{num_value:,.{precision}f}"
            # Jika value adalah integer, tampilkan tanpa desimal
            elif isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
                return f"{int(num_value):,}"
            else:
                return f"{num_value:,.2f}" # Default 2 desimal jika float
        elif rule_type == "number_with_decimal": # Alias untuk number_with_separator
             num_value = float(value)
             if precision is not None:
                 return f"{num_value:,.{precision}f}"
             elif isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
                return f"{int(num_value):,}"
             else:
                return f"{num_value:,.2f}"
        elif rule_type == "date_DD_MMM_YYYY":
            # Asumsi value adalah string tanggal ISO (YYYY-MM-DD) atau objek date/datetime
            dt_obj = datetime.fromisoformat(str(value).replace("Z", "")) if isinstance(value, str) else value
            return dt_obj.strftime("%d %b %Y")
        elif rule_type == "percentage":
            num_value = float(value)
            return f"{num_value:.{precision if precision is not None else 2}f}%"
        else: # Default: string
            return str(value)
    except (ValueError, TypeError) as e:
        print(f"replace_placeholders_node: Error formatting value '{value}' with rule '{formatting_rule}': {e}", file=sys.stderr)
        return str(value) # Kembalikan nilai asli jika error format

def replace_placeholders_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: replace_placeholders_node ---", file=sys.stderr)

    response_template: Optional[str] = state.get("response_template")
    financial_calculations: Optional[Dict[str, Any]] = state.get("financial_calculations")
    placeholder_mapping: Optional[Dict[str, Dict[str, Any]]] = state.get("placeholder_mapping")
    raw_query_results: Optional[List[Dict[str, Any]]] = state.get("raw_query_results")
    
    # Ambil dari state yang sudah ada
    data_source_info: Optional[Dict[str, Any]] = state.get("data_source_info", {})
    validation_warnings_from_prev_node: Optional[List[str]] = state.get("validation_warnings", [])
    current_mcp_history = state.get("mcp_tool_call_history", [])

    final_narrative = response_template if response_template else "Tidak ada narasi yang dihasilkan."
    data_table_for_display: List[Dict[str, Any]] = []
    executive_summary_items: List[ExecutiveSummaryItem] = [] # Menggunakan type dari agent_state.py
    
    # 1. Isi placeholder dalam narasi
    if response_template and financial_calculations and placeholder_mapping:
        # Pola regex untuk menemukan placeholder seperti {{PLACEHOLDER_NAME}}
        # Memastikan placeholder adalah kata valid (huruf, angka, underscore)
        pattern = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")
        
        def replace_match(match):
            placeholder_key = match.group(1)
            if placeholder_key in financial_calculations:
                value_to_format = financial_calculations[placeholder_key]
                formatting_rule = placeholder_mapping.get(placeholder_key)
                return format_value(value_to_format, formatting_rule)
            else:
                # Jika placeholder tidak ada di financial_calculations, biarkan apa adanya atau beri penanda
                print(f"replace_placeholders_node: Placeholder '{{{{{placeholder_key}}}}}' not found in financial_calculations.", file=sys.stderr)
                return f"{{{{Data N/A: {placeholder_key}}}}}" # Penanda bahwa data tidak ada
        
        final_narrative = pattern.sub(replace_match, response_template)
    elif not response_template:
        validation_warnings_from_prev_node.append("Info: Template respons tidak dibuat oleh node perencanaan.")

    # 2. Siapkan data_table_for_display dari raw_query_results
    # Ini memerlukan pemformatan kolom yang lebih canggih berdasarkan tipe data aktual
    # Untuk MVP, kita bisa melakukan pemformatan dasar atau mengandalkan frontend
    # Contoh dari 2_contoh.md menunjukkan pemformatan angka dan tanggal di sini.
    if raw_query_results:
        # Untuk menentukan pemformatan kolom, idealnya kita punya info tipe data dari skema atau hasil query.
        # Atau, kita bisa mencoba mendeteksi tipe dan menerapkan pemformatan sederhana.
        for row in raw_query_results:
            formatted_row = {}
            for col_name, col_value in row.items():
                # Contoh pemformatan dasar (bisa diperluas)
                from datetime import datetime, date
                if isinstance(col_value, (int, float)):
                    # Asumsi format angka default jika tidak ada aturan spesifik dari placeholder_mapping
                    # (placeholder_mapping biasanya untuk financial_calculations, bukan raw_data)
                    formatted_row[col_name] = format_value(col_value, {"type": "number_with_separator"})
                elif isinstance(col_value, (datetime, date)): 
                     formatted_row[col_name] = format_value(col_value, {"type": "date_DD_MMM_YYYY"})
                else:
                    formatted_row[col_name] = str(col_value) if col_value is not None else "N/A"
            data_table_for_display.append(formatted_row)

    # 3. Siapkan executive_summary
    # Ini juga akan menggunakan financial_calculations dan placeholder_mapping
    # Struktur ExecutiveSummaryItem: {"metric_name": str, "value": str, "label": str}
    # Kita asumsikan placeholder_mapping memiliki info label atau kita bisa buat label generik.
    if financial_calculations and placeholder_mapping:
        for key, rule in placeholder_mapping.items():
            if key in financial_calculations and financial_calculations[key] is not None:
                # rule bisa berisi 'label' atau kita buat dari key
                label = rule.get("label", key.replace("_", " ").title()) 
                # Atau jika ada field 'purpose' di placeholder_mapping yg dibuat plan_execution
                # label = rule.get("purpose", key.replace("_", " ").title())
                
                value = financial_calculations[key]
                formatted_val = format_value(value, rule)
                
                executive_summary_items.append(
                    {"metric_name": key, "value": formatted_val, "label": label}
                )
    
    # 4. Siapkan warnings_for_display
    # Ini hanya meneruskan validation_warnings dari node sebelumnya
    warnings_for_display = validation_warnings_from_prev_node if validation_warnings_from_prev_node else []

    # 5. Log "pseudo" MCP call untuk operasi ini (jika dianggap sebagai tool formatting)
    mcp_log_entry = {
        "server_name": "placeholder_system_inline",
        "tool_name": "fill_placeholders_and_format_output_inline",
        "request_payload": {
            "response_template": response_template,
            "data_values": financial_calculations,
            "formatting_rules": placeholder_mapping,
            "raw_data": raw_query_results
        },
        "response_payload": {
            "final_narrative": final_narrative,
            "data_table_for_display": data_table_for_display,
            "executive_summary": executive_summary_items,
            "warnings_for_display": warnings_for_display
        },
        "status": "success",
        "error_message": None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    current_mcp_history.append(mcp_log_entry)

    print(f"replace_placeholders_node: Placeholders replaced and output formatted.", file=sys.stderr)

    return {
        "final_narrative": final_narrative,
        "data_table_for_display": data_table_for_display,
        "executive_summary": [dict(item) for item in executive_summary_items], # Konversi balik ke dict jika perlu
        "warnings_for_display": warnings_for_display,
        "data_source_info": data_source_info, # Teruskan dari state sebelumnya
        "current_node_name": "replace_placeholders",
        "workflow_status": "completed", # Tandai workflow selesai
        "mcp_tool_call_history": current_mcp_history
    }