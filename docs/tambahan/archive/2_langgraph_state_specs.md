
**Dokumen Perencanaan Tambahan 2: Detail State LangGraph Setiap Node (Revisi & Tambahan)**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
2.  Struktur State Global LangGraph
3.  Detail Node
    3.1. Node 1: `understand_query`
    3.2. Node 2: `consult_schema`
    3.3. Node 3: `plan_execution`
    3.4. Node 4: `execute_query`
    3.5. Node 5: `validate_results`
    3.6. Node 6: `replace_placeholders`
4.  Node Error: `generate_error_response`

---

**1. Pendahuluan**

Dokumen ini memberikan rincian operasional untuk setiap node dalam alur kerja (workflow) LangGraph AI Agent. Fokus utama adalah pada aliran *state* (data) secara keseluruhan, interaksi dengan MCP Server, dan strategi penanganan error untuk setiap node. Tujuannya adalah untuk memastikan setiap node memiliki input yang jelas, proses yang terdefinisi, dan output yang konsisten, serta siap menghadapi berbagai skenario kegagalan.

---

**2. Struktur State Global LangGraph (Contoh)**

Berikut adalah contoh struktur data utama (state) yang akan dikelola dan dimodifikasi oleh berbagai node dalam LangGraph. Tidak semua *key* akan ada di setiap tahap, dan beberapa *key* akan ditambahkan oleh node tertentu.

```python
# Menggunakan TypedDict untuk representasi state di Python
from typing import TypedDict, List, Dict, Any, Optional

class TimePeriod(TypedDict):
    start_date: Optional[str]
    end_date: Optional[str]
    period_label: Optional[str]

class MCPToolCallLog(TypedDict):
    server_name: str
    tool_name: str
    request_payload: Dict[str, Any]
    response_payload: Optional[Dict[str, Any]]
    status: str # 'success' atau 'error'
    error_message: Optional[str]
    timestamp: str

class SqlQueryPlan(TypedDict):
    purpose: str
    query: str
    result_key: str # Key untuk menyimpan hasil di financial_calculations atau raw_data_query
    # error_handling_strategy: Optional[str] # Misal 'retry_simplified', 'skip'

class AgentState(TypedDict):
    # Input Awal & Konteks Sesi
    user_query: str
    session_id: str
    conversation_history: List[Dict[str, str]] # [{ "role": "user", "content": "..."}]
    
    # Hasil dari `understand_query`
    intent: Optional[str]
    entities_mentioned: Optional[List[str]]
    time_period: Optional[TimePeriod]
    requested_metrics: Optional[List[str]]
    query_complexity: Optional[str] # 'simple', 'medium', 'complex'

    # Hasil dari `consult_schema`
    relevant_tables: Optional[List[Dict[str, Any]]] # Menggunakan struktur TableSchemaMcp dari MCP Server
    table_relationships: Optional[List[Dict[str, Any]]] # Menggunakan struktur RelationshipMcp
    financial_columns: Optional[Dict[str, List[str]]]
    temporal_columns: Optional[Dict[str, List[str]]]
    schema_consultation_warnings: Optional[List[str]] # Peringatan jika skema tidak lengkap atau ambigu

    # Hasil dari `plan_execution`
    sql_queries_plan: Optional[List[SqlQueryPlan]] # Rencana query SQL yang akan dieksekusi
    response_template: Optional[str] # Template narasi dengan placeholder
    placeholder_mapping: Optional[Dict[str, str]] # Aturan pemformatan untuk placeholder
    raw_data_query_plan: Optional[SqlQueryPlan] # Rencana query untuk tabel data mentah
    validation_rules_for_results: Optional[List[Dict[str, Any]]] # Aturan untuk node validate_results

    # Hasil dari `execute_query`
    financial_calculations: Optional[Dict[str, Any]] # Hasil agregasi, misal {"TOTAL_SALES_JAN_2023": 125000}
    raw_query_results: Optional[List[Dict[str, Any]]] # Hasil data mentah untuk tabel
    query_execution_status: Optional[str] # 'success', 'partial_failure', 'total_failure'
    query_execution_errors: Optional[List[Dict[str, str]]] # Detail error jika ada

    # Hasil dari `validate_results`
    data_quality_checks: Optional[Dict[str, Any]]
    validation_warnings: Optional[List[str]]
    validation_status: Optional[str] # 'passed', 'passed_with_warnings', 'failed_critical'
    quality_score: Optional[int] # 0-100

    # Hasil dari `replace_placeholders` (Output Final)
    final_narrative: Optional[str]
    data_table_for_display: Optional[List[Dict[str, Any]]]
    executive_summary: Optional[Dict[str, Any]]
    warnings_for_display: Optional[List[str]]

    # Logging dan Status Internal
    current_node_name: Optional[str]
    error_message_for_user: Optional[str] # Pesan error yang aman untuk ditampilkan ke user
    technical_error_details: Optional[str] # Detail error teknis untuk logging
    mcp_tool_call_history: List[MCPToolCallLog] # Riwayat pemanggilan tool MCP
    workflow_status: str # 'processing', 'completed', 'error'
```

---

**3. Detail Node**

**3.1. Node 1: `understand_query`**
*   **Fungsi**: Menganalisis dan memahami pertanyaan pengguna dalam *natural language*.
*   **Input State (Full)**:
    *   `user_query: str`
    *   `session_id: str`
    *   `conversation_history: List[Dict[str, str]]`
    *   `mcp_tool_call_history: List[MCPToolCallLog]` (awalnya kosong)
    *   `workflow_status: str` (awalnya 'processing')
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"understand_query"`.
    2.  Menggunakan LLM (DeepSeek via API OpenAI-compatible) untuk:
        *   **Intent Classification**: Mengidentifikasi tujuan utama query (misalnya, `sales_analysis`, `customer_report`).
        *   **Entity Extraction**: Menangkap entitas penting (misalnya, "sales" -> `business_domain`, "Januari 2023" -> `time_period_description`).
        *   **Metric Identification**: Menentukan metrik yang diminta (misalnya, `total_sales`, `transaction_count`).
        *   **Query Scope Analysis**: Memperkirakan kompleksitas query.
    3.  Mengkonversi entitas waktu (seperti "Januari 2023") menjadi format tanggal standar (`start_date`, `end_date`).
    4.  Tidak ada interaksi dengan MCP Server pada node ini (kecuali LLM call itu sendiri dianggap sebagai tool abstrak).
*   **Output State (Full)**:
    *   Semua *key* dari Input State.
    *   Ditambah/Dimodifikasi:
        *   `intent: str`
        *   `entities_mentioned: List[str]`
        *   `time_period: TimePeriod`
        *   `requested_metrics: List[str]`
        *   `query_complexity: str`
        *   `current_node_name: str`
*   **Potensi Error dan Penanganannya**:
    *   **Error**: LLM tidak dapat memahami query (intent tidak jelas, entitas ambigu).
        *   **Penanganan**:
            *   Set `validation_status` ke `'failed_understanding'`.
            *   Set `error_message_for_user` dengan pesan meminta klarifikasi.
            *   Alihkan ke `generate_error_response` node atau langsung minta klarifikasi dari user jika arsitektur mendukung.
    *   **Error**: LLM API call gagal (timeout, error koneksi).
        *   **Penanganan**:
            *   Strategi *retry* dengan *backoff exponential* untuk LLM call.
            *   Jika *retry* gagal, set `technical_error_details` dan `error_message_for_user` (pesan generik).
            *   Alihkan ke `generate_error_response`.
*   **Ketergantungan pada Node Sebelumnya**: Tidak ada (ini adalah node awal setelah input pengguna).

**3.2. Node 2: `consult_schema`**
*   **Fungsi**: Berkonsultasi dengan Graphiti melalui MCP Server untuk mendapatkan informasi skema database yang relevan.
*   **Input State (Full)**:
    *   Semua *key* dari output `understand_query`.
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"consult_schema"`.
    2.  Menggunakan `intent` dan `entities_mentioned` dari *state*.
    3.  **Interaksi dengan `graphiti_mcp_server`**:
        *   Memanggil tool `get_relevant_schema_info`.
        *   **Request Payload**: `{ "intent": state.intent, "entities": state.entities_mentioned }`
        *   Mencatat pemanggilan ke `mcp_tool_call_history`.
    4.  Menerima respons dari `graphiti_mcp_server` yang berisi `relevant_tables`, `table_relationships`, `financial_columns`, `temporal_columns`.
    5.  Memproses respons:
        *   Jika tidak ada tabel relevan ditemukan, set `schema_consultation_warnings` dengan pesan "Tidak ada tabel relevan ditemukan untuk query ini."
*   **Output State (Full)**:
    *   Semua *key* dari Input State.
    *   Ditambah/Dimodifikasi:
        *   `relevant_tables: List[TableSchemaMcp]`
        *   `table_relationships: List[RelationshipMcp]`
        *   `financial_columns: Dict[str, List[str]]`
        *   `temporal_columns: Dict[str, List[str]]`
        *   `schema_consultation_warnings: Optional[List[str]]`
        *   `mcp_tool_call_history` (diperbarui)
        *   `current_node_name: str`
*   **Potensi Error dan Penanganannya**:
    *   **Error**: `graphiti_mcp_server` tidak merespons atau *tool call* gagal.
        *   **Penanganan**:
            *   Strategi *retry* untuk MCP call.
            *   Jika gagal, set `technical_error_details` ("Graphiti MCP Server communication error").
            *   Set `error_message_for_user` ("Tidak dapat mengambil informasi skema database saat ini.").
            *   Alihkan ke `generate_error_response`.
    *   **Error**: Respons dari `graphiti_mcp_server` tidak valid atau kosong padahal diharapkan ada data.
        *   **Penanganan**:
            *   Set `schema_consultation_warnings` dengan detail.
            *   Lanjutkan proses jika memungkinkan (mungkin dengan skema default yang sangat terbatas atau tanpa skema). Jika tidak, alihkan ke `generate_error_response` dengan pesan "Informasi skema tidak memadai."
*   **Ketergantungan pada Node Sebelumnya**: `intent`, `entities_mentioned` dari `understand_query`.

**3.3. Node 3: `plan_execution`**
*   **Fungsi**: Membuat rencana eksekusi SQL dan template respons dengan placeholder.
*   **Input State (Full)**:
    *   Semua *key* dari output `consult_schema`.
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"plan_execution"`.
    2.  Menggunakan `intent`, `entities_mentioned`, `time_period`, `requested_metrics`, dan informasi skema (`relevant_tables`, `financial_columns`, `temporal_columns`) dari *state*.
    3.  Menggunakan LLM untuk:
        *   **SQL Query Planning**: Merancang satu atau lebih query SQL berdasarkan informasi yang ada. Query harus aman (misalnya, hindari SQL injection, batasi `SELECT *`) dan efisien. Targetkan hanya kolom yang dibutuhkan.
        *   **Template Generation**: Membuat template narasi respons dengan placeholder (misalnya, `"{TOTAL_SALES_JAN_2023}"`). Placeholder harus konsisten dengan *result key* dari rencana SQL.
    4.  Menentukan aturan validasi dasar untuk hasil query (misalnya, `TOTAL_SALES` tidak boleh negatif).
    5.  Memetakan placeholder ke kalkulasi SQL dan menentukan aturan pemformatan untuk setiap placeholder (misalnya, `TOTAL_SALES_JAN_2023` -> `currency_IDR`).
*   **Output State (Full)**:
    *   Semua *key* dari Input State.
    *   Ditambah/Dimodifikasi:
        *   `sql_queries_plan: List[SqlQueryPlan]`
        *   `response_template: str`
        *   `placeholder_mapping: Dict[str, str]` (berisi tipe pemformatan)
        *   `raw_data_query_plan: Optional[SqlQueryPlan]`
        *   `validation_rules_for_results: Optional[List[Dict[str, Any]]]`
        *   `current_node_name: str`
*   **Potensi Error dan Penanganannya**:
    *   **Error**: LLM gagal membuat rencana SQL yang valid atau template respons.
        *   **Penanganan**:
            *   Jika informasi skema tidak memadai (berdasarkan `schema_consultation_warnings`), coba minta LLM untuk membuat query yang lebih generik atau informasikan pengguna bahwa query tidak dapat diproses dengan skema saat ini.
            *   Jika LLM call gagal, *retry*. Jika tetap gagal, alihkan ke `generate_error_response` dengan pesan "Tidak dapat merencanakan eksekusi query."
    *   **Error**: Tidak ada kolom finansial atau temporal yang cocok untuk metrik yang diminta.
        *   **Penanganan**: Set `validation_status` ke `'failed_planning'`, `error_message_for_user` ("Tidak dapat menemukan data yang sesuai untuk permintaan Anda."), alihkan ke `generate_error_response`.
*   **Ketergantungan pada Node Sebelumnya**: Semua output dari `understand_query` dan `consult_schema`.

**3.4. Node 4: `execute_query`**
*   **Fungsi**: Mengeksekusi query SQL ke database MySQL melalui MCP Server.
*   **Input State (Full)**:
    *   Semua *key* dari output `plan_execution`.
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"execute_query"`.
    2.  Mengambil `sql_queries_plan` dan `raw_data_query_plan` dari *state*.
    3.  **Interaksi dengan `mysql_mcp_server`**:
        *   Untuk setiap query dalam `sql_queries_plan` dan `raw_data_query_plan`:
            *   Memanggil tool `execute_sql_query`.
            *   **Request Payload**: `{ "sql_queries": [query_plan.query] }` (mengirim satu per satu atau batch jika didukung dan aman).
            *   Mencatat pemanggilan ke `mcp_tool_call_history`.
    4.  Mengumpulkan hasil:
        *   Menyimpan hasil agregasi ke `financial_calculations` menggunakan `result_key` dari `SqlQueryPlan`.
        *   Menyimpan hasil query data mentah ke `raw_query_results`.
    5.  Set `query_execution_status` berdasarkan hasil semua eksekusi ('success', 'partial_failure', 'total_failure').
    6.  Jika ada error, kumpulkan di `query_execution_errors`.
*   **Output State (Full)**:
    *   Semua *key* dari Input State.
    *   Ditambah/Dimodifikasi:
        *   `financial_calculations: Dict[str, Any]`
        *   `raw_query_results: List[Dict[str, Any]]`
        *   `query_execution_status: str`
        *   `query_execution_errors: Optional[List[Dict[str, str]]]`
        *   `mcp_tool_call_history` (diperbarui)
        *   `current_node_name: str`
*   **Potensi Error dan Penanganannya**:
    *   **Error**: `mysql_mcp_server` tidak merespons atau *tool call* gagal.
        *   **Penanganan**: *Retry*. Jika gagal, set `technical_error_details` ("MySQL MCP Server communication error"), `error_message_for_user` ("Gagal menghubungi database."), alihkan ke `generate_error_response`.
    *   **Error**: Salah satu atau lebih query SQL gagal dieksekusi oleh database (syntax error, tabel tidak ada, dll.).
        *   **Penanganan**:
            *   Catat error di `query_execution_errors`.
            *   Jika query penting gagal, set `query_execution_status` ke `'total_failure'` atau `'partial_failure'`.
            *   Jika query opsional gagal, mungkin bisa dilanjutkan dengan `status = 'partial_failure'`.
            *   Alihkan ke `generate_error_response` jika kegagalan bersifat kritis, dengan pesan yang sesuai (misalnya, "Terjadi kesalahan saat mengambil data dari database.").
    *   **Error**: Query mengembalikan data yang terlalu besar (jika ada batasan `max_rows` di MCP Server).
        *   **Penanganan**: `mysql_mcp_server` seharusnya menangani ini dan mengembalikan error atau data terpotong dengan peringatan. Node ini akan mencatat peringatan tersebut.
*   **Ketergantungan pada Node Sebelumnya**: `sql_queries_plan`, `raw_data_query_plan` dari `plan_execution`.

**3.5. Node 5: `validate_results`**
*   **Fungsi**: Memvalidasi kualitas data dan konsistensi hasil query.
*   **Input State (Full)**:
    *   Semua *key* dari output `execute_query`.
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"validate_results"`.
    2.  Mengambil `financial_calculations`, `raw_query_results`, dan `validation_rules_for_results` dari *state*.
    3.  Melakukan validasi berdasarkan `validation_rules_for_results`:
        *   **Data Quality Checks**: Nilai masuk akal (misalnya, `TOTAL_SALES >= 0`).
        *   **Consistency Validation**: Kalkulasi silang (misalnya, jika `AVG_ORDER_VALUE` diminta, periksa `TOTAL_SALES / TRANSACTION_COUNT`).
        *   **Business Logic Validation**: Aturan bisnis spesifik.
    4.  Menghasilkan `validation_warnings` untuk anomali ringan.
    5.  Menentukan `validation_status` ('passed', 'passed_with_warnings', 'failed_critical').
    6.  Menghitung `quality_score`.
*   **Output State (Full)**:
    *   Semua *key* dari Input State.
    *   Ditambah/Dimodifikasi:
        *   `data_quality_checks: Dict[str, Any]`
        *   `validation_warnings: List[str]`
        *   `validation_status: str`
        *   `quality_score: int`
        *   `current_node_name: str`
*   **Potensi Error dan Penanganannya**:
    *   **Error**: Ditemukan error data kritis (misalnya, total penjualan negatif yang signifikan dan tidak bisa dijelaskan).
        *   **Penanganan**: Set `validation_status` ke `'failed_critical'`, `error_message_for_user` ("Hasil data tidak valid setelah diverifikasi."), alihkan ke `generate_error_response`.
    *   **Error**: Tidak ada hasil query (jika `financial_calculations` dan `raw_query_results` kosong).
        *   **Penanganan**: Set `validation_status` ke `'failed_no_data'`, `error_message_for_user` ("Tidak ada data ditemukan untuk periode atau kriteria yang diminta."), alihkan ke `generate_error_response`.
*   **Ketergantungan pada Node Sebelumnya**: `financial_calculations`, `raw_query_results`, `validation_rules_for_results` dari `execute_query` dan `plan_execution`.

**3.6. Node 6: `replace_placeholders`**
*   **Fungsi**: Mengganti placeholder dengan nilai aktual dan memformat output final.
*   **Input State (Full)**:
    *   Semua *key* dari output `validate_results`.
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"replace_placeholders"`.
    2.  Mengambil `response_template`, `financial_calculations`, `placeholder_mapping`, `raw_query_results`, `validation_warnings` dari *state*.
    3.  **Interaksi dengan `placeholder_mcp_server`**:
        *   Memanggil tool `fill_placeholders`.
        *   **Request Payload**: `{ "response_template": state.response_template, "data_values": state.financial_calculations, "formatting_rules": state.placeholder_mapping }` (formatting_rules mungkin perlu di-transform dari `placeholder_mapping` yang ada di state).
        *   Mencatat pemanggilan ke `mcp_tool_call_history`.
    4.  Menerima `final_narrative` dari MCP Server.
    5.  Memformat `raw_query_results` menjadi `data_table_for_display` (mungkin menerapkan pemformatan angka dan tanggal).
    6.  Menyiapkan `executive_summary` (mungkin dari `financial_calculations` yang sudah diformat).
    7.  Menyiapkan `warnings_for_display` dari `validation_warnings`.
    8.  Set `workflow_status` menjadi `'completed'`.
*   **Output State (Full)**:
    *   Semua *key* dari Input State.
    *   Ditambah/Dimodifikasi:
        *   `final_narrative: str`
        *   `data_table_for_display: List[Dict[str, Any]]`
        *   `executive_summary: Dict[str, Any]`
        *   `warnings_for_display: List[str]`
        *   `mcp_tool_call_history` (diperbarui)
        *   `current_node_name: str`
        *   `workflow_status: str`
*   **Potensi Error dan Penanganannya**:
    *   **Error**: `placeholder_mcp_server` tidak merespons atau *tool call* gagal.
        *   **Penanganan**: *Retry*. Jika gagal, set `technical_error_details` ("Placeholder MCP Server communication error"), `error_message_for_user` ("Gagal memformat hasil akhir."), alihkan ke `generate_error_response`.
    *   **Error**: Placeholder tidak ditemukan di `data_values` atau aturan pemformatan tidak valid.
        *   **Penanganan**: `placeholder_mcp_server` idealnya menangani ini. Jika error sampai ke node ini, catat sebagai `technical_error_details`, coba hasilkan narasi seadanya (misalnya, tanpa placeholder yang gagal), atau alihkan ke `generate_error_response`.
*   **Ketergantungan pada Node Sebelumnya**: `response_template`, `financial_calculations`, `placeholder_mapping`, `raw_query_results`, `validation_warnings` dari node-node sebelumnya.

---

**4. Node Error: `generate_error_response`**
*   **Fungsi**: Menghasilkan respons error yang informatif untuk pengguna dan logging.
*   **Input State (Full)**:
    *   `user_query: str`
    *   `session_id: str`
    *   `conversation_history: List[Dict[str, str]]`
    *   `current_node_name: Optional[str]` (node tempat error terjadi)
    *   `error_message_for_user: Optional[str]`
    *   `technical_error_details: Optional[str]`
    *   `mcp_tool_call_history: List[MCPToolCallLog]`
*   **Proses yang Terjadi**:
    1.  Set `current_node_name` menjadi `"generate_error_response"`.
    2.  Membangun objek respons error standar berdasarkan input.
    3.  Memberikan saran umum jika memungkinkan (misalnya, "Coba sederhanakan pertanyaan Anda" atau "Periksa kembali periode waktu yang diminta").
    4.  Set `workflow_status` menjadi `'error'`.
*   **Output State (Final - untuk error)**:
    ```python
    class ErrorResponse(TypedDict):
        success: bool # selalu false
        error_source_node: Optional[str]
        user_message: str
        technical_details_for_log: Optional[str]
        session_id: str
        suggestions: Optional[List[str]]
    ```
    *Key-key ini akan menjadi output akhir dari graph jika terjadi error.*
*   **Potensi Error dan Penanganannya**: Idealnya, node ini tidak menghasilkan error. Jika ada, itu adalah error sistem internal yang parah.
*   **Ketergantungan pada Node Sebelumnya**: Dipicu oleh node mana pun yang mengalami error kritis. Membutuhkan `error_message_for_user` dan `technical_error_details` dari *state*.

---
