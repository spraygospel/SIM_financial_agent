

**Dokumen Perencanaan Tambahan 5: Strategi Penanganan Error dan Fallback (Lebih Detail)**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
2.  Filosofi Penanganan Error
3.  Kategori Error dan Skenario Spesifik
    3.1. Error Input Pengguna & Pemahaman Query (Node `understand_query`)
    3.2. Error Konsultasi Skema (Node `consult_schema` & `graphiti_mcp_server`)
    3.3. Error Perencanaan Eksekusi (Node `plan_execution`)
    3.4. Error Eksekusi Query SQL (Node `execute_query` & `mysql_mcp_server`)
    3.5. Error Validasi Hasil (Node `validate_results`)
    3.6. Error Pemformatan Output (Node `replace_placeholders` & `placeholder_mcp_server`)
    3.7. Error Komunikasi MCP Server Umum
    3.8. Error Infrastruktur & LLM
4.  Mekanisme Fallback Umum
5.  Komunikasi Error kepada Pengguna (Integrasi dengan Frontend)
6.  Pencatatan (Logging) Error
7.  Alur Kerja Error dalam LangGraph (Node `generate_error_response`)

---

**1. Pendahuluan**

Sistem AI Agent yang kompleks pasti akan menghadapi berbagai jenis error, mulai dari input pengguna yang tidak jelas hingga masalah teknis di backend. Dokumen ini menguraikan strategi komprehensif untuk mendeteksi, menangani, dan melakukan *fallback* dari error tersebut. Tujuannya adalah untuk menciptakan sistem yang tangguh (*resilient*), memberikan pengalaman pengguna yang baik meskipun terjadi masalah, dan menyediakan informasi yang cukup untuk debugging.

---

**2. Filosofi Penanganan Error**

*   **Graceful Degradation**: Jika terjadi error, sistem harus mencoba memberikan respons yang paling berguna semampu mungkin, daripada gagal total.
*   **Informative Feedback**: Pengguna harus diberi tahu tentang masalah dengan cara yang mudah dimengerti, beserta saran jika memungkinkan.
*   **Transparency (untuk Debugging)**: Error teknis harus dicatat dengan detail yang cukup untuk memudahkan identifikasi dan perbaikan.
*   **Prioritaskan Pengalaman Pengguna**: Hindari menampilkan pesan error teknis mentah kepada pengguna.
*   **Retryability**: Untuk error yang bersifat sementara (misalnya, masalah jaringan), implementasikan mekanisme *retry* otomatis dengan *backoff*.
*   **Fallback Cerdas**: Jika proses utama gagal, coba alternatif yang lebih sederhana atau lebih umum.

---

**3. Kategori Error dan Skenario Spesifik**

Berikut adalah rincian error yang mungkin terjadi di setiap tahapan/node, beserta strategi penanganannya:

**3.1. Error Input Pengguna & Pemahaman Query (Node `understand_query`)**
*   **Skenario Error**:
    *   Query pengguna terlalu ambigu atau tidak lengkap.
    *   Intent tidak dapat diklasifikasikan dengan percaya diri.
    *   Entitas penting (seperti periode waktu atau metrik) tidak dapat diekstrak.
    *   Bahasa tidak didukung (jika ada batasan).
*   **Strategi Penanganan/Fallback**:
    1.  **Minta Klarifikasi**: Jika LLM menandai ambiguitas tinggi, node akan mengembalikan status yang meminta frontend untuk memicu permintaan klarifikasi kepada pengguna.
        *   **`error_message_for_user`**: "Maaf, saya kurang mengerti maksud Anda. Bisakah Anda merumuskan pertanyaan dengan lebih spesifik? Misalnya, sebutkan metrik dan periode waktu yang jelas."
        *   **`technical_error_details`**: "NLU Confidence Low: Intent ambiguous, entities missing."
        *   **Alur**: Alihkan ke `generate_error_response` (atau mekanisme feedback langsung).
    2.  **Asumsi Default (Hati-hati)**: Untuk kasus minor (misalnya, periode waktu tidak ada, bisa diasumsikan "bulan ini" atau "tahun ini" dengan catatan), namun untuk MVP awal lebih baik minta klarifikasi.
    3.  **Saran Query**: Jika memungkinkan, LLM bisa memberikan contoh query yang lebih baik berdasarkan kata kunci yang terdeteksi.

**3.2. Error Konsultasi Skema (Node `consult_schema` & `graphiti_mcp_server`)**
*   **Skenario Error**:
    *   `graphiti_mcp_server` tidak responsif atau *tool call* gagal.
    *   Tidak ada tabel atau kolom relevan yang ditemukan di Graphiti untuk intent/entitas yang diberikan.
    *   Informasi skema yang dikembalikan ambigu atau tidak lengkap untuk merencanakan query.
    *   Graphiti *out-of-sync* dengan skema database aktual.
*   **Strategi Penanganan/Fallback**:
    1.  **Retry MCP Call**: Implementasikan *retry* dengan *backoff* untuk panggilan ke `graphiti_mcp_server`.
    2.  **Pesan Error ke Pengguna (Jika Kritis)**:
        *   **`error_message_for_user`**: "Saat ini saya kesulitan memahami struktur data yang relevan untuk permintaan Anda. Tim teknis sedang menanganinya."
        *   **`technical_error_details`**: "Graphiti MCP Error: [detail error dari MCP] / No relevant schema found for intent: [intent]."
        *   **Alur**: Alihkan ke `generate_error_response`.
    3.  **Peringatan (Jika Tidak Kritis)**: Jika beberapa informasi skema ditemukan tetapi tidak sepenuhnya ideal, catat di `schema_consultation_warnings` dan lanjutkan, namun tandai bahwa hasil mungkin tidak optimal.
    4.  **Fallback (Jika Tidak Ada Skema Sama Sekali)**: Untuk MVP, ini akan menjadi error kritis. Untuk pengembangan selanjutnya, bisa dipertimbangkan untuk mencoba "menebak" tabel/kolom berdasarkan nama entitas (berisiko tinggi).

**3.3. Error Perencanaan Eksekusi (Node `plan_execution`)**
*   **Skenario Error**:
    *   LLM gagal menghasilkan rencana SQL yang valid meskipun skema sudah ada.
    *   LLM menghasilkan query yang dianggap tidak aman (misalnya, terdeteksi pola SQL Injection sederhana, atau query tanpa `WHERE` clause pada tabel besar).
    *   Tidak ada kolom yang cocok untuk metrik yang diminta berdasarkan skema yang tersedia.
    *   Template respons yang dihasilkan LLM tidak memiliki placeholder yang sesuai dengan rencana SQL.
*   **Strategi Penanganan/Fallback**:
    1.  **Coba Sederhanakan Permintaan ke LLM**: Jika rencana awal gagal, coba minta LLM untuk membuat rencana yang lebih sederhana (misalnya, fokus pada satu metrik dulu).
    2.  **Validasi Keamanan Query Dasar**: Implementasikan pemeriksaan dasar pada query SQL yang dihasilkan (misalnya, tidak ada `DROP`, `DELETE`; `SELECT` harus punya `LIMIT` jika tidak ada agregasi kuat). Jika gagal, minta LLM merevisi.
    3.  **Pesan Error ke Pengguna**:
        *   **`error_message_for_user`**: "Saya tidak dapat membuat rencana yang valid untuk mengambil data sesuai permintaan Anda. Mungkin permintaan terlalu kompleks atau data yang dibutuhkan tidak tersedia."
        *   **`technical_error_details`**: "LLM SQL Planning Failed: [alasan, misal 'unsafe query generated' atau 'metric not mappable to schema']."
        *   **Alur**: Alihkan ke `generate_error_response`.

**3.4. Error Eksekusi Query SQL (Node `execute_query` & `mysql_mcp_server`)**
*   **Skenario Error**:
    *   `mysql_mcp_server` tidak responsif atau *tool call* gagal.
    *   Database menolak koneksi.
    *   Query SQL mengandung *syntax error*.
    *   Tabel atau kolom yang dirujuk dalam query tidak ada di database (mismatch dengan Graphiti).
    *   Timeout saat eksekusi query yang terlalu lama.
    *   Data tidak ditemukan (query valid, tapi hasilnya kosong).
*   **Strategi Penanganan/Fallback**:
    1.  **Retry MCP Call**: Untuk error koneksi ke `mysql_mcp_server`.
    2.  **Tangkap Error Spesifik dari Database**: `mysql_mcp_server` harus mengembalikan kode error database yang jelas.
    3.  **Untuk `syntax error` atau `table/column not found`**: Ini mengindikasikan masalah pada `plan_execution` atau ketidaksesuaian Graphiti.
        *   **`technical_error_details`**: "SQL Execution Error: [pesan error SQL]. Query: [SQL query]."
        *   **`error_message_for_user`**: "Terjadi kesalahan saat menjalankan query ke database. Tim kami sedang memeriksanya."
        *   **Alur**: Alihkan ke `generate_error_response`.
    4.  **Untuk `timeout`**:
        *   Coba eksekusi query yang lebih sederhana (misalnya, dengan `LIMIT` yang lebih kecil atau periode waktu yang lebih pendek) jika memungkinkan, atau batalkan.
        *   **`error_message_for_user`**: "Permintaan Anda membutuhkan waktu terlalu lama untuk diproses. Coba persempit periode waktu atau kriteria Anda."
        *   **Alur**: Alihkan ke `generate_error_response`.
    5.  **Untuk `Data tidak ditemukan`**: Ini bukan error teknis, tapi perlu ditangani.
        *   Set `financial_calculations` dan `raw_query_results` menjadi kosong/null.
        *   Lanjutkan ke `validate_results` yang akan menangani ini.

**3.5. Error Validasi Hasil (Node `validate_results`)**
*   **Skenario Error**:
    *   Hasil kalkulasi tidak konsisten (misalnya, total penjualan negatif signifikan).
    *   Tidak ada data yang ditemukan (diteruskan dari `execute_query`).
    *   Data melanggar aturan bisnis penting.
*   **Strategi Penanganan/Fallback**:
    1.  **Error Kritis**: Jika validasi menemukan masalah serius yang membuat data tidak dapat dipercaya (misalnya, `TOTAL_SALES < 0` yang besar).
        *   Set `validation_status` ke `'failed_critical'`.
        *   **`error_message_for_user`**: "Hasil data yang saya dapatkan tampak tidak valid setelah diverifikasi. Silakan coba lagi nanti atau hubungi support jika masalah berlanjut."
        *   **`technical_error_details`**: "Critical Data Validation Failed: [detail aturan yang dilanggar]."
        *   **Alur**: Alihkan ke `generate_error_response`.
    2.  **Tidak Ada Data Ditemukan**:
        *   Set `validation_status` ke `'failed_no_data'`.
        *   **`error_message_for_user`**: "Saya tidak menemukan data untuk periode atau kriteria yang Anda minta."
        *   **Alur**: Alihkan ke `generate_error_response`.
    3.  **Peringatan**: Jika ada anomali minor (misalnya, beberapa transaksi kecil di bawah batas tertentu).
        *   Set `validation_status` ke `'passed_with_warnings'`.
        *   Tambahkan ke `validation_warnings`.
        *   Lanjutkan ke node berikutnya.

**3.6. Error Pemformatan Output (Node `replace_placeholders` & `placeholder_mcp_server`)**
*   **Skenario Error**:
    *   `placeholder_mcp_server` tidak responsif atau *tool call* gagal.
    *   Placeholder dalam template tidak ditemukan dalam data yang disediakan (`financial_calculations`).
    *   Aturan pemformatan tidak valid.
*   **Strategi Penanganan/Fallback**:
    1.  **Retry MCP Call**: Untuk error koneksi ke `placeholder_mcp_server`.
    2.  **Tangani Placeholder Hilang**: Jika placeholder penting hilang, ini mungkin error kritis.
        *   **`error_message_for_user`**: "Terjadi kesalahan saat menyiapkan laporan akhir."
        *   **`technical_error_details`**: "Placeholder Formatting Error: Placeholder '{placeholder_name}' not found in data_values."
        *   **Alur**: Alihkan ke `generate_error_response`.
    3.  **Gunakan Pemformatan Default**: Jika aturan pemformatan spesifik gagal, `placeholder_mcp_server` bisa mencoba menggunakan pemformatan default untuk tipe data tersebut.
    4.  **Keluarkan Narasi Seadanya**: Jika hanya beberapa placeholder minor yang gagal diformat, mungkin bisa menampilkan narasi dengan placeholder yang tidak terisi atau pesan error di tempat placeholder tersebut.

**3.7. Error Komunikasi MCP Server Umum**
*   **Skenario Error**: Semua MCP Server (Graphiti, MySQL, Placeholder) mungkin mengalami:
    *   Server tidak berjalan atau tidak dapat dijangkau.
    *   Masalah jaringan.
    *   Error internal di dalam MCP Server itu sendiri.
*   **Strategi Penanganan/Fallback**:
    1.  **Retry Terstandardisasi**: Semua MCP Client (di dalam node LangGraph) harus mengimplementasikan mekanisme *retry* (misalnya, 3 kali dengan *exponential backoff*).
    2.  **Circuit Breaker (Lanjutan)**: Untuk mencegah panggilan berulang ke server yang sedang bermasalah.
    3.  **Pesan Error Generik tapi Informatif**:
        *   **`error_message_for_user`**: "Maaf, saya tidak dapat terhubung ke salah satu layanan pendukung saat ini. Silakan coba lagi beberapa saat."
        *   **`technical_error_details`**: "MCP Communication Error: Server [nama_server_mcp] at [url_mcp] failed after [N] retries. Error: [pesan_error_koneksi]."
        *   **Alur**: Alihkan ke `generate_error_response`.

**3.8. Error Infrastruktur & LLM**
*   **Skenario Error**:
    *   LLM API (DeepSeek) tidak responsif, mengembalikan error rate limit, atau error API lainnya.
    *   LangGraph mengalami error internal.
    *   FastAPI backend mengalami error.
*   **Strategi Penanganan/Fallback**:
    1.  **Retry untuk LLM API Call**: Dengan *backoff*, perhatikan *rate limit*.
    2.  **Error LLM Kritis**: Jika LLM terus gagal.
        *   **`error_message_for_user`**: "Maaf, ada gangguan pada layanan AI kami. Silakan coba lagi nanti."
        *   **`technical_error_details`**: "LLM API Error: [kode_error_api] - [pesan_error_api]."
        *   **Alur**: Alihkan ke `generate_error_response`.
    3.  **Error LangGraph/FastAPI**: Ini adalah error sistem.
        *   **`error_message_for_user`**: "Maaf, terjadi kesalahan teknis pada sistem kami. Tim kami telah diberitahu."
        *   **`technical_error_details`**: Log stack trace lengkap di sisi server.
        *   **Alur**: Alihkan ke `generate_error_response`.

---

**4. Mekanisme Fallback Umum**

*   **Query yang Lebih Sederhana**: Jika query kompleks gagal (baik saat perencanaan atau eksekusi), sistem dapat secara otomatis atau dengan bantuan LLM mencoba merumuskan ulang query menjadi versi yang lebih sederhana. Misalnya, jika analisis tren gagal, coba ambil total saja.
*   **Periode Waktu yang Lebih Luas/Default**: Jika data untuk periode spesifik tidak ada, tawarkan untuk menampilkan data untuk periode default (misalnya, bulan lalu) atau periode yang lebih luas.
*   **Pesan "Tidak Dapat Memproses Permintaan Spesifik"**: Jika semua *fallback* gagal, berikan pesan yang jelas bahwa permintaan spesifik tersebut tidak dapat diproses, daripada memberikan hasil yang salah atau tidak relevan.

---

**5. Komunikasi Error kepada Pengguna (Integrasi dengan Frontend)**

*   Node `generate_error_response` akan menyiapkan `error_message_for_user` dan `suggestions`.
*   Frontend (`AIAgentDashboard`) akan menampilkan pesan ini dengan cara yang ramah.
*   Komponen `FallbackTracker` di frontend akan idealnya menampilkan beberapa informasi tentang upaya *fallback* yang dilakukan agent (jika relevan dan tidak terlalu teknis). Misalnya, "Mencoba mengambil data Q1 2023 karena data Januari 2023 tidak ditemukan..." (jika *fallback* ini diimplementasikan).

---

**6. Pencatatan (Logging) Error**

*   Semua error, baik yang ditangani maupun yang tidak, harus dicatat (log) di sisi server (FastAPI/LangGraph).
*   Log harus mencakup:
    *   Timestamp.
    *   `session_id`.
    *   `user_query` (hati-hati dengan data sensitif).
    *   Node tempat error terjadi (`current_node_name`).
    *   `technical_error_details` (termasuk stack trace jika ada).
    *   Pesan error dari layanan eksternal (LLM, MCP Server, Database).
    *   Riwayat pemanggilan `mcp_tool_call_history` hingga titik error.
*   Gunakan level log yang sesuai (ERROR, CRITICAL, WARNING).
*   Pertimbangkan sistem *monitoring* dan *alerting* terpusat untuk error kritis.

---

**7. Alur Kerja Error dalam LangGraph (Node `generate_error_response`)**

*   Ketika sebuah node mengalami error yang tidak dapat ditangani secara lokal atau setelah *retry* gagal, node tersebut akan memperbarui `AgentState` dengan `error_message_for_user` dan `technical_error_details`.
*   Kemudian, alur kerja LangGraph akan diarahkan (melalui *conditional edge*) ke node `generate_error_response`.
*   Node `generate_error_response` akan menggunakan informasi error dari `AgentState` untuk membuat objek respons error final yang akan dikirim kembali ke Backend API dan kemudian ke Frontend.
*   `workflow_status` di `AgentState` akan diubah menjadi `'error'`.

---
