# backend/app/schemas/api_models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Request Models ---
class QueryRequest(BaseModel):
    user_query: str = Field(..., description="Pertanyaan pengguna dalam bahasa alami.", example="Tunjukkan total penjualan bulan lalu.")
    session_id: str = Field(..., description="ID unik untuk sesi percakapan pengguna.", example="user_session_abc123")

# --- Response Models ---
class ExecutiveSummaryItem(BaseModel):
    metric_name: str = Field(description="Nama metrik yang diringkas.")
    value: str = Field(description="Nilai metrik yang sudah diformat sebagai string untuk tampilan.")
    label: str = Field(description="Label atau deskripsi singkat untuk metrik.")

class DataSourceDetails(BaseModel):
    description: Optional[str] = Field(default=None, description="Deskripsi umum sumber data.") # Dibuat opsional
    tables_used: List[str] = Field(default_factory=list, description="Daftar tabel utama yang digunakan.") # Dibuat opsional dengan default
    join_details: Optional[List[str]] = Field(default_factory=list, description="Penjelasan bagaimana tabel di-JOIN, jika ada.")
    filters_applied: Optional[List[str]] = Field(default_factory=list, description="Penjelasan filter utama yang diterapkan.")
    report_generated_at: Optional[str] = Field(default=None, description="Waktu laporan ini digenerate (diisi oleh API/Service).")


class QueryResponseSuccess(BaseModel):
    session_id: str = Field(description="ID sesi yang sama dengan request.")
    final_narrative: str = Field(description="Narasi analisis yang dihasilkan oleh agent.")
    data_table_for_display: List[Dict[str, Any]] = Field(description="Data mentah yang diformat untuk ditampilkan dalam tabel.")
    executive_summary: Optional[List[ExecutiveSummaryItem]] = Field(default_factory=list, description="Ringkasan metrik kunci (opsional).")
    warnings_for_display: Optional[List[str]] = Field(default_factory=list, description="Peringatan validasi data atau catatan untuk ditampilkan ke pengguna (opsional).")
    data_source_info: Optional[DataSourceDetails] = Field(default=None, description="Informasi mengenai sumber data untuk tabel yang ditampilkan.")
    data_quality_score: Optional[int] = Field(default=None, description="Skor kualitas data (0-100) dari proses validasi.")

class QueryResponseError(BaseModel):
    session_id: str = Field(description="ID sesi yang sama dengan request.")
    success: bool = Field(default=False, description="Selalu false untuk respons error.")
    error_type: str = Field(description="Kategori error, misal 'NLU_FAILURE', 'DB_ERROR', 'VALIDATION_ERROR', 'INTERNAL_AGENT_ERROR'.")
    user_message: str = Field(description="Pesan error yang aman dan mudah dimengerti untuk ditampilkan ke pengguna.")
    technical_details: Optional[str] = Field(default=None, description="Detail teknis error untuk logging (tidak selalu dikirim ke client).") # Dibuat opsional
    suggestions: Optional[List[str]] = Field(default_factory=list, description="Saran untuk pengguna jika ada (opsional).")

# Jika menggunakan Server-Sent Events (SSE) untuk pembaruan status (opsional untuk MVP awal)
class StreamUpdateEvent(BaseModel):
    event_type: str = Field(description="Tipe pembaruan, misal 'NODE_STARTED', 'NODE_COMPLETED', 'MCP_CALL', 'FALLBACK_TRIGGERED', 'FINAL_RESULT_READY'.")
    node_name: Optional[str] = Field(default=None, description="Nama node LangGraph yang terkait dengan event.")
    status: Optional[str] = Field(default=None, description="Status node atau proses (misal, 'processing', 'success', 'error').")
    timestamp: str = Field(description="Timestamp event ISO format.")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Data tambahan terkait event (misal, detail error, progress %.")
    message: Optional[str] = Field(default=None, description="Pesan singkat yang bisa ditampilkan di UI Process Monitor.")