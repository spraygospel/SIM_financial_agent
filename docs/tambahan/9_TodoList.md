### **Dokumen Perencanaan: To-do List - Pembangunan Komponen Database (v1.2)**

**Versi:** 1.2
**Status:** In Progress

**Filosofi:** Setiap komponen fondasi data harus dibangun dan divalidasi secara terpisah sebelum diintegrasikan. Pengujian di setiap langkah adalah kunci untuk memastikan keandalan data, yang merupakan dasar dari seluruh sistem AI Agent.

---

### **Fase 1: Penyiapan dan Validasi Database Sumber (MySQL)**

**Tujuan:** Memastikan database `sim_testgeluran` siap dengan skema yang benar dan berisi data sampel yang relevan untuk pengujian.

*   **1.1. Finalisasi dan Validasi Model ORM**
    *   **Aktivitas:** Melakukan tinjauan mendalam pada semua file model ORM (`orm_*.py`) untuk memastikan kesesuaian 100% dengan skema fisik yang diinginkan.
    *   **Detail:**
        *   a. Verifikasi setiap `Column` (tipe data, `nullable`, `primary_key`) di `orm_*.py` terhadap definisi di `schema_export.txt`.
        *   b. Periksa kembali definisi `relationship()` antar model. Pastikan `foreign_keys`, `back_populates`, dan nama relasinya logis dan konsisten.
    *   **File yang Diubah/Divalidasi:** `backend/mcp_servers/mysql_server/db_models/orm_*.py`.

*   **1.2. Pembuatan Data Sampel Berbasis Skenario**
    *   **Aktivitas:** Membuat file `data.sql` yang secara strategis dirancang untuk menguji fungsionalitas inti AI agent.
    *   **Detail:** Data sampel **wajib** mencakup:
        *   Customer dengan piutang yang sudah jatuh tempo (`arbook.DueDate` < hari ini).
        *   Customer dengan piutang yang belum jatuh tempo.
        *   Customer yang sudah lunas (`arbook.PaymentValueLocal` >= `arbook.DocValueLocal`).
        *   Beberapa transaksi untuk satu `mastercustomer`.
        *   Data dari setidaknya dua periode/bulan yang berbeda untuk menguji filter tanggal.
        *   Data yang akan memerlukan `JOIN` untuk menjawab query (misalnya, `arbook` yang memiliki `CustomerCode` yang ada di `mastercustomer`).
    *   **File yang Dibuat:** `data_samples/data.sql`.

*   **1.3. Implementasi Skrip Inisialisasi Database Berbasis ORM**
    *   **Aktivitas:** Membuat skrip Python yang mengotomatiskan pembuatan skema dan pengisian data, menggunakan ORM sebagai satu-satunya sumber kebenaran untuk struktur.
    *   **Detail:**
        *   a. Skrip membaca `settings` dari `backend.app.core.config` untuk koneksi.
        *   b. Skrip membuat *engine* SQLAlchemy.
        *   c. **(Penting)** Skrip menjalankan `Base.metadata.create_all(engine)`. Ini akan membuat semua tabel di database MySQL **berdasarkan definisi di file `orm_*.py`**, bukan dari `schema.sql`.
        *   d. Setelah skema dibuat, skrip membaca dan mengeksekusi perintah `INSERT` dari `data_samples/data.sql`.
    *   **File yang Dibuat:** `scripts/initialize_db_mysql.py`.

*   **1.4. Pengujian Fase 1: Validasi Database MySQL**
    *   **Aktivitas:** Menjalankan pengujian untuk memverifikasi bahwa database operasional telah berhasil disiapkan.
    *   **Langkah Pengujian:**
        *   a. Jalankan skrip `python scripts/initialize_db_mysql.py`. Pastikan tidak ada error.
        *   b. Gunakan *database client* (DBeaver, MySQL Workbench) untuk terhubung ke database `sim_testgeluran`.
        *   c. **Verifikasi Skema:** Pastikan semua tabel dari `orm_*.py` telah dibuat, dan periksa tipe data beberapa kolom kunci secara acak untuk memastikan kesesuaian.
        *   d. **Verifikasi Data:** Jalankan `SELECT COUNT(*) FROM arbook;` dan `SELECT * FROM mastercustomer LIMIT 5;`. Pastikan data sampel telah terisi dengan benar.
        *   e. **Kriteria Sukses:** Database MySQL siap digunakan, strukturnya sinkron dengan kode ORM, dan berisi data yang memadai untuk pengujian.

---

### **Fase 2: Pembangunan dan Validasi Knowledge Graph (Neo4j)**

**Tujuan:** Mengubah skema MySQL yang sudah divalidasi menjadi *knowledge graph* yang kaya makna dan memastikan hasilnya akurat.

*   **2.1. Peninjauan Skrip Sinkronisasi dan Pemetaan Semantik**
    *   **Aktivitas:** Memastikan skrip `sync_mysql_to_graphiti.py` siap untuk dijalankan dan pemetaan semantik sudah benar.
    *   **Detail:**
        *   a. Tinjau kembali `graphiti_semantic_mapping.json` untuk beberapa tabel kunci (`arbook`, `mastercustomer`, `salesorderh`). Pastikan `purpose`, `classification`, dan `relationships` sudah logis.
        *   b. Tinjau skrip `sync_mysql_to_graphiti.py` untuk memastikan ia membaca file pemetaan dengan benar dan menghasilkan query Cypher yang tepat.
    *   **File yang Divalidasi:** `scripts/sync_mysql_to_graphiti.py`, `data_samples/graphiti_semantic_mapping.json`.

*   **2.2. Eksekusi Sinkronisasi Skema ke Neo4j**
    *   **Aktivitas:** Menjalankan skrip untuk mempopulasi Neo4j.
    *   **Langkah Eksekusi:**
        *   a. Pastikan Fase 1 telah selesai dan layanan Neo4j sedang berjalan.
        *   b. Jalankan `python scripts/sync_mysql_to_graphiti.py`. Pastikan skrip berjalan tanpa error.

*   **2.3. Pengujian Fase 2: Validasi Mendalam Knowledge Graph**
    *   **Aktivitas:** Menggunakan Neo4j Browser untuk memverifikasi integritas dan kebenaran *knowledge graph* yang dihasilkan.
    *   **Langkah Pengujian:**
        *   a. **Uji Keberadaan Node:** Jalankan `MATCH (n:DatabaseTable) RETURN count(n) as table_count` dan `MATCH (n:DatabaseColumn) RETURN count(n) as column_count`.
        *   b. **Uji Atribut Semantik:** Jalankan `MATCH (t:DatabaseTable {table_name: 'mastercustomer'}) RETURN t.purpose, t.business_category`.
        *   c. **Uji Relasi `:HAS_COLUMN`:** Jalankan `MATCH (t:DatabaseTable {table_name: 'arbook'})-[:HAS_COLUMN]->(c:DatabaseColumn) RETURN c.column_name, c.classification`.
        *   d. **Uji Relasi `:REFERENCES` (Krusial):** Jalankan `MATCH (c1:DatabaseColumn {table_name_prop: 'arbook', column_name: 'CustomerCode'})-[r:REFERENCES]->(c2:DatabaseColumn) RETURN c1.table_name_prop as from_table, c2.column_name as to_column, c2.table_name_prop as to_table`.
        *   e. **Kriteria Sukses:** Hasil dari semua query Cypher di atas sesuai dengan yang diharapkan dari pemetaan semantik, terutama relasi antar tabel.

---

### **Fase 3: Perencanaan Evolusi Skema**

**Tujuan:** Mempersiapkan proyek untuk perubahan skema di masa depan agar tidak perlu melakukan perubahan manual yang berisiko.

*   **3.1. Inisialisasi dan Konfigurasi Alembic**
    *   **Aktivitas:** Mengintegrasikan Alembic sebagai alat manajemen migrasi skema database MySQL.
    *   **Detail:**
        *   a. Install Alembic (`pip install alembic`).
        *   b. Jalankan `alembic init` di `backend/mcp_servers/mysql_server/` untuk membuat struktur direktori Alembic.
        *   c. Konfigurasi file `alembic.ini` untuk menunjuk ke URL database dari `config.py`.
        *   d. Modifikasi `alembic/env.py` agar ia mengimpor `Base` dari `db_models` dan menyetel `target_metadata = Base.metadata`.
    *   **File yang Dibuat/Diubah:** `backend/mcp_servers/mysql_server/alembic.ini`, `backend/mcp_servers/mysql_server/alembic/env.py`.

*   **3.2. Pengujian Fase 3: Validasi Konfigurasi Alembic**
    *   **Aktivitas:** Memastikan Alembic dapat mendeteksi model ORM kita dan menghasilkan skrip migrasi.
    *   **Langkah Pengujian:**
        *   a. Hapus database `sim_testgeluran` (jika memungkinkan di lingkungan dev) atau gunakan database tes kosong.
        *   b. Jalankan `alembic revision --autogenerate -m "Initial schema from models"`.
        *   c. Periksa file migrasi yang baru dibuat di `alembic/versions/`. Pastikan isinya adalah serangkaian perintah `op.create_table()` untuk semua model ORM kita.
        *   d. Jalankan `alembic upgrade head`.
        *   e. **Kriteria Sukses:** Database yang tadinya kosong sekarang memiliki semua tabel yang dibuat oleh Alembic. Ini membuktikan sistem migrasi kita siap untuk digunakan.

---


### **Dokumen Perencanaan: To-do List - Pembangunan Backend & AI Agent (v3.0 - Detail & Bertahap)**

**Versi:** 3.0
**Status:** Not Started

**Filosofi:** Mengikuti pendekatan **"Kerangka Berjalan"** secara ketat. Kita akan membangun pipa data end-to-end yang paling sederhana terlebih dahulu, lalu secara bertahap mengganti komponen "dummy" dengan logika cerdas yang sesungguhnya. Setiap fase diakhiri dengan pengujian integrasi yang jelas.

---

### **Fase 1: Pembangunan "Pipa Lurus" (Konektivitas Dasar)**

**Tujuan:** Membuktikan bahwa semua komponen server (API, LangGraph, MCP Server) dapat dinyalakan dan saling berkomunikasi dalam alur yang paling sederhana. Ini adalah pemasangan semua "pipa" utama tanpa ada "filter" atau "katup cerdas" di dalamnya.

*   **1.1. Inisialisasi Proyek & Konfigurasi**
    *   **Aktivitas:** Buat struktur folder lengkap sesuai rencana. Buat file `config.py` untuk memuat semua variabel lingkungan dari `.env`.
    *   **File Dibuat:** Struktur folder, `backend/app/core/config.py`.

*   **1.2. Implementasi MCP Server "Ping"**
    *   **Aktivitas:** Buat `mysql_server` paling minimalis yang **tidak terhubung ke database**. Implementasikan satu tool `@mcp.tool()` bernama `ping()` yang hanya mengembalikan `{"status": "pong"}`.
    *   **File Dibuat:** `backend/mcp_servers/mysql_server/main.py`, `backend/mcp_servers/mysql_server/tools.py`.

*   **1.3. Implementasi API & Service "Pass-through"**
    *   **Aktivitas:**
        *   a. Buat endpoint `GET /api/v1/session/start` yang mengembalikan `session_id` dan daftar `suggested_queries` yang di-*hardcode*.
        *   b. Buat endpoint `POST /api/v1/query` yang hanya meneruskan permintaan ke `agent_service`.
    *   **File Dibuat:** `backend/app/main.py`, `backend/app/api/v1/endpoints/query.py`, `backend/app/services/agent_service.py`.

*   **1.4. Implementasi LangGraph "Pipa Lurus"**
    *   **Aktivitas:** Buat alur kerja LangGraph paling sederhana:
        *   a. `AgentState` hanya berisi `final_response: str`.
        *   b. Node `call_ping_tool`: Berperan sebagai MCP Client untuk memanggil tool `ping()` di `mysql_server`.
        *   c. Node `format_ping_response`: Mengambil hasil "pong" dan menyimpannya ke `final_response`.
    *   **File Dibuat:** `backend/app/schemas/agent_state.py` (versi minimal), `backend/app/langgraph_workflow/graph.py`, `nodes/call_ping_tool.py`, `nodes/format_ping_response.py`.

*   **1.5. Pengujian Fase 1: Uji Coba Pipa Lurus**
    *   **Aktivitas:** Jalankan server backend utama dan `mysql_server`.
    *   **Langkah Pengujian:**
        *   a. Panggil `GET /api/v1/session/start`, pastikan mendapatkan `session_id`.
        *   b. Panggil `POST /api/v1/query`.
        *   c. **Kriteria Sukses:** Respons yang diterima adalah JSON `{ "final_response": "pong" }`. Ini membuktikan seluruh kerangka komunikasi dari API hingga MCP server berfungsi.

---

### **Fase 2: Aktivasi "Mesin Data" & "Sistem Loker"**

**Tujuan:** Mengganti tool `ping()` dengan eksekusi query database nyata dan mengaktifkan sistem penyimpanan sementara menggunakan `DataHandle`.

*   **2.1. Implementasi Penuh `mysql_server`**
    *   **Aktivitas:** Ganti tool `ping()` dengan `execute_operation_plan`. Implementasikan `DynamicQueryBuilder` yang menerjemahkan `DatabaseOperationPlan` menjadi query ORM.
    *   **File Diubah/Dibuat:** `backend/mcp_servers/mysql_server/tools.py` (Revisi), `query_builder.py` (Baru).

*   **2.2. Implementasi `graphiti_server` untuk Penyimpanan Data**
    *   **Aktivitas:** Buat `graphiti_server` dengan tool `store_session_data` dan `retrieve_session_data`.
    *   **File Dibuat:** `backend/mcp_servers/graphiti_server/main.py`, `tools.py`.

*   **2.3. Upgrade LangGraph dengan Eksekusi & Penyimpanan Data**
    *   **Aktivitas:**
        *   a. Ganti node `call_ping_tool` menjadi `execute_and_store_data_node`.
        *   b. Node ini sekarang memanggil `execute_operation_plan` di `mysql_server` (dengan `DatabaseOperationPlan` yang masih di-*hardcode*).
        *   c. Kemudian, ia memanggil `store_session_data` di `graphiti_server` untuk menyimpan hasilnya.
        *   d. Perbarui `AgentState` untuk menyimpan `DataHandle` yang diterima.
    *   **File Diubah:** `backend/app/langgraph_workflow/nodes/` (file node baru), `graph.py`.

*   **2.4. Pengujian Fase 2: Uji Coba Aliran Data & Penyimpanan**
    *   **Aktivitas:** Jalankan semua server.
    *   **Langkah Pengujian:**
        *   a. Uji `mysql_server` dan `graphiti_server` secara terpisah dengan `mcp inspector`.
        *   b. Jalankan alur end-to-end melalui API `POST /api/v1/query`.
        *   c. **Kriteria Sukses:** Respons dari API berisi objek `DataHandle` yang valid. Verifikasi di Neo4j Browser bahwa node `:SessionData` yang sesuai telah dibuat.

---

### **Fase 3: Pemasangan "Otak Perencana"**

**Tujuan:** Memberikan kemampuan pada agent untuk secara dinamis membuat rencana query berdasarkan input pengguna dan `intent`.

*   **3.1. Implementasi Konsultasi Skema di `graphiti_server`**
    *   **Aktivitas:** Tambahkan tool `get_relevant_schema` ke `graphiti_server`.
    *   **File Diubah:** `backend/mcp_servers/graphiti_server/tools.py`.

*   **3.2. Implementasi Node Perencanaan Cerdas**
    *   **Aktivitas:** Buat node-node inti untuk proses berpikir agent.
        *   a. `router.py`: Memanggil LLM untuk menentukan `intent`.
        *   b. `consult_schema.py`: Memanggil `get_relevant_schema`.
        *   c. `plan_execution.py`: Memanggil LLM untuk membuat `DatabaseOperationPlan` berdasarkan `intent` dan skema.
    *   **File Dibuat:** `nodes/router.py`, `nodes/consult_schema.py`, `nodes/plan_execution.py`.

*   **3.3. Integrasi Alur Perencanaan ke Graph Utama**
    *   **Aktivitas:**
        *   a. Perbarui `graph.py` untuk menambahkan node-node baru ini.
        *   b. Jadikan `router` sebagai *entry point*.
        *   c. Rangkai alurnya: `router` -> `consult_schema` -> `plan_execution` -> `execute_and_store_data_node`.
        *   d. Hapus `DatabaseOperationPlan` yang di-*hardcode*.
    *   **File Diubah:** `backend/app/langgraph_workflow/graph.py`.

*   **3.4. Pengujian Fase 3: Uji Coba Penalaran Dinamis**
    *   **Aktivitas:** Uji kemampuan agent untuk membuat rencana dari nol.
    *   **Langkah Pengujian:**
        *   a. Kirim query bahasa natural ke API (`POST /api/v1/query`), misalnya "tampilkan 5 customer dari Jakarta".
        *   b. **Kriteria Sukses:** Agent harus berhasil menghasilkan `DatabaseOperationPlan` yang benar, mengeksekusinya, dan mengembalikan `DataHandle` dari hasil query yang sudah difilter.

---

### **Fase 4: Finalisasi "Sistem Produksi Laporan & Komunikasi"**

**Tujuan:** Menyempurnakan alur dengan validasi, penyajian hasil profesional, penanganan semua skenario, dan komunikasi *real-time* ke frontend.

*   **4.1. Implementasi Validasi & Ketahanan**
    *   **Aktivitas:** Tambahkan node `validate_plan` (dengan *self-correction loop*) dan `validate_results` ke dalam alur kerja.
    *   **File Dibuat/Diubah:** `nodes/validate_plan.py`, `nodes/validate_results.py`, `graph.py` (Revisi).

*   **4.2. Implementasi Penyajian & Alur Alternatif**
    *   **Aktivitas:**
        *   a. Implementasikan `replace_placeholders.py`. Node ini akan memanggil `retrieve_session_data` dari `graphiti_server` untuk mendapatkan data asli dan mengisi template.
        *   b. Implementasikan node `generate_acknowledgement` dan `generate_error_response`.
        *   c. **(Penting)** Implementasikan logika revisi di `plan_execution.py` untuk menangani `intent: REQUEST_MODIFICATION`.
    *   **File Dibuat/Diubah:** `nodes/replace_placeholders.py`, `nodes/generate_acknowledgement.py`, `nodes/generate_error_response.py`, `nodes/plan_execution.py` (Revisi).

*   **4.3. Implementasi Logging & Streaming (SSE)**
    *   **Aktivitas:**
        *   a. Implementasikan endpoint streaming SSE (`GET /api/v1/stream_updates/{session_id}`).
        *   b. Modifikasi `agent_service` untuk menggunakan `astream_events()` dan mengirim pembaruan ke klien yang terhubung.
        *   c. Tambahkan kode *timing* di setiap node.
        *   d. Implementasikan node `log_analytics` dan pastikan semua alur berakhir di sana.
    *   **File Dibuat/Diubah:** `api/v1/endpoints/query.py` (Revisi), `services/agent_service.py` (Revisi), semua file di `nodes/`, `nodes/log_analytics.py`.

*   **4.4. Pengujian Fase 4: Uji Coba Sistem Penuh**
    *   **Aktivitas:** Lakukan pengujian E2E yang komprehensif untuk semua skenario.
    *   **Langkah Pengujian:**
        *   a. Uji alur sukses (`EXECUTE_QUERY`), alur modifikasi (`REQUEST_MODIFICATION`), alur sosial (`ACKNOWLEDGE_RESPONSE`), dan alur error.
        *   b. **Verifikasi Streaming:** Gunakan *SSE client* untuk memastikan pembaruan *real-time* diterima dengan benar.
        *   c. **Verifikasi Hasil Akhir:** Pastikan respons final dari API berisi narasi dan tabel data yang sudah diformat dengan benar (bukan `DataHandle`).
        *   d. **Verifikasi Logging:** Periksa `logs/analytics.log` untuk memastikan setiap interaksi tercatat dengan lengkap.

---
Dengan pendekatan ini, kita membangun fitur secara logis, menguji integrasi di setiap fase, dan memastikan tidak ada "pemasangan kursi setelah badan pesawat ditutup". Ini adalah rencana yang jauh lebih kokoh dan profesional.
---

### **Dokumen Perencanaan: To-do List - Pembangunan Frontend (v1.0)**

**Versi:** 1.0
**Status:** Not Started

**Filosofi:** Membangun antarmuka pengguna secara bertahap, dimulai dengan kerangka visual dan konektivitas, lalu menambahkan lapisan interaktivitas dan fitur. Setiap fase diakhiri dengan pengujian untuk memastikan fondasi UI kokoh.

---

### **Fase 1: Pembangunan "Kerangka UI" & Konektivitas Dasar**

**Tujuan:** Membuat struktur visual dasar aplikasi (layout 3 panel), menerapkan tema, dan memastikan frontend dapat berkomunikasi dengan backend untuk memulai sesi dan mengirim permintaan. Ini adalah "chassis" dan "kabel-kabel dasar" dari mobil kita.

*   **1.1. Inisialisasi Proyek React & Struktur Folder Awal**
    *   **Aktivitas:** Gunakan `create-react-app` atau Vite untuk membuat proyek React baru. Susun struktur folder awal untuk komponen, service, dan style.
    *   **File yang Dibuat:**
        *   `frontend/` (root folder)
        *   `frontend/src/App.js`, `index.js`
        *   `frontend/src/components/` (folder kosong)
        *   `frontend/src/services/` (folder kosong)
        *   `frontend/src/styles/` (folder kosong)

*   **1.2. Implementasi Layout Tiga Panel & Tema Gelap**
    *   **Aktivitas:** Buat komponen-komponen dasar untuk layout tiga panel. Terapkan styling global untuk tema gelap (dark mode) menggunakan CSS atau library seperti Styled Components.
    *   **File yang Dibuat:**
        *   `frontend/src/components/layout/MainLayout.js`: Komponen utama yang mengatur tiga panel.
        *   `frontend/src/components/layout/LeftSidebar.js`: Komponen placeholder untuk panel kiri.
        *   `frontend/src/components/layout/MainContent.js`: Komponen placeholder untuk area tengah.
        *   `frontend/src/components/layout/RightSidebar.js`: Komponen placeholder untuk panel kanan.
        *   `frontend/src/styles/global.css`: CSS untuk tema gelap, font, dan layout dasar.
    *   **File yang Diubah:** `frontend/src/App.js` (untuk menggunakan `MainLayout`).

*   **1.3. Implementasi Service API untuk Komunikasi Backend**
    *   **Aktivitas:** Buat sebuah file service yang berisi fungsi-fungsi untuk berinteraksi dengan API backend. Untuk fase ini, kita hanya butuh dua fungsi.
        *   a. `startSession()`: Fungsi yang melakukan `GET` request ke `/api/v1/session/start`.
        *   b. `postQuery()`: Fungsi yang melakukan `POST` request ke `/api/v1/query` dengan membawa payload query.
    *   **File yang Dibuat:** `frontend/src/services/apiService.js`.

*   **1.4. Integrasi Manajemen Sesi pada Level Aplikasi**
    *   **Aktivitas:** Gunakan React's state management (misalnya, `useState` dan `useEffect` di `App.js`) untuk mengelola alur sesi.
        *   a. Saat komponen `App` pertama kali dimuat, panggil `apiService.startSession()`.
        *   b. Simpan `session_id` dan `suggested_queries` yang diterima dari backend ke dalam state aplikasi.
        *   c. Buat komponen `QueryInput` yang akan memanggil `apiService.postQuery()` saat pengguna mengirim pesan.
    *   **File yang Dibuat:** `frontend/src/components/chat/QueryInput.js`.
    *   **File yang Diubah:** `frontend/src/App.js` (untuk menambahkan state management dan logika pemanggilan API).

*   **1.5. Pengujian Fase 1: Validasi Kerangka dan Konektivitas**
    *   **Aktivitas:** Lakukan pengujian manual untuk memastikan semua komponen dasar terpasang dan berfungsi.
    *   **Langkah Pengujian:**
        *   a. **Uji Tampilan:** Jalankan aplikasi frontend (`npm start` atau `yarn start`). Pastikan layout tiga panel muncul dengan benar dan memiliki tema gelap.
        *   b. **Uji Inisiasi Sesi:**
            *   Buka *Developer Tools* di browser, pergi ke tab "Network".
            *   Refresh halaman. Verifikasi bahwa ada panggilan `GET` yang berhasil ke `/api/v1/session/start`.
            *   Periksa *console log* di aplikasi React untuk memastikan `session_id` dan `suggested_queries` berhasil diterima dan disimpan di dalam state.
        *   c. **Uji Pengiriman Query:**
            *   Ketik pesan di `QueryInput` dan tekan kirim.
            *   Di tab "Network", verifikasi bahwa ada panggilan `POST` ke `/api/v1/query`.
            *   Periksa payload request untuk memastikan `session_id` dan teks query dikirim dengan benar.
            *   **Kriteria Sukses:** Tidak harus ada respons yang "cantik" di UI saat ini. Cukup pastikan panggilan API terjadi dan backend (jika sedang berjalan dalam mode "skeleton") memberikan respons `200 OK`. Jika kita menjalankan backend "skeleton", kita bisa melihat log "pong" di konsol browser.

---
Setelah menyelesaikan fase ini, kita akan memiliki fondasi UI yang kokoh: aplikasi sudah memiliki "tubuh" (layout) dan "sistem saraf dasar" (koneksi API) yang siap untuk dihubungkan dengan fitur-fitur yang lebih cerdas di fase berikutnya.

---


### **Dokumen Perencanaan: To-do List - Pembangunan Frontend (v1.0)**

**Filosofi:** Membangun antarmuka pengguna secara bertahap, dimulai dengan kerangka visual dan konektivitas (chassis & kabel), lalu menambahkan alur kerja utama (mesin), diikuti oleh skenario alternatif (interior & kontrol), dan diakhiri dengan penyempurnaan (cat & detail).

---

### **Fase 1: Pembangunan "Kerangka UI" & Konektivitas Dasar**

**Tujuan:** Membuat struktur visual dasar aplikasi (layout 3 panel), menerapkan tema, dan memastikan frontend dapat berkomunikasi dengan backend untuk memulai sesi dan mengirim permintaan. Ini adalah "chassis" dan "kabel-kabel dasar" dari mobil kita.

*   **1.1. Inisialisasi Proyek React & Struktur Folder Awal**
    *   **Aktivitas:** Gunakan `create-react-app` atau Vite untuk membuat proyek React baru. Susun struktur folder awal untuk komponen, service, dan style.
    *   **File yang Dibuat:**
        *   `frontend/` (root folder)
        *   `frontend/src/App.js`, `index.js`
        *   `frontend/src/components/` (folder kosong)
        *   `frontend/src/services/` (folder kosong)
        *   `frontend/src/styles/` (folder kosong)

*   **1.2. Implementasi Layout Tiga Panel & Tema Gelap**
    *   **Aktivitas:** Buat komponen-komponen dasar untuk layout tiga panel. Terapkan styling global untuk tema gelap (dark mode) menggunakan CSS atau library seperti Styled Components.
    *   **File yang Dibuat:**
        *   `frontend/src/components/layout/MainLayout.js`: Komponen utama yang mengatur tiga panel.
        *   `frontend/src/components/layout/LeftSidebar.js`: Komponen placeholder untuk panel kiri.
        *   `frontend/src/components/layout/MainContent.js`: Komponen placeholder untuk area tengah.
        *   `frontend/src/components/layout/RightSidebar.js`: Komponen placeholder untuk panel kanan.
        *   `frontend/src/styles/global.css`: CSS untuk tema gelap, font, dan layout dasar.
    *   **File yang Diubah:** `frontend/src/App.js` (untuk menggunakan `MainLayout`).

*   **1.3. Implementasi Service API untuk Komunikasi Backend**
    *   **Aktivitas:** Buat sebuah file service yang berisi fungsi-fungsi untuk berinteraksi dengan API backend. Untuk fase ini, kita hanya butuh dua fungsi.
        *   a. `startSession()`: Fungsi yang melakukan `GET` request ke `/api/v1/session/start`.
        *   b. `postQuery()`: Fungsi yang melakukan `POST` request ke `/api/v1/query` dengan membawa payload query.
    *   **File yang Dibuat:** `frontend/src/services/apiService.js`.

*   **1.4. Integrasi Manajemen Sesi pada Level Aplikasi**
    *   **Aktivitas:** Gunakan React's state management (misalnya, `useState` dan `useEffect` di `App.js`) untuk mengelola alur sesi.
        *   a. Saat komponen `App` pertama kali dimuat, panggil `apiService.startSession()`.
        *   b. Simpan `session_id` dan `suggested_queries` yang diterima dari backend ke dalam state aplikasi.
        *   c. Buat komponen `QueryInput` yang akan memanggil `apiService.postQuery()` saat pengguna mengirim pesan.
    *   **File yang Dibuat:** `frontend/src/components/chat/QueryInput.js`.
    *   **File yang Diubah:** `frontend/src/App.js` (untuk menambahkan state management dan logika pemanggilan API).

*   **1.5. Pengujian Fase 1: Validasi Kerangka dan Konektivitas**
    *   **Aktivitas:** Lakukan pengujian manual untuk memastikan semua komponen dasar terpasang dan berfungsi.
    *   **Langkah Pengujian:**
        *   a. **Uji Tampilan:** Jalankan aplikasi frontend (`npm start` atau `yarn start`). Pastikan layout tiga panel muncul dengan benar dan memiliki tema gelap.
        *   b. **Uji Inisiasi Sesi:**
            *   Buka *Developer Tools* di browser, pergi ke tab "Network".
            *   Refresh halaman. Verifikasi bahwa ada panggilan `GET` yang berhasil ke `/api/v1/session/start`.
            *   Periksa *console log* di aplikasi React untuk memastikan `session_id` dan `suggested_queries` berhasil diterima dan disimpan di dalam state.
        *   c. **Uji Pengiriman Query:**
            *   Ketik pesan di `QueryInput` dan tekan kirim.
            *   Di tab "Network", verifikasi bahwa ada panggilan `POST` ke `/api/v1/query`.
            *   Periksa payload request untuk memastikan `session_id` dan teks query dikirim dengan benar.
    *   **Kriteria Sukses:** Aplikasi dapat dijalankan, menampilkan layout dasar, dan berhasil melakukan panggilan API untuk memulai sesi dan mengirim query. "Kerangka berjalan" kita sudah siap.

---

### **Fase 2: Implementasi Alur "Happy Path" (Query Baru & Hasil)**

**Tujuan:** Mengimplementasikan alur interaksi inti dari awal hingga akhir. Pengguna harus dapat mengajukan query baru, melihat visualisasi proses berpikir agent secara *real-time*, dan menerima laporan hasil yang terstruktur dan komprehensif.

*   **2.1. Implementasi Koneksi Server-Sent Events (SSE)**
    *   **Aktivitas:** Buat logika di frontend untuk membuat dan mengelola koneksi SSE.
        *   a. Setelah `session_id` didapat (dari Fase 1), buat instance `EventSource` yang menunjuk ke endpoint `GET /api/v1/stream_updates/{session_id}`.
        *   b. Buat *event listener* untuk menangani berbagai `event_type` yang akan dikirim dari backend (misalnya, `AGENT_THINKING`, `PLANNING_STEP_UPDATE`, `FINAL_RESULT`, `WORKFLOW_ERROR`).
        *   c. Simpan status koneksi SSE di dalam state aplikasi (misal: 'connecting', 'open', 'closed').
    *   **File yang Diubah:** `frontend/src/services/apiService.js` (untuk logika SSE), `frontend/src/App.js` (untuk mengelola koneksi).

*   **2.2. Implementasi Komponen "Fase Perencanaan" (State A)**
    *   **Aktivitas:** Buat komponen React baru yang secara dinamis me-render Daftar Rencana Aksi (To-do List) berdasarkan data dari SSE.
        *   a. Buat komponen `PlanningPhaseDisplay.js`.
        *   b. Komponen ini menerima daftar langkah-langkah perencanaan dari state aplikasi.
        *   c. Berdasarkan status setiap langkah ('pending', 'active', 'completed', 'failed'), komponen akan me-render ikon yang sesuai (lingkaran kosong, lingkaran berdenyut, centang hijau, silang merah).
        *   d. State ini diperbarui setiap kali *event listener* SSE menerima event `PLANNING_STEP_UPDATE`.
    *   **File yang Dibuat:** `frontend/src/components/chat/PlanningPhaseDisplay.js`.
    *   **File yang Diubah:** `frontend/src/components/chat/ConversationBlock.js` (sebuah komponen baru untuk membungkus setiap interaksi, yang akan menampilkan `PlanningPhaseDisplay` saat agent bekerja).

*   **2.3. Implementasi Komponen "Fase Hasil" (State B) - Bagian Utama**
    *   **Aktivitas:** Buat komponen-komponen untuk menampilkan hasil akhir yang diterima dari event `FINAL_RESULT`.
        *   a. Buat komponen `ResultsDisplay.js`.
        *   b. Di dalamnya, buat sub-komponen:
            *   `ExecutiveSummary.js`: Menampilkan metrik-metrik kunci.
            *   `AnalysisNarrative.js`: Menampilkan teks narasi dari agent.
            *   `DataQualityPanel.js`: Menampilkan skor kualitas, tingkat kepercayaan, dan peringatan.
    *   **File yang Dibuat:** `frontend/src/components/results/ResultsDisplay.js`, `ExecutiveSummary.js`, `AnalysisNarrative.js`, `DataQualityPanel.js`.
    *   **File yang Diubah:** `frontend/src/components/chat/ConversationBlock.js` (untuk menampilkan `ResultsDisplay` setelah proses selesai).

*   **2.4. Implementasi Komponen Tabel Data Interaktif**
    *   **Aktivitas:** Buat komponen tabel yang canggih untuk menampilkan data mentah di Panel Kanan.
        *   a. Pilih dan install library tabel yang baik untuk React (misalnya, `react-table` atau AG Grid Community).
        *   b. Buat komponen `InteractiveDataTable.js`.
        *   c. Komponen ini harus menerima `data` (array of objects) dan `columns` (konfigurasi header) dari state aplikasi.
        *   d. Implementasikan fungsionalitas **sorting per kolom**.
        *   e. Implementasikan tombol **ekspor ke CSV**.
    *   **File yang Dibuat:** `frontend/src/components/details/InteractiveDataTable.js`.
    *   **File yang Diubah:** `frontend/src/components/layout/RightSidebar.js` (untuk menampilkan tabel ini).

*   **2.5. Pengujian Fase 2: Validasi Alur "Happy Path"**
    *   **Aktivitas:** Lakukan pengujian end-to-end dengan backend yang sudah fungsional.
    *   **Langkah Pengujian:**
        *   a. **Uji Koneksi SSE:** Jalankan aplikasi. Setelah sesi dimulai, verifikasi di tab "Network" bahwa koneksi SSE berhasil dibuat dan tetap `pending`.
        *   b. **Uji Visualisasi Perencanaan:**
            *   Kirim query baru yang valid (misal: "tampilkan 5 customer").
            *   Amati dengan saksama: UI harus menampilkan Daftar Rencana Aksi. Verifikasi bahwa status setiap langkah berubah dari 'pending' -> 'active' (dengan animasi denyut) -> 'completed' (dengan centang hijau) secara *real-time* sesuai dengan event SSE yang masuk.
        *   c. **Uji Tampilan Hasil:**
            *   Setelah proses selesai, verifikasi bahwa "Daftar Rencana Aksi" menghilang dan digantikan oleh blok `ResultsDisplay`.
            *   Periksa apakah Ringkasan Eksekutif, Narasi, dan Skor Kualitas ditampilkan dengan benar sesuai data dari payload `FINAL_RESULT`.
        *   d. **Uji Tabel Interaktif:**
            *   Verifikasi bahwa tabel data mentah muncul di Panel Kanan.
            *   Klik header kolom untuk menguji fungsionalitas sorting.
            *   Klik tombol "Ekspor CSV" dan pastikan file CSV yang benar berhasil diunduh.
    *   **Kriteria Sukses:** Pengguna dapat mengajukan query dan mendapatkan laporan lengkap dengan pengalaman "live" yang transparan, dari awal hingga akhir. "Mesin utama" aplikasi sudah berfungsi.

---

### **Fase 3: Implementasi Alur Alternatif & Ketahanan UI**

**Tujuan:** Mengembangkan fungsionalitas UI untuk menangani skenario di luar alur query baru yang standar. Ini termasuk merespons berbagai `intent` dari backend, menangani error secara elegan, dan menyempurnakan alur percakapan.

*   **3.1. Implementasi State Management untuk Alur Percakapan**
    *   **Aktivitas:** Refaktor state management aplikasi untuk dapat menangani percakapan yang lebih kompleks.
        *   a. Struktur data state utama (misalnya di `App.js`) harus diubah untuk menyimpan riwayat interaksi sebagai sebuah array of "blok". Setiap blok akan memiliki ID unik dan bisa berisi `query`, `planning_steps`, `results`, atau `error_info`.
        *   b. Ini memungkinkan kita untuk merujuk dan memperbarui blok-blok sebelumnya, yang krusial untuk fitur modifikasi (Langkah 3.2).
    *   **File yang Diubah:** `frontend/src/App.js` (Refaktor besar pada state management).

*   **3.2. Implementasi Tampilan "Mode Revisi" (`REQUEST_MODIFICATION`)**
    *   **Aktivitas:** Buat logika di frontend untuk menangani `intent: REQUEST_MODIFICATION` dengan benar, sesuai yang telah kita rencanakan.
        *   a. Saat pengguna mengirim query lanjutan (misal: "filter untuk Jakarta"), frontend akan mengirimnya ke backend seperti biasa.
        *   b. Backend akan merespons dengan event SSE yang menandakan `intent` adalah `REQUEST_MODIFICATION`.
        *   c. Frontend harus menampilkan **Daftar Rencana Aksi yang lebih singkat** (misal: "Memperbarui rencana...", "Mengeksekusi ulang...").
        *   d. **Penting:** Setelah menerima `FINAL_RESULT` untuk modifikasi, UI harus **menemukan blok respons asli dan memperbaruinya**, bukan membuat blok baru. Ini bisa dilakukan dengan animasi *fade out/fade in* untuk menunjukkan pembaruan.
    *   **File yang Diubah:** `frontend/src/App.js` (logika untuk memperbarui blok), `frontend/src/components/chat/ConversationBlock.js`.

*   **3.3. Implementasi Tampilan Respons Sosial (`ACKNOWLEDGE_RESPONSE`)**
    *   **Aktivitas:** Tangani `intent` untuk interaksi sosial sederhana.
        *   a. Jika backend merespons dengan `intent: ACKNOWLEDGE_RESPONSE`, frontend harus langsung menampilkan respons teks singkat (misal: "Sama-sama! Senang bisa membantu.") tanpa melalui "Fase Perencanaan".
        *   b. Ini memastikan pengalaman yang cepat dan alami untuk basa-basi.
    *   **File yang Diubah:** `frontend/src/App.js` (logika untuk menangani `intent` ini).

*   **3.4. Implementasi Tampilan Penanganan Error yang Membimbing (`Graceful Failure`)**
    *   **Aktivitas:** Buat komponen UI khusus untuk menampilkan pesan error secara informatif.
        *   a. Buat komponen `ErrorDisplay.js`.
        *   b. Ketika backend mengirim event `WORKFLOW_ERROR`, komponen ini akan ditampilkan.
        *   c. Komponen ini akan menampilkan `user_message` dengan jelas dan ikon yang sesuai (misalnya, ikon peringatan).
        *   d. Sediakan tombol atau tautan "Lihat Detail Teknis" yang, jika diklik, akan menampilkan `technical_details` di Panel Kanan.
    *   **File yang Dibuat:** `frontend/src/components/chat/ErrorDisplay.js`.
    *   **File yang Diubah:** `frontend/src/components/chat/ConversationBlock.js` (untuk menampilkan `ErrorDisplay`).

*   **3.5. Pengujian Fase 3: Validasi Semua Alur Percakapan**
    *   **Aktivitas:** Lakukan pengujian manual yang komprehensif untuk semua skenario yang mungkin terjadi.
    *   **Langkah Pengujian:**
        *   a. **Uji Alur Modifikasi:** Kirim query awal, lalu kirim query modifikasi. Verifikasi UI memperbarui blok sebelumnya.
        *   b. **Uji Alur Sosial:** Kirim pesan "terima kasih". Verifikasi respons muncul instan.
        *   c. **Uji Alur Error:** Kirim query ambigu. Verifikasi komponen `ErrorDisplay` muncul.
        *   d. **Uji Regresi:** Pastikan alur "happy path" dari Fase 2 masih berfungsi dengan sempurna.
    *   **Kriteria Sukses:** Aplikasi terasa cerdas, dapat diandalkan, dan mampu menangani berbagai jenis dialog secara berbeda dan tepat, sesuai dengan konteks.

---

### **Fase 4: Polishing, Pemantauan, dan Detail Tambahan**

**Tujuan:** Menyempurnakan pengalaman pengguna dengan menambahkan fitur pemantauan kinerja, detail UI yang lebih kaya, dan interaktivitas yang lebih baik. Ini adalah fase "pemasangan interior mewah dan dashboard canggih" pada mobil kita.

*   **4.1. Implementasi Panel Detail Bertab yang Lengkap**
    *   **Aktivitas:** Lengkapi Panel Kanan dengan semua tab yang telah direncanakan.
        *   a. Buat komponen `TabbedDetailsPanel.js` yang akan menjadi kontainer untuk tab-tab.
        *   b. Buat komponen `ExecutionPlanDisplay.js` untuk menampilkan `DatabaseOperationPlan`. Gunakan library *syntax highlighter* (seperti `react-syntax-highlighter`) agar JSON mudah dibaca.
        *   c. Buat komponen `PerformanceLog.js` untuk menampilkan metrik performa (Total Durasi, Waktu Eksekusi DB, dll.) dalam format yang rapi.
    *   **File yang Dibuat:** `frontend/src/components/details/TabbedDetailsPanel.js`, `ExecutionPlanDisplay.js`, `PerformanceLog.js`.
    *   **File yang Diubah:** `frontend/src/components/layout/RightSidebar.js` (untuk menggunakan `TabbedDetailsPanel`).

*   **4.2. Implementasi Detail UI & Interaktivitas (Polishing)**
    *   **Aktivitas:** Tambahkan sentuhan-sentuhan kecil yang meningkatkan kualitas pengalaman pengguna.
        *   a. **Sapaan & Saran Query Kontekstual:** Tampilkan `greeting_message` dan `suggested_queries` dari backend saat sesi dimulai.
        *   b. **Animasi Mikro:** Tambahkan transisi CSS yang halus (misalnya, `transition: all 0.3s ease;`) pada elemen-elemen UI seperti saat blok respons baru muncul (*fade-in*).
        *   c. **Tombol Minimize Panel:** Implementasikan logika `useState` untuk mengontrol visibilitas Panel Kiri dan Kanan. Tambahkan tombol ikon (misal: `<<` dan `>>`) untuk memicu perubahan state ini.

*   **4.3. Pengujian Fase 4: Validasi Fitur Lanjutan dan Kualitas UI**
    *   **Aktivitas:** Lakukan pengujian menyeluruh pada semua fitur baru dan pastikan tidak ada regresi pada fungsionalitas yang sudah ada.
    *   **Langkah Pengujian:**
        *   a. **Uji Panel Detail:** Klik setiap tab ("Data Mentah", "Rencana Eksekusi", "Log & Performa"). Pastikan konten yang ditampilkan di setiap tab benar dan rapi.
        *   b. **Uji Interaktivitas:** Klik tombol minimize pada panel samping. Pastikan panel menyusut/menghilang dengan animasi yang halus.
        *   c. **Uji Onboarding:** Refresh aplikasi. Verifikasi bahwa sapaan pembuka dan tombol saran query muncul dengan benar.
        *   d. **Uji Regresi Penuh:** Lakukan kembali pengujian dari Fase 2 dan 3 untuk memastikan semua alur utama masih berfungsi dengan sempurna.
    *   **Kriteria Sukses:** Aplikasi terasa lengkap, profesional, dan informatif. Semua fitur yang direncanakan di dokumen UI/UX telah terimplementasi dan berfungsi dengan baik.