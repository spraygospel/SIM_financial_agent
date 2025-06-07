# backend/app/langgraph_workflow/nodes/validate_results.py
from typing import Dict, Any, List, Optional
import sys
from datetime import datetime

from backend.app.schemas.agent_state import AgentState

def validate_results_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: validate_results_node ---", file=sys.stderr)

    financial_calculations: Optional[Dict[str, Any]] = state.get("financial_calculations")
    raw_query_results: Optional[List[Dict[str, Any]]] = state.get("raw_query_results")
    query_execution_status: Optional[str] = state.get("query_execution_status")
    query_execution_errors: Optional[List[Dict[str, str]]] = state.get("query_execution_errors", [])
    
    # Untuk MVP, validation_rules_for_results mungkin belum diisi dari plan_execution.
    # Kita akan melakukan validasi generik.
    # validation_rules: Optional[List[Dict[str, Any]]] = state.get("validation_rules_for_results")

    data_quality_checks: Dict[str, Any] = {
        "negative_values_found_in_financials": False, # Contoh
        "null_values_in_raw_data_critical_fields": 0, # Contoh
        "calculations_consistent": True, # Default, bisa diubah
        "data_found_for_query": True # Default
    }
    validation_warnings: List[str] = []
    validation_status: str = "passed" # Default
    quality_score: int = 100 # Default

    # 1. Periksa status eksekusi query dari node sebelumnya
    if query_execution_status == "total_failure":
        validation_status = "failed_critical"
        quality_score = 0
        data_quality_checks["data_found_for_query"] = False
        user_msg = "Gagal mengeksekusi semua query yang dibutuhkan."
        tech_msg = f"Query execution resulted in total_failure. Errors: {query_execution_errors}"
        validation_warnings.append(f"Critical: {user_msg}")
        print(f"validate_results_node: {tech_msg}", file=sys.stderr)
        return {
            "data_quality_checks": data_quality_checks,
            "validation_warnings": validation_warnings,
            "validation_status": validation_status,
            "quality_score": quality_score,
            "current_node_name": "validate_results",
            "error_message_for_user": user_msg,
            "technical_error_details": tech_msg
        }
    elif query_execution_status == "no_queries":
        validation_status = "failed_no_data" # Atau status lain yang sesuai
        quality_score = 10 # Mungkin tidak ada data karena tidak ada query
        data_quality_checks["data_found_for_query"] = False
        user_msg = "Tidak ada query yang direncanakan untuk dieksekusi."
        tech_msg = "No queries were planned for execution."
        validation_warnings.append(f"Info: {user_msg}")
        print(f"validate_results_node: {tech_msg}", file=sys.stderr)
        # Ini mungkin bukan error kritis, tapi tidak ada data untuk divalidasi/ditampilkan
        return {
            "data_quality_checks": data_quality_checks,
            "validation_warnings": validation_warnings,
            "validation_status": validation_status,
            "quality_score": quality_score,
            "current_node_name": "validate_results",
            "error_message_for_user": user_msg, # Atau biarkan kosong jika ini bukan error
            "technical_error_details": tech_msg
        }

    # 2. Validasi financial_calculations
    if financial_calculations:
        for key, value in financial_calculations.items():
            if isinstance(value, str) and "ERROR:" in value:
                data_quality_checks["calculations_consistent"] = False
                validation_warnings.append(f"Peringatan: Kalkulasi untuk '{key}' menghasilkan error: {value}")
                quality_score -= 20
            # Contoh validasi sederhana: jika angka, tidak boleh negatif (tergantung metrik)
            # Ini perlu aturan yang lebih spesifik dari `validation_rules_for_results` nantinya
            if isinstance(value, (int, float)) and value < 0:
                 # Ini sangat tergantung konteks, misal profit bisa negatif.
                 # Untuk demo ini, kita anggap saja sebagai potensi warning jika bukan metrik yang jelas boleh negatif.
                 if "profit" not in key.lower() and "margin" not in key.lower() and "change" not in key.lower():
                    data_quality_checks["negative_values_found_in_financials"] = True
                    validation_warnings.append(f"Peringatan: Metrik '{key}' memiliki nilai negatif: {value}")
                    quality_score -= 10
    else:
        # Jika tidak ada financial_calculations tapi query_execution_status bukan error total
        if not raw_query_results: # Dan juga tidak ada raw data
            validation_warnings.append("Info: Tidak ada data hasil kalkulasi finansial.")
            data_quality_checks["data_found_for_query"] = False
            quality_score -= 30
            validation_status = "passed_with_notes" # Atau "failed_no_data" jika ini dianggap gagal


    # 3. Validasi raw_query_results (Contoh dasar)
    if raw_query_results:
        if not financial_calculations: # Jika hanya raw data yang ada
            validation_warnings.append("Info: Hanya data mentah yang tersedia, tidak ada kalkulasi finansial.")
            quality_score -= 15
            
        # Contoh: Cek null di kolom penting (misal 'customer_name' jika ada di skema dan diharapkan)
        # Ini memerlukan pengetahuan skema yang lebih dalam atau aturan dari LLM.
        # Untuk MVP, kita bisa skip validasi kolom spesifik di raw_query_results kecuali ada aturan jelas.
        # Misal, jika ada lebih dari 50% baris dengan field penting bernilai None
        # num_rows_with_nulls = 0
        # for row in raw_query_results:
        #     if row.get("critical_column_example") is None: # Ganti "critical_column_example"
        #         num_rows_with_nulls +=1
        # if num_rows_with_nulls > len(raw_query_results) / 2 :
        #    data_quality_checks["null_values_in_raw_data_critical_fields"] = num_rows_with_nulls
        #    validation_warnings.append(f"Warning: Significant nulls found in critical fields of raw data.")
        #    quality_score -= 20
        pass # Placeholder untuk validasi raw data yang lebih canggih

    elif not financial_calculations: # Jika keduanya tidak ada (sudah dicek di atas juga)
        validation_status = "failed_no_data"
        quality_score = 0
        data_quality_checks["data_found_for_query"] = False
        user_msg = "Tidak ada data yang ditemukan setelah eksekusi query."
        tech_msg = "Both financial_calculations and raw_query_results are empty/None."
        validation_warnings.append(f"Kritis: {user_msg}")
        print(f"validate_results_node: {tech_msg}", file=sys.stderr)
        return {
            "data_quality_checks": data_quality_checks,
            "validation_warnings": validation_warnings,
            "validation_status": validation_status,
            "quality_score": quality_score,
            "current_node_name": "validate_results",
            "error_message_for_user": user_msg,
            "technical_error_details": tech_msg
        }
        
    # 4. Handle query_execution_errors jika ada (misalnya partial_failure)
    if query_execution_errors:
        for err in query_execution_errors:
            validation_warnings.append(f"Catatan Eksekusi: Query '{err.get('query', 'N/A')}' mengalami masalah: {err.get('error', 'Unknown error')}")
        quality_score -= (len(query_execution_errors) * 5) # Kurangi skor berdasarkan jumlah error
        if validation_status == "passed":
             validation_status = "passed_with_notes"


    # Penyesuaian akhir quality_score dan validation_status
    if quality_score < 0:
        quality_score = 0
    if quality_score < 50 and validation_status == "passed": # Jika skor rendah tapi status masih "passed"
        validation_status = "passed_with_warnings" # Anggap ada masalah signifikan
    if not data_quality_checks["calculations_consistent"] and validation_status == "passed":
        validation_status = "passed_with_warnings"

    if validation_status == "passed" and validation_warnings:
        validation_status = "passed_with_notes"


    print(f"validate_results_node: Validation Status: {validation_status}, Quality Score: {quality_score}", file=sys.stderr)
    if validation_warnings:
        print(f"validate_results_node: Warnings: {validation_warnings}", file=sys.stderr)

    # Mengikuti contoh dari 2_contoh.md untuk state output
    output_state_update: Dict[str, Any] = {
        "data_quality_checks": data_quality_checks, # Ini struktur detailnya bisa disesuaikan lagi
        "validation_warnings": validation_warnings, # Ini akan menjadi dasar untuk warnings_for_display
        "validation_status": validation_status,
        "quality_score": quality_score,
        "current_node_name": "validate_results"
    }
    
    # Jika validasi gagal kritis, set pesan error untuk pengguna
    if validation_status == "failed_critical":
        output_state_update["error_message_for_user"] = "Data yang dihasilkan tidak valid atau tidak konsisten."
        output_state_update["technical_error_details"] = f"Data validation failed with critical issues. Checks: {data_quality_checks}, Warnings: {validation_warnings}"
    elif validation_status == "failed_no_data":
         output_state_update["error_message_for_user"] = "Tidak ada data yang ditemukan untuk permintaan Anda."
         output_state_update["technical_error_details"] = "Validation determined no data was found or applicable."


    return output_state_update