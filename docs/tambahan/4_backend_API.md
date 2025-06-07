Baik, sekarang kita akan membuat **Dokumen Desain Antarmuka API (Backend FastAPI)**.

Dokumen ini akan mendefinisikan *endpoints* API yang akan disediakan oleh backend FastAPI, yang berfungsi sebagai jembatan antara frontend React.js dan LangGraph Workflow.

---

**Dokumen Perencanaan Tambahan 4: Desain Antarmuka API (Backend FastAPI)**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
2.  Prinsip Desain API
3.  Spesifikasi Endpoint
    3.1. Endpoint Utama Pemrosesan Query
        3.1.1. `POST /api/v1/query`
    3.2. Endpoint Pembaruan Status Real-time (Opsional untuk MVP Awal)
        3.2.1. `GET /api/v1/stream_updates/{session_id}`
4.  Struktur Data Umum (Pydantic Models)
5.  Autentikasi dan Autorisasi (Pertimbangan Masa Depan)
6.  Penanganan Error API

---

**1. Pendahuluan**

Dokumen ini merinci desain antarmuka pemrograman aplikasi (API) untuk backend sistem AI Agent yang dibangun menggunakan FastAPI. API ini akan melayani permintaan dari frontend (React.js), memprosesnya melalui LangGraph Workflow, dan mengembalikan hasil analisis atau pesan error.

---

**2. Prinsip Desain API**

*   **RESTful**: Menggunakan prinsip-prinsip RESTful untuk desain endpoint.
*   **Jelas dan Konsisten**: Menggunakan penamaan yang jelas dan struktur respons yang konsisten.
*   **Stateless (untuk `/query`)**: Endpoint `/query` utama bersifat stateless, mengandalkan `session_id` untuk konteks jika diperlukan oleh LangGraph.
*   **Validasi Input/Output**: Menggunakan Pydantic untuk validasi data request dan serialisasi data response.
*   **Asinkron**: Memanfaatkan kemampuan asinkron FastAPI dan LangGraph untuk menangani pemrosesan yang mungkin memakan waktu.

---

**3. Spesifikasi Endpoint**

**3.1. Endpoint Utama Pemrosesan Query**

   **3.1.1. `POST /api/v1/query`**
    *   **Deskripsi**: Menerima query pengguna dari frontend, memicunya melalui LangGraph Workflow, dan mengembalikan hasil analisis atau pesan error.
    *   **Method**: `POST`
    *   **URL**: `/api/v1/query`
    *   **Request Body**:
        *   Format: `application/json`
        *   Struktur (Pydantic Model `QueryRequest`):
            ```python
            from pydantic import BaseModel, Field
            from typing import List, Dict

            class QueryRequest(BaseModel):
                user_query: str = Field(..., description="Pertanyaan pengguna dalam bahasa alami.", example="Tunjukkan total penjualan bulan lalu.")
                session_id: str = Field(..., description="ID unik untuk sesi percakapan pengguna.", example="user_session_abc123")
                # conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Riwayat percakapan sebelumnya dalam sesi ini.") 
                # Jika riwayat percakapan dikelola oleh checkpointer LangGraph, ini mungkin tidak perlu dikirim setiap kali.
                # Namun, jika frontend yang mengelola, ini bisa dikirim. Untuk MVP, kita asumsikan checkpointer LangGraph yang utama.
            ```
    *   **Response Body (Sukses - HTTP 200 OK)**:
        *   Format: `application/json`
        *   Struktur (Pydantic Model `QueryResponseSuccess`):
            ```python
            from pydantic import BaseModel, Field
            from typing import List, Dict, Any, Optional

            class ExecutiveSummaryItem(BaseModel):
                metric_name: str
                value: str # Sudah diformat
                label: str

            class QueryResponseSuccess(BaseModel):
                session_id: str
                final_narrative: str = Field(description="Narasi analisis yang dihasilkan oleh agent.")
                data_table_for_display: List[Dict[str, Any]] = Field(description="Data mentah yang diformat untuk ditampilkan dalam tabel.")
                executive_summary: Optional[List[ExecutiveSummaryItem]] = Field(default_factory=list, description="Ringkasan metrik kunci.")
                warnings_for_display: Optional[List[str]] = Field(default_factory=list, description="Peringatan validasi data untuk ditampilkan ke pengguna.")
                # Optional: Tambahkan field untuk UI monitoring jika tidak menggunakan endpoint streaming terpisah
                # query_duration_ms: Optional[int] = Field(description="Durasi total pemrosesan query dalam milidetik.")
                # steps_completed: Optional[List[str]] = Field(description="Node LangGraph yang berhasil dieksekusi.")
            ```
    *   **Response Body (Error Aplikasi - HTTP 200 OK dengan status error internal, atau HTTP 4xx/5xx)**:
        *   Struktur (Pydantic Model `QueryResponseError`):
            ```python
            class QueryResponseError(BaseModel):
                session_id: str
                success: bool = Field(default=False)
                error_type: str = Field(description="Kategori error, misal 'NLU_FAILURE', 'DB_ERROR', 'VALIDATION_ERROR'.")
                user_message: str = Field(description="Pesan error yang aman dan mudah dimengerti untuk ditampilkan ke pengguna.")
                # technical_details: Optional[str] = Field(default=None, description="Detail teknis error untuk debugging (opsional, mungkin hanya untuk log server).")
                suggestions: Optional[List[str]] = Field(default_factory=list, description="Saran untuk pengguna jika ada.")
            ```
        *   **Catatan Kode Status HTTP**:
            *   Jika error terjadi karena input pengguna yang salah (misal, `user_query` kosong), gunakan **HTTP 400 Bad Request** atau **HTTP 422 Unprocessable Entity**.
            *   Jika error terjadi di sisi server (misal, LangGraph gagal, database error), bisa tetap **HTTP 200 OK** namun dengan `success: false` dalam body, atau gunakan **HTTP 500 Internal Server Error** jika lebih sesuai. Konsistensi adalah kunci. Untuk MVP, HTTP 200 dengan `success: false` mungkin lebih mudah dihandle frontend.

**3.2. Endpoint Pembaruan Status Real-time (Opsional untuk MVP Awal, tapi direkomendasikan untuk UX yang baik)**

Jika Anda ingin UI `ProcessMonitor` dan sejenisnya di frontend diperbarui secara *real-time*, Anda memerlukan mekanisme seperti Server-Sent Events (SSE) atau WebSockets.

   **3.2.1. `GET /api/v1/stream_updates/{session_id}` (Menggunakan Server-Sent Events)**
    *   **Deskripsi**: Mengirimkan aliran pembaruan status pemrosesan query untuk `session_id` tertentu. Frontend akan membuat koneksi ke endpoint ini setelah mengirim query via `POST /api/v1/query`.
    *   **Method**: `GET`
    *   **URL**: `/api/v1/stream_updates/{session_id}`
    *   **Path Parameter**:
        *   `session_id: str` - ID sesi yang ingin dipantau.
    *   **Response Body**:
        *   Format: `text/event-stream`
        *   Setiap *event* adalah objek JSON dengan struktur (Pydantic Model `StreamUpdateEvent`):
            ```python
            class StreamUpdateEvent(BaseModel):
                event_type: str = Field(description="Tipe pembaruan, misal 'NODE_STARTED', 'NODE_COMPLETED', 'MCP_CALL', 'FALLBACK_TRIGGERED', 'FINAL_RESULT_READY'.")
                node_name: Optional[str] = Field(default=None, description="Nama node LangGraph yang terkait dengan event.")
                status: Optional[str] = Field(default=None, description="Status node atau proses (misal, 'processing', 'success', 'error').")
                timestamp: str = Field(description="Timestamp event.")
                data: Optional[Dict[str, Any]] = Field(default=None, description="Data tambahan terkait event (misal, detail error, progress %.")
                # Contoh spesifik untuk UI monitoring
                # context_usage_percent: Optional[int]
                # current_step_description: Optional[str]
            ```
    *   **Cara Kerja**:
        1.  Frontend melakukan POST ke `/api/v1/query`.
        2.  Backend FastAPI memulai LangGraph Workflow secara asinkron untuk `session_id` tersebut.
        3.  Frontend kemudian membuka koneksi SSE ke `/api/v1/stream_updates/{session_id}`.
        4.  Selama LangGraph Workflow berjalan, ia (atau wrapper di sekitarnya) akan mem-publish *event* pembaruan.
        5.  Backend FastAPI akan mengirimkan *event* ini melalui koneksi SSE ke frontend.
        6.  Ketika hasil akhir siap, sebuah event `FINAL_RESULT_READY` bisa dikirim, atau frontend bisa menunggu respons dari `POST /api/v1/query` awal.
    *   **Alternatif**: WebSocket bisa digunakan jika komunikasi dua arah diperlukan, tapi SSE lebih sederhana untuk pembaruan satu arah dari server ke client.

---

**4. Struktur Data Umum (Pydantic Models)**

Model Pydantic yang digunakan dalam Request/Response Body di atas sudah mencakup sebagian besar struktur data yang dibutuhkan. Pastikan untuk menjaga konsistensi model ini antara backend dan kontrak yang diharapkan oleh frontend.

---

**5. Autentikasi dan Autorisasi (Pertimbangan Masa Depan)**

Untuk MVP awal, autentikasi mungkin belum menjadi prioritas utama. Namun, untuk pengembangan selanjutnya, pertimbangkan:

*   **Autentikasi API Key**: Untuk akses programatik atau antar-service.
*   **Autentikasi berbasis Token (JWT)**: Jika ada login pengguna.
*   Header `Authorization: Bearer <token>` pada setiap request.
*   Mekanisme otorisasi untuk membatasi akses berdasarkan peran pengguna atau grup (misalnya, hanya user tertentu yang boleh melihat data finansial sensitif).

---

**6. Penanganan Error API**

*   Backend harus menangkap semua potensi error dari LangGraph Workflow atau MCP Server.
*   Menggunakan `HTTPException` dari FastAPI untuk error standar HTTP (400, 401, 403, 404, 500).
*   Untuk error aplikasi yang berhasil ditangkap (misalnya, query tidak valid setelah diproses agent), kembalikan HTTP 200 OK dengan body `QueryResponseError` yang berisi `success: false` dan detail error yang relevan.
*   Semua error harus dicatat (log) di sisi server dengan detail teknis yang cukup untuk debugging.

Contoh Implementasi Error di FastAPI:
```python
from fastapi import FastAPI, HTTPException, Body
# ... import Pydantic models ...

app = FastAPI()

@app.post("/api/v1/query", response_model=Union[QueryResponseSuccess, QueryResponseError])
async def process_user_query(request_data: QueryRequest = Body(...)):
    try:
        # ... panggil LangGraph Workflow ...
        # Contoh hasil sukses:
        # final_result = await langgraph_workflow.arun(session_id=request_data.session_id, user_query=request_data.user_query)
        # return QueryResponseSuccess(**final_result, session_id=request_data.session_id)
        
        # Contoh simulasi error dari agent
        if "error" in request_data.user_query:
            return QueryResponseError(
                session_id=request_data.session_id,
                error_type="AGENT_PROCESSING_ERROR",
                user_message="Maaf, terjadi kesalahan saat memproses permintaan Anda.",
                suggestions=["Coba sederhanakan pertanyaan Anda."]
            )

        # Contoh validasi input gagal
        if not request_data.user_query.strip():
            raise HTTPException(status_code=422, detail="User query tidak boleh kosong.")

        # Placeholder untuk hasil sukses
        return QueryResponseSuccess(
            session_id=request_data.session_id,
            final_narrative="Ini adalah narasi hasil.",
            data_table_for_display=[{"kolom1": "nilai1"}],
            executive_summary=[{"metric_name": "Total Sales", "value": "Rp 100.000", "label": "Penjualan Bulan Ini"}],
            warnings_for_display=["Data mungkin belum lengkap untuk periode akhir."]
        )

    except HTTPException as http_exc:
        raise http_exc # Re-raise HTTPException agar FastAPI menanganinya
    except Exception as e:
        # Log error e
        # Untuk error server yang tidak terduga
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan internal server: {str(e)}")

# Tambahkan endpoint untuk SSE jika diimplementasikan
# from sse_starlette.sse import EventSourceResponse
# async def event_generator(session_id: str, request: Request):
#     # Logika untuk menghasilkan event
#     pass
# @app.get("/api/v1/stream_updates/{session_id}")
# async def stream_updates(session_id: str, request: Request):
#     return EventSourceResponse(event_generator(session_id, request))

```
---
