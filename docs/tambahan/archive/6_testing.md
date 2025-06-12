Baik, kita akan membuat **Dokumen Rencana Testing dan Kasus Uji (Test Plan and Test Cases)**.

Dokumen ini akan mendefinisikan pendekatan pengujian untuk memastikan kualitas, fungsionalitas, dan keandalan MVP AI Agent.

---

**Dokumen Perencanaan Tambahan 6: Rencana Testing dan Kasus Uji**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
    1.1. Tujuan Pengujian
    1.2. Lingkup Pengujian MVP
2.  Strategi Pengujian
    2.1. Level Pengujian
    2.2. Jenis Pengujian
3.  Lingkungan Pengujian
4.  Tools Pengujian
5.  Kriteria Keberhasilan Pengujian
6.  Rincian Kasus Uji
    6.1. Unit Tests
        6.1.1. Node LangGraph
        6.1.2. MCP Server Tools
        6.1.3. Fungsi Utilitas Backend
    6.2. Integration Tests
        6.2.1. Alur Kerja LangGraph (End-to-End Internal)
        6.2.2. Frontend <-> Backend API
        6.2.3. LangGraph Node <-> MCP Server
    6.3. End-to-End (E2E) System Tests
        6.3.1. Skenario Pengguna Utama
        6.3.2. Skenario Penanganan Error dan Fallback
        6.3.3. Skenario Data Variatif
    6.4. User Acceptance Tests (UAT)
7.  Pelaporan Hasil Pengujian
8.  Jadwal Pengujian (Placeholder)

---

**1. Pendahuluan**

**1.1. Tujuan Pengujian**
Tujuan utama dari pengujian ini adalah untuk:
*   Memastikan semua fungsionalitas inti AI Agent MVP berjalan sesuai dengan spesifikasi.
*   Mengidentifikasi dan memperbaiki *bug* atau masalah sebelum rilis.
*   Memvalidasi akurasi pemrosesan query dan hasil yang diberikan.
*   Memastikan sistem dapat menangani error dan skenario *fallback* dengan baik.
*   Memverifikasi bahwa pengalaman pengguna melalui frontend berjalan lancar.

**1.2. Lingkup Pengujian MVP**
Pengujian akan difokuskan pada fitur-fitur yang didefinisikan dalam lingkup MVP, termasuk:
*   Pemahaman query natural language untuk analisis penjualan dasar.
*   Konsultasi skema ke Graphiti melalui MCP Server.
*   Perencanaan dan eksekusi query SQL ke SQLite (via MCP Server) berdasarkan data sampel.
*   Validasi hasil dan penggantian placeholder.
*   Tampilan hasil (narasi & tabel) di frontend.
*   Penanganan error dasar.

---

**2. Strategi Pengujian**

**2.1. Level Pengujian**
Pengujian akan dilakukan pada beberapa level:
*   **Unit Testing**: Menguji komponen terkecil secara terisolasi (fungsi, method, class).
*   **Integration Testing**: Menguji interaksi antar komponen/modul (misalnya, node LangGraph dengan MCP Server).
*   **System Testing (End-to-End)**: Menguji sistem secara keseluruhan dari input pengguna hingga output.
*   **User Acceptance Testing (UAT)**: Pengujian oleh perwakilan pengguna untuk memastikan sistem memenuhi kebutuhan.

**2.2. Jenis Pengujian**
*   **Functional Testing**: Memastikan fungsionalitas bekerja sesuai yang diharapkan.
*   **Error Handling Testing**: Menguji bagaimana sistem menangani kondisi error.
*   **Data Validation Testing**: Memastikan validasi data berjalan benar.
*   **(Minimal untuk MVP) Performance Testing**: Gambaran kasar waktu respons untuk query umum.
*   **(Minimal untuk MVP) Usability Testing**: Feedback awal terkait kemudahan penggunaan frontend.

---

**3. Lingkungan Pengujian**

*   **Lingkungan Development**: Digunakan oleh developer untuk unit testing dan debugging awal.
*   **Lingkungan Staging/Testing**: Replika lingkungan produksi (sebisa mungkin) untuk integration testing dan E2E testing. Untuk MVP, ini bisa berjalan di satu mesin dengan semua service (FastAPI, MCP Servers, SQLite, Graphiti) berjalan.
*   **Database Sampel**: SQLite in-memory akan diinisialisasi dengan skema dan data sampel yang konsisten untuk setiap pengujian E2E. Graphiti juga akan diisi dengan metadata skema yang sesuai.

---

**4. Tools Pengujian**

*   **Python**:
    *   `pytest`: Framework untuk unit dan integration testing.
    *   `unittest.mock`: Untuk mocking dependensi eksternal (seperti LLM API call atau MCP Server selama unit test node).
*   **FastAPI**:
    *   `TestClient`: Untuk integration testing endpoint API.
*   **JavaScript (React)**:
    *   `Jest` & `React Testing Library`: Untuk unit dan integration testing komponen frontend.
*   **Manual Testing**: Untuk E2E testing skenario kompleks dan UAT.
*   **Postman/Insomnia**: Untuk pengujian API backend secara manual.
*   **LangSmith (jika digunakan)**: Untuk memantau dan men-debug alur kerja LangGraph.

---

**5. Kriteria Keberhasilan Pengujian**

*   **Unit Tests**: Minimal 80% *code coverage* untuk logika inti. Semua tes kritis lulus.
*   **Integration Tests**: Semua skenario integrasi utama lulus. Tidak ada *breaking changes* pada antarmuka antar komponen.
*   **E2E Tests**: Semua skenario pengguna utama (kasus uji E2E) berhasil diselesaikan dengan output yang akurat dan sesuai ekspektasi. Penanganan error berfungsi.
*   **UAT**: Sistem diterima oleh perwakilan pengguna, memenuhi kebutuhan dasar yang didefinisikan untuk MVP.
*   Jumlah *bug* kritis/mayor yang ditemukan dan belum diperbaiki: 0.

---

**6. Rincian Kasus Uji**

**6.1. Unit Tests**

   **6.1.1. Node LangGraph**
    *   **Node `understand_query`**:
        *   Input: Berbagai contoh `user_query`.
        *   Output yang Diharapkan: `intent`, `entities_mentioned`, `time_period`, `requested_metrics`, `query_complexity` yang benar.
        *   Mock: LLM call.
    *   **Node `consult_schema`**:
        *   Input: `intent`, `entities_mentioned`.
        *   Output yang Diharapkan: `relevant_tables`, `table_relationships`, dll., yang sesuai.
        *   Mock: Panggilan ke `graphiti_mcp_server.get_relevant_schema_info`.
    *   **Node `plan_execution`**:
        *   Input: `intent`, `entities_mentioned`, `time_period`, informasi skema.
        *   Output yang Diharapkan: `sql_queries_plan`, `response_template` yang valid.
        *   Mock: LLM call.
    *   **Node `execute_query`**:
        *   Input: `sql_queries_plan`.
        *   Output yang Diharapkan: `financial_calculations`, `raw_query_results` yang benar.
        *   Mock: Panggilan ke `mysql_mcp_server.execute_sql_query`.
    *   **Node `validate_results`**:
        *   Input: `financial_calculations`, `raw_query_results`.
        *   Output yang Diharapkan: `validation_status`, `validation_warnings` yang sesuai.
    *   **Node `replace_placeholders`**:
        *   Input: `response_template`, `financial_calculations`, `placeholder_mapping`.
        *   Output yang Diharapkan: `final_narrative` yang terisi dengan benar.
        *   Mock: Panggilan ke `placeholder_mcp_server.fill_placeholders`.

   **6.1.2. MCP Server Tools**
    *   **`graphiti_mcp_server.get_relevant_schema_info`**:
        *   Input: `intent`, `entities`.
        *   Output yang Diharapkan: Struktur skema yang relevan.
        *   Mock: Graphiti KG (atau gunakan instance Graphiti dengan data tes).
    *   **`mysql_mcp_server.execute_sql_query`**:
        *   Input: `sql_queries`.
        *   Output yang Diharapkan: Hasil eksekusi SQL.
        *   Mock: Koneksi database (atau gunakan SQLite in-memory). Test case untuk query valid, query invalid, query tanpa hasil.
    *   **`placeholder_mcp_server.fill_placeholders`**:
        *   Input: `template`, `data_values`, `formatting_rules`.
        *   Output yang Diharapkan: String yang terisi dan terformat.

   **6.1.3. Fungsi Utilitas Backend**
    *   Tes untuk fungsi parsing, formatting, validasi, dll.

**6.2. Integration Tests**

   **6.2.1. Alur Kerja LangGraph (End-to-End Internal)**
    *   Input: `AgentState` awal dengan `user_query`.
    *   Output yang Diharapkan: `AgentState` akhir dengan `final_narrative`, `data_table_for_display`.
    *   Mock: Hanya LLM call di node `understand_query` dan `plan_execution`. MCP Server dan database sampel digunakan secara nyata (atau di-mock di level MCP Client jika sulit).
    *   Skenario: Query penjualan sederhana, query dengan filter tanggal.

   **6.2.2. Frontend <-> Backend API**
    *   Menggunakan `TestClient` FastAPI.
    *   Kirim request ke `POST /api/v1/query`.
    *   Verifikasi struktur dan konten response (sukses & error).
    *   (Jika ada SSE) Verifikasi aliran event pembaruan status.
    *   Mock: LangGraph Workflow di backend.

   **6.2.3. LangGraph Node <-> MCP Server**
    *   Tes spesifik untuk interaksi antara node LangGraph (bertindak sebagai MCP Client) dan MCP Server yang sesuai.
    *   Contoh: Node `consult_schema` memanggil `graphiti_mcp_server`.
    *   Verifikasi request yang dikirim dan response yang diterima sesuai spesifikasi MCP Server.

**6.3. End-to-End (E2E) System Tests**
*   Dilakukan secara manual atau dengan skrip automasi (jika memungkinkan).
*   Melibatkan interaksi dari Frontend hingga Database dan kembali.
*   Database sampel dan Graphiti diinisialisasi dengan data yang diketahui.

   **6.3.1. Skenario Pengguna Utama**
    *   **TC_E2E_001**: Sales Januari 2023
        *   Input Query: "Tunjukkan data sales bulan Januari 2023"
        *   Output yang Diharapkan: Narasi dengan total penjualan dan jumlah transaksi Januari 2023, tabel data transaksi Januari 2023. Akurasi angka diverifikasi terhadap data sampel.
    *   **TC_E2E_002**: Customer Belum Bayar
        *   Input Query: "Siapa saja customer yang belum lunas membayar invoice mereka?"
        *   Output yang Diharapkan: Narasi ringkasan, tabel customer dengan invoice outstanding dan due date.
    *   **TC_E2E_003**: Query tanpa filter waktu (misalnya, "Total sales sepanjang masa")
        *   Output yang Diharapkan: Sesuai dengan data total di sampel.
    *   **TC_E2E_004**: Query dengan metrik berbeda (misalnya, "Rata-rata nilai transaksi Februari 2023")
        *   Output yang Diharapkan: Sesuai dengan perhitungan rata-rata.

   **6.3.2. Skenario Penanganan Error dan Fallback**
    *   **TC_E2E_ERR_001**: Query Ambigu
        *   Input Query: "sales?"
        *   Output yang Diharapkan: Pesan meminta klarifikasi.
    *   **TC_E2E_ERR_002**: Data Tidak Ditemukan
        *   Input Query: "Tunjukkan sales di planet Mars tahun 1800"
        *   Output yang Diharapkan: Pesan "Tidak ada data ditemukan...".
    *   **TC_E2E_ERR_003**: Simulasi MCP Server Down (salah satu)
        *   Input Query: Query valid.
        *   Output yang Diharapkan: Pesan error yang sesuai ("Tidak dapat terhubung ke layanan...").
    *   **TC_E2E_ERR_004**: Query menghasilkan data tidak valid (disimulasikan dengan data sampel yang 'rusak')
        *   Input Query: Query yang menargetkan data 'rusak'.
        *   Output yang Diharapkan: Pesan "Hasil data tidak valid..." atau peringatan dari `validate_results`.

   **6.3.3. Skenario Data Variatif**
    *   **TC_E2E_DATA_001**: Query pada periode tanpa transaksi.
        *   Output yang Diharapkan: Total penjualan 0, jumlah transaksi 0.
    *   **TC_E2E_DATA_002**: Query yang menghasilkan banyak baris data mentah (uji tampilan tabel).
    *   **TC_E2E_DATA_003**: Query dengan karakter khusus atau bahasa non-Inggris minor (jika relevan).

**6.4. User Acceptance Tests (UAT)**
*   Dilakukan oleh perwakilan *product owner* atau pengguna akhir.
*   Kasus uji akan mirip dengan E2E, tetapi fokus pada apakah sistem memenuhi kebutuhan bisnis dan mudah digunakan.
*   Contoh Kriteria UAT:
    *   Apakah agent dapat menjawab pertanyaan umum tentang sales dengan akurat?
    *   Apakah informasi yang ditampilkan mudah dimengerti?
    *   Apakah waktu respons agent dapat diterima?
    *   Apakah sistem menangani pertanyaan yang tidak jelas dengan baik?

---

**7. Pelaporan Hasil Pengujian**

*   Setiap siklus pengujian akan menghasilkan laporan yang berisi:
    *   Ringkasan hasil (jumlah tes dijalankan, lulus, gagal).
    *   Daftar *bug* yang ditemukan (beserta prioritas dan tingkat keparahan).
    *   Status perbaikan *bug*.
    *   Rekomendasi (jika ada).
*   Gunakan *issue tracker* (seperti Jira atau GitHub Issues) untuk melacak *bug*.

---

**8. Jadwal Pengujian (Placeholder)**

*   Unit testing: Berkelanjutan selama development sprint.
*   Integration testing: Dilakukan setelah komponen-komponen utama selesai dan sebelum E2E.
*   E2E testing: Dilakukan dalam siklus tersendiri menjelang akhir sprint atau rilis.
*   UAT: Dilakukan sebelum rilis MVP.

---
