# backend/app/langgraph_workflow/nodes/presenter.py
from typing import Dict, Any, List, Optional
from backend.app.schemas.agent_state import AgentState

def format_as_rupiah(amount: float) -> str:
    """Formats a float as an IDR currency string."""
    return f"Rp {amount:,.0f}".replace(",", ".")

def present_financial_report(state: AgentState, report_data: List[Dict[str, Any]]) -> AgentState:
    """
    Mengambil data mentah dari tool database, memformatnya menjadi
    laporan terstruktur, dan mengisi field-field di AgentState.
    Ini adalah "tool" internal yang tidak memanggil API luar.
    """
    print("--- Formatting Data with presenter_tool ---")

    if not report_data:
        state['final_narrative'] = "Saya tidak menemukan data yang relevan dengan permintaan Anda."
        state['warnings_for_display'] = ["Info: Tidak ada data yang ditemukan."]
        state['quality_score'] = 0
        return state

    # --- 1. Persiapan Data Table untuk UI (data_table_for_display) ---
    table_for_display = []
    total_outstanding = 0
    total_customers = set()

    for item in report_data:
        outstanding_amount = item.get('DocValueLocal', 0) - item.get('PaymentValueLocal', 0)
        total_outstanding += outstanding_amount
        total_customers.add(item.get('CustomerCode'))

        table_for_display.append({
            "Customer Name": item.get('Name', 'N/A'),
            "Invoice Number": item.get('DocNo', 'N/A'),
            "Invoice Amount": format_as_rupiah(item.get('DocValueLocal', 0)),
            "Outstanding": format_as_rupiah(outstanding_amount),
            "Due Date": item.get('DueDate', 'N/A').strftime('%d %b %Y') if item.get('DueDate') else 'N/A'
        })
    
    state['data_table_for_display'] = table_for_display

    # --- 2. Persiapan Ringkasan Eksekutif (executive_summary) ---
    avg_days_overdue = 0  # Perhitungan ini bisa ditambahkan jika datanya ada
    state['executive_summary'] = {
        "Total Outstanding": format_as_rupiah(total_outstanding),
        "Jumlah Customer Outstanding": f"{len(total_customers)} customer",
        "Rata-rata Keterlambatan": f"{int(avg_days_overdue)} hari"
    }

    # --- 3. Persiapan Analisis Naratif (final_narrative) ---
    # Di sini kita bisa memanggil LLM lagi secara spesifik untuk membuat narasi,
    # atau membuat template sederhana. Untuk MVP, kita pakai template.
    top_customer = max(report_data, key=lambda x: x.get('DocValueLocal', 0) - x.get('PaymentValueLocal', 0))
    top_customer_name = top_customer.get('Name', 'N/A')
    top_outstanding_amount = top_customer.get('DocValueLocal', 0) - top_customer.get('PaymentValueLocal', 0)

    narrative = (
        f"Ditemukan {len(total_customers)} customer dengan total piutang sebesar {format_as_rupiah(total_outstanding)}.\n\n"
        f"**Analisis Risiko:**\n"
        f"Customer dengan risiko tertinggi adalah **{top_customer_name}** dengan nilai outstanding sebesar {format_as_rupiah(top_outstanding_amount)}.\n\n"
        f"**Rekomendasi:**\n"
        f"Disarankan untuk melakukan follow-up prioritas kepada customer dengan nilai outstanding terbesar."
    )
    state['final_narrative'] = narrative
    
    # --- 4. Persiapan Catatan Kualitas (warnings_for_display & quality_score) ---
    state['warnings_for_display'] = [f"✅ Data berhasil diproses ({len(report_data)} record)."]
    state['quality_score'] = 95 # Contoh skor statis

    print("--- Formatting Complete. AgentState updated. ---")
    return state