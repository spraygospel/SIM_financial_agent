# Rancangan MVP AI Agent untuk Query SQL Source File

## 1. Konsep Dasar & Tujuan MVP

### Tujuan Utama
Membangun AI agent yang dapat memahami pertanyaan bisnis dalam bahasa natural dan menghasilkan laporan finansial akurat dari SQL source file. Agent harus dapat menampilkan data mentah dalam tabel dan memberikan analisis naratif yang dapat dipercaya.

### Prinsip Desain MVP
- **Fokus Fungsionalitas**: Prioritas pada akurasi data dan kemampuan query, bukan keamanan
- **Zero Manual Calculation by LLM**: LLM dilarang keras melakukan perhitungan angka
- **Transparency First**: Semua data mentah ditampilkan untuk verifikasi user
- **Placeholder Strategy**: LLM bekerja dengan template, angka diisi oleh system

Tentu. Saya siap. Mari kita mulai proses penulisan ulang dokumen perencanaan inti kita, dimulai dengan Bab 2.

Berikut adalah draf revisi untuk **Bab 2: Arsitektur Sistem** dari dokumen `1mvp_ai_agent_rancangan.md`. Bab ini telah ditulis ulang sepenuhnya untuk mencerminkan arsitektur **Model Context Protocol (MCP)** yang telah kita sepakati.

---

## **Bab 2: Arsitektur Sistem**

### **2.1. Filosofi Arsitektur Baru: Modular dan Terisolasi**

Arsitektur sistem AI Agent ini dirancang dengan filosofi **modularitas, portabilitas, dan keamanan** sebagai pilar utamanya. Kita secara sadar menghindari pendekatan monolitik di mana agent memiliki akses langsung ke semua sumber daya.

Sebagai gantinya, kita mengadopsi **Model Context Protocol (MCP)**. Dalam arsitektur ini, AI Agent inti (yang dibangun dengan LangGraph) bertindak sebagai **"Otak" atau "MCP Client"** yang cerdas. Ia tidak melakukan pekerjaan teknis seperti koneksi database secara langsung. Sebaliknya, ia mendelegasikan tugas-tugas tersebut kepada **"Departemen Spesialis" atau "MCP Server"** yang terisolasi.

Pendekatan ini memberikan beberapa keuntungan strategis:
*   **Keamanan:** Agent inti tidak pernah memiliki kredensial atau akses langsung ke database. Semua interaksi dimediasi melalui server spesialis yang memiliki satu tugas jelas.
*   **Portabilitas:** Setiap MCP Server (misalnya, untuk database `sim_testgeluran` atau Graphiti) adalah komponen mandiri. Mereka dapat dengan mudah diperbarui, diganti, atau bahkan digunakan kembali di proyek AI lain di masa depan tanpa mengubah agent inti.
*   **Skalabilitas:** Setiap server spesialis dapat di-scale secara independen sesuai dengan bebannya.

### **2.2. Komponen Utama Sistem**

Sistem kita terdiri dari beberapa komponen utama yang berinteraksi melalui peran yang jelas:

1.  **Frontend (React.js):** Antarmuka pengguna tempat pengguna berinteraksi, memasukkan query, dan melihat hasil (termasuk Fase Perencanaan dan Fase Hasil).

2.  **Backend API (FastAPI):** Gerbang utama yang menerima permintaan dari frontend dan mengorkestrasi seluruh proses dengan memanggil `AgentService`.

3.  **LangGraph Workflow (AI Agent Core - sebagai MCP Client):**
    *   Ini adalah otak dari operasi. Bertanggung jawab untuk memahami query, merencanakan `DatabaseOperationPlan`, dan mengelola alur kerja.
    *   **Peran Kunci:** Ia tidak lagi terhubung ke database. Sebaliknya, ia bertindak sebagai **klien** yang memanggil *tools* yang disediakan oleh MCP Server.

4.  **`sim_testgeluran_server` (MCP Server):**
    *   Ini adalah "Departemen" yang bertanggung jawab penuh atas database operasional MySQL `sim_testgeluran`.
    *   **Tugas Inti:** Mengekspos sebuah *tool* (misalnya, `execute_operation_plan`) yang menerima `DatabaseOperationPlan` dalam format JSON.
    *   **Teknologi Internal:** Di dalam server inilah **logika SQLAlchemy ORM** berada. Ia menerjemahkan rencana JSON menjadi query ORM yang aman dan mengeksekusinya.

5.  **`graphiti_server` (MCP Server):**
    *   Ini adalah "Departemen" yang bertanggung jawab atas *knowledge graph* (Neo4j).
    *   **Tugas Inti:** Mengekspos *tool* (misalnya, `get_relevant_schema`) yang menerima intent dan entitas, lalu mengembalikan informasi skema yang relevan.

6.  **Database Operasional (MySQL):** Sumber data aktual yang berisi data bisnis `sim_testgeluran`. Hanya dapat diakses oleh `sim_testgeluran_server`.

7.  **Knowledge Graph (Graphiti/Neo4j):** Sumber metadata skema yang diperkaya. Hanya dapat diakses oleh `graphiti_server`.

### **2.3. Diagram Aliran Data (DFD) dengan Arsitektur MCP**

Diagram ini mengilustrasikan alur baru di mana Agent Core (LangGraph) berkomunikasi dengan MCP Server, dan MCP Server-lah yang berkomunikasi dengan sumber data.

```mermaid
graph TD
    A[Pengguna via Frontend] --> B{Backend API (FastAPI)};
    B --> C[Memulai LangGraph Workflow (Agent Core)];

    subgraph Agent Core (Bertindak sebagai MCP Client)
        direction LR
        N1[Node: Router] --> N2[Node: consult_schema];
        N2 --> N3[Node: plan_execution];
        N3 --> N4[Node: validate_plan];
        N4 --> N5[Node: execute_query];
        N5 --> N6[Node: validate_results];
        N6 --> N7[Node: replace_placeholders];
        N7 --> N8[Node: log_analytics];
        N8 --> F[Hasil Akhir untuk API];

        %% Jalur Error (Sederhana)
        subgraph Alur Error
            direction LR
            N1 & N2 & N3 & N4 & N5 & N6 & N7 -- Error Kritis --> NE[Node: generate_error_response];
            NE --> N8_ERR[Node: log_analytics];
            N8_ERR --> G[Respons Error untuk API];
        end
    end

    %% Interaksi dengan MCP Servers
    N2 -- 1. Panggil Tool `get_relevant_schema` --> MCP_Graphiti[MCP Server: graphiti_server];
    MCP_Graphiti -- 2. Query Metadata --> GraphitiDB[(Graphiti KG / Neo4j)];
    GraphitiDB -- 3. Respons Metadata --> MCP_Graphiti;
    MCP_Graphiti -- 4. Kirim Hasil Skema (JSON) --> N2;

    N5 -- 5. Panggil Tool `execute_operation_plan` --> MCP_MySQL[MCP Server: sim_testgeluran_server];
    MCP_MySQL -- 6. Terjemahkan Rencana ke Query ORM --> ORM[SQLAlchemy ORM Layer];
    ORM -- 7. Eksekusi Query --> MySQL_DB[(Database ERP / MySQL)];
    MySQL_DB -- 8. Respons Data Mentah --> ORM;
    ORM -- 9. Kirim Hasil Data (JSON) --> MCP_MySQL;
    MCP_MySQL -- 10. Kirim Hasil Data (JSON) --> N5;

    F --> H{AgentService di Backend API};
    G --> H;
    H --> I[Respons API ke Frontend];
    I --> J[Tampilan ke Pengguna];
```

### **2.4. Deskripsi Aliran Data Detail**

1.  **Input Pengguna:** Pengguna mengirimkan query melalui Frontend ke Backend API.
2.  **Inisiasi Agent:** `AgentService` memulai LangGraph Workflow.
3.  **Routing & Perencanaan:** `Router` menentukan intent, `consult_schema` memanggil `graphiti_server` untuk mendapatkan peta data, dan `plan_execution` membuat `DatabaseOperationPlan` (rencana JSON).
4.  **Validasi Rencana:** `validate_plan` memeriksa apakah rencana JSON tersebut logis dan bisa dijalankan.
5.  **Delegasi Eksekusi:** Node `execute_query` sekarang bertindak sebagai klien. Ia **mengirim `DatabaseOperationPlan`** ke `sim_testgeluran_server` melalui panggilan *tool* MCP.
6.  **Eksekusi oleh Spesialis:** `sim_testgeluran_server` menerima rencana JSON. Di dalam server ini, **SQLAlchemy ORM menerjemahkan rencana tersebut** menjadi query yang aman dan mengeksekusinya ke database MySQL.
7.  **Laporan Hasil:** `sim_testgeluran_server` mengembalikan hasil query (dalam format JSON) ke node `execute_query`.
8.  **Pemrosesan Akhir:** Alur LangGraph melanjutkan prosesnya (validasi hasil, mengisi template, logging analitik) menggunakan data yang diterima dari MCP server.
9.  **Output ke Pengguna:** Hasil akhir yang sudah dipoles dikirim kembali melalui API ke Frontend untuk ditampilkan.

---

## 3. Strategi Placeholder untuk Mencegah LLM Generate Angka

### Konsep Placeholder
LLM tidak pernah melihat angka finansial aktual saat generate response. Sebagai gantinya, LLM bekerja dengan placeholder yang akan diganti oleh system sebelum ditampilkan ke user.

### Contoh Implementasi Placeholder
**User Query**: "Tunjukkan total penjualan Januari 2023"

**LLM Generate Template**:
```
Berdasarkan analisis data penjualan Januari 2023:

Total Penjualan: {TOTAL_SALES_JAN_2023}
Jumlah Transaksi: {COUNT_ORDERS_JAN_2023}
Rata-rata Nilai Order: {AVG_ORDER_VALUE_JAN_2023}

Analisis:
Performa penjualan pada periode ini menunjukkan {PERFORMANCE_TREND_JAN_2023}. 
Dibandingkan dengan target bulanan sebesar {MONTHLY_TARGET_JAN_2023}, 
pencapaian berada pada level {ACHIEVEMENT_PERCENTAGE_JAN_2023}.
```

**System Replace Placeholder**:
```
Total Penjualan: Rp 125.000.000
Jumlah Transaksi: 456 transaksi
Rata-rata Nilai Order: Rp 274.123
```

### Jenis-Jenis Placeholder
- **Financial Values**: `{TOTAL_SALES_Q1}`, `{REVENUE_GROWTH_RATE}`
- **Counts**: `{CUSTOMER_COUNT}`, `{TRANSACTION_COUNT}`
- **Percentages**: `{PROFIT_MARGIN}`, `{GROWTH_PERCENTAGE}`
- **Dates**: `{REPORT_PERIOD}`, `{LAST_UPDATE_DATE}`
- **Names/Labels**: `{TOP_CUSTOMER}`, `{BEST_PRODUCT}`


---


## **Bab 4: Penanganan Database & Knowledge Graph**

### **4.1. Pemisahan Tanggung Jawab Akses Data**

Dalam arsitektur baru kami, AI Agent Core (LangGraph) **tidak lagi memiliki akses langsung** ke sumber data mana pun. Semua interaksi data dimediasi melalui dua server spesialis (MCP Server) yang bertindak sebagai gateway yang aman dan terstruktur.

1.  **`sim_testgeluran_server`**: Satu-satunya komponen yang diizinkan untuk terhubung dan melakukan query ke database operasional **MySQL `sim_testgeluran`**. Ia menggunakan SQLAlchemy ORM secara internal untuk keamanan dan keandalan.
2.  **`graphiti_server`**: Satu-satunya komponen yang diizinkan untuk terhubung dan melakukan query ke **Graphiti Knowledge Graph (Neo4j)** untuk mengambil metadata skema.

Pemisahan ini memastikan bahwa logika bisnis agent tetap terpisah dari detail teknis implementasi penyimpanan data.

### **4.2. Strategi Pemuatan dan Pengelolaan Skema di `graphiti_server`**

`graphiti_server` bertanggung jawab untuk menyediakan "peta data" yang kaya dan kontekstual kepada agent.

*   **Inisialisasi Awal (Offline/Scripted):**
    1.  **Ekstraksi Skema Dasar:** Sebuah skrip (`scripts/extract_mysql_schema.py`) akan digunakan untuk mengekstrak struktur dasar (`CREATE TABLE`) dari database MySQL `sim_testgeluran`.
    2.  **Pengayaan Semantik:** Informasi skema dasar ini akan diperkaya dengan metadata semantik dari file konfigurasi terpusat (misalnya, `graphiti_semantic_mapping.json`). Metadata ini mencakup:
        *   **`purpose`**: Tujuan bisnis dari setiap tabel (misalnya, "Mencatat transaksi penjualan").
        *   **`business_category`**: Kategori data ("financial", "operational", "master_data").
        *   **`classification`**: Klasifikasi fungsional untuk setiap kolom ("financial_amount", "temporal", "identifier").
        *   **`is_aggregatable`**: Menandai kolom mana yang bisa di-`SUM`, `AVG`, `COUNT`.
        *   **`relationships`**: Definisi eksplisit dari `Foreign Key` antar tabel.
    3.  **Populasi ke Neo4j:** Skrip lain (`scripts/sync_mysql_to_graphiti.py`) akan mengambil skema yang telah diperkaya ini dan mempopulasikannya ke dalam Neo4j, menciptakan node `:DatabaseTable`, `:DatabaseColumn`, dan relasi `:HAS_COLUMN` serta `:REFERENCES`.

*   **Akses Saat Runtime:**
    *   AI Agent (melalui `consult_schema_node`) akan memanggil *tool* yang diekspos oleh `graphiti_server` (misalnya, `get_relevant_schema`).
    *   Tool ini akan melakukan query Cypher ke Neo4j untuk mengambil hanya bagian dari skema yang relevan dengan `intent` dan `entities` dari permintaan pengguna, lalu mengembalikannya dalam format JSON yang bersih.

### **4.3. Strategi Eksekusi Query di `sim_testgeluran_server`**

`sim_testgeluran_server` adalah "tangan" yang mengeksekusi permintaan data ke database MySQL.

*   **Prinsip Utama: Eksekusi Berdasarkan Rencana, Bukan Perintah SQL**
    *   Server ini **tidak akan pernah** menerima string SQL mentah dari agent. Ini adalah aturan keamanan yang fundamental.
    *   Sebagai gantinya, ia menerima objek **`DatabaseOperationPlan`** dalam format JSON.

*   **Proses Internal `sim_testgeluran_server`:**
    1.  **Menerima Rencana:** Tool `execute_operation_plan` menerima `DatabaseOperationPlan` dari `execute_query_node`.
    2.  **Penerjemahan ke ORM:** Di sinilah keajaiban terjadi. Server akan mem-parsing objek JSON tersebut dan, menggunakan **SQLAlchemy ORM**, secara dinamis membangun objek query Python.
        *   `"main_table": "arbook"` akan diterjemahkan menjadi `session.query(Arbook)`.
        *   `"joins": [...]` akan menjadi `query.join(MasterCustomer, ...)`.
        *   `"filters": [...]` akan menjadi `query.filter(...)`.
        *   `"select_columns": [{"aggregation": "SUM", ...}]` akan menjadi `query.with_entities(func.sum(...))`.
    3.  **Eksekusi Aman:** SQLAlchemy akan menghasilkan query SQL yang aman (dengan parameterisasi otomatis untuk mencegah SQL injection) dan mengeksekusinya ke database MySQL.
    4.  **Mengembalikan Hasil:** Hasil query dari database (biasanya berupa list objek atau tuple) akan dikonversi kembali menjadi format JSON standar (`List[Dict[str, Any]]`) dan dikirim kembali sebagai respons ke agent.

Pendekatan ini memastikan bahwa semua logika interaksi database yang kompleks dan rentan terhadap error terisolasi di dalam server spesialis ini, sementara agent inti dapat fokus pada tugas-tugas tingkat tinggi seperti perencanaan dan penalaran.


---

## **Bab 5: LangGraph Workflow Design (Revisi)**

### **5.1. Alur Kerja Cerdas Berbasis Intent**

Desain alur kerja (workflow) LangGraph kami telah berevolusi dari alur linear sederhana menjadi **State Machine yang cerdas dan adaptif**. Alih-alih mengikuti satu jalur yang kaku, agent kini mampu memilih alur kerja yang paling efisien berdasarkan **intent** (maksud) dari permintaan pengguna. Ini memungkinkan respons yang lebih cepat untuk tugas-tugas sederhana dan alur yang lebih teliti untuk permintaan data yang kompleks.

### **5.2. `AgentState`: Memori Kerja Agent**

Struktur `AgentState` adalah pusat dari semua operasi. Ini adalah memori dinamis yang dibawa dan diperbarui oleh setiap node.

*   **Penyimpanan Data:** Untuk menjaga `AgentState` tetap ringan, data mentah hasil query dari database tidak disimpan langsung di sini. Sebaliknya, kita menggunakan **`DataHandle`**, sebuah pointer yang merujuk ke data yang disimpan sementara di Graphiti selama sesi berlangsung.
*   **Struktur Kunci `AgentState`:**
    *   **Input & Konteks:** `user_query`, `session_id`, `conversation_history`.
    *   **Hasil Routing:** `intent` (misalnya, `EXECUTE_QUERY`, `REQUEST_MODIFICATION`).
    *   **Hasil Perencanaan:** `database_operations_plan` (rencana JSON untuk dieksekusi).
    *   **Pointer Data:** `raw_query_results_handle`, `financial_calculations_handles` (objek `DataHandle`).
    *   **Status & Hasil:** `validation_status`, `quality_score`, `final_narrative`, dll.

### **5.3. Diagram Alur Kerja LangGraph yang Telah Disempurnakan**

Diagram ini menunjukkan alur kerja baru yang bercabang, dengan `Router` sebagai titik keputusan utama.

```mermaid
graph TD
    A[START] --> N1_Router(Node: Router);
    
    subgraph Alur Utama
        direction LR
        N1_Router -- Intent: EXECUTE_QUERY --> N2_ConsultSchema(Node: consult_schema);
        N2_ConsultSchema --> N3_PlanExecution(Node: plan_execution);
        
        N1_Router -- Intent: REQUEST_MODIFICATION --> N3_PlanExecution_Mod(Node: plan_execution<br/>(Mode Revisi));
        
        N3_PlanExecution --> N4_ValidatePlan(Node: validate_plan);
        N3_PlanExecution_Mod --> N4_ValidatePlan;

        subgraph "Validation & Repair Loop"
            direction TB
            N4_ValidatePlan -- Rencana Valid --> N5_ExecuteQuery(Node: execute_query);
            N4_ValidatePlan -- Rencana TIDAK Valid --> N3_RePlan(Node: plan_execution<br/>(Mode Perbaikan));
            N3_RePlan --> N4_ValidatePlan;
        end
        
        N5_ExecuteQuery --> N6_ValidateResults(Node: validate_results);
    end
    
    subgraph Alur Sederhana
        direction LR
        N1_Router -- Intent: ACKNOWLEDGE_RESPONSE --> N_Ack(Node: generate_acknowledgement);
    end

    subgraph Alur Penanganan Error
        direction LR
        N1_Router -- Intent: UNKNOWN_OR_AMBIGUOUS --> N_Error(Node: generate_error_response);
        N6_ValidateResults -- Hasil Gagal Kritis --> N_Error;
    end
    
    subgraph Alur Akhir
        direction LR
        N6_ValidateResults -- Hasil Valid --> N7_FormatOutput(Node: replace_placeholders);
        N_Ack --> N8_Log(Node: log_analytics);
        N7_FormatOutput --> N8_Log;
        N_Error -- " " --> N8_Log;
        N8_Log --> Z[END];
    end
```

### **5.4. Deskripsi Node dan Logika Kondisional**

**1. Node: `Router` (Titik Awal & Keputusan)**
*   **Tugas:** Menganalisis `user_query` dan `conversation_history` untuk menentukan satu dari beberapa intent yang telah didefinisikan (`EXECUTE_QUERY`, `REQUEST_MODIFICATION`, `ACKNOWLEDGE_RESPONSE`, `UNKNOWN_OR_AMBIGUOUS`).
*   **Logika Kondisional Berikutnya:** Alur diarahkan berdasarkan `intent` yang dihasilkan.

**2. Node: `consult_schema`**
*   **Tugas:** Dipanggil hanya jika intent adalah `EXECUTE_QUERY`. Bertindak sebagai MCP Client untuk memanggil `graphiti_server` dan mendapatkan "peta data" yang relevan.

**3. Node: `plan_execution`**
*   **Tugas:**
    *   **Mode Normal (`EXECUTE_QUERY`):** Membuat `DatabaseOperationPlan` dari nol.
    *   **Mode Revisi (`REQUEST_MODIFICATION`):** Mengambil rencana sebelumnya dari `AgentState` dan memodifikasinya (misalnya, menambahkan filter).
    *   **Mode Perbaikan (`Repair Loop`):** Menerima rencana yang gagal validasi dan mencoba memperbaikinya berdasarkan pesan error.

**4. Node: `validate_plan` (Validation & Repair Loop)**
*   **Tugas:** Memeriksa `DatabaseOperationPlan` yang dibuat oleh `plan_execution`. Apakah tabel dan kolomnya valid? Apakah strukturnya benar?
*   **Logika Kondisional Berikutnya:**
    *   **Jika Valid:** Lanjutkan ke `execute_query`.
    *   **Jika Tidak Valid:** Kembali ke `plan_execution` dengan mode perbaikan. Jika perbaikan gagal setelah beberapa kali percobaan, alihkan ke `generate_error_response`.

**5. Node: `execute_query`**
*   **Tugas:** Bertindak sebagai MCP Client. Mengirim `DatabaseOperationPlan` ke `sim_testgeluran_server`. Setelah menerima hasil, ia akan menyimpan data ke Graphiti dan menempatkan `DataHandle` ke dalam `AgentState`.

**6. Node: `validate_results`**
*   **Tugas:** Menggunakan `DataHandle` untuk mengambil data dari Graphiti, lalu melakukan pemeriksaan kualitas dan konsistensi.
*   **Logika Kondisional Berikutnya:**
    *   **Jika Hasil Valid:** Lanjutkan ke `replace_placeholders`.
    *   **Jika Hasil Gagal Kritis (misal, data tidak ada atau tidak logis):** Alihkan ke `generate_error_response`.

**7. Node: `replace_placeholders` & `generate_acknowledgement`**
*   **Tugas:** Mempersiapkan output akhir yang akan dilihat pengguna, baik berupa laporan lengkap maupun respons sosial singkat.

**8. Node: `generate_error_response`**
*   **Tugas:** Menangani semua kondisi error kritis, menyiapkan pesan yang ramah untuk pengguna dan detail teknis untuk log.

**9. Node: `log_analytics` (Langkah Terakhir)**
*   **Tugas:** Titik temu untuk semua alur (sukses maupun gagal). Node ini mengumpulkan semua metrik dari `AgentState` dan mencatatnya sebagai `AnalyticsLogEntry` untuk analisis performa di kemudian hari. Setelah itu, alur kerja berakhir.

Desain alur kerja ini mengubah agent kita menjadi sistem yang lebih tangguh, efisien, dan sadar-konteks, siap untuk menangani berbagai jenis interaksi pengguna dengan cerdas.

## 6. Implementasi Teknik dari Dokumen Odoo

### Structured Data Mapping (DRLF-like)
Buat mapping konstanta untuk standardisasi financial metrics:
```
FINANCIAL_METRICS_MAPPING = {
  "REVENUE_TOTAL": {
    "label_id": "Total Pendapatan",
    "label_en": "Total Revenue", 
    "typical_sources": ["sales_orders.total_amount"],
    "aggregation": "SUM",
    "category": "income_statement"
  },
  "CUSTOMER_COUNT": {
    "label_id": "Jumlah Customer",
    "label_en": "Customer Count",
    "typical_sources": ["customers.customer_id"],
    "aggregation": "COUNT_DISTINCT",
    "category": "operational"
  }
}
```

### Validation Summary Pattern
Setiap output akan include validation summary seperti di Odoo:
```
Validation Summary:
✓ Data Quality Checks Passed: 5/6
✓ Total Records Processed: 1,247
✓ Date Range Validity: Valid (Jan 1 - Jan 31, 2023)
⚠ Warning: 3 transactions have zero amount
⚠ Note: Data only available until Jan 28, 2023
```

### Pemisahan Peran LLM vs Tools
- **LLM Role**: Understanding, planning, narrative generation
- **Tools Role**: SQL execution, calculations, data aggregation
- **Validation Role**: Data quality checks, consistency validation
- **Formatting Role**: Number formatting, currency display

### Episodic Memory dengan Graphiti
Gunakan Graphiti untuk menyimpan:
- **Schema Episodes**: Setiap table dan column sebagai knowledge entities
- **Query Episodes**: Pattern query yang sering digunakan untuk learning
- **Validation Episodes**: Common data issues dan cara penanganannya
- **User Preference Episodes**: Format output yang disukai user

---

## **Bab 7: User Experience (UX) & Desain Antarmuka (UI)**

### **7.1. Filosofi Desain: Profesional, Transparan, dan Personal**

Desain antarmuka pengguna (UI) dan pengalaman pengguna (UX) untuk AI Agent ini berpegang pada tiga prinsip utama untuk memberikan kesan premium dan membangun kepercayaan:

1.  **Profesional & Modern:** Antarmuka akan mengadopsi tema gelap (dark mode) yang bersih dengan tipografi yang jelas dan ikonografi minimalis, layaknya perangkat lunak analitik kelas atas.
2.  **Transparansi Radikal:** Pengguna tidak akan pernah merasa berinteraksi dengan "kotak hitam". Setiap langkah yang diambil agent, mulai dari perencanaan hingga eksekusi, akan divisualisasikan, memberikan pengguna pemahaman penuh atas proses yang terjadi.
3.  **Personal & Cerdas:** Interaksi harus terasa seperti dialog dengan asisten pribadi yang cerdas, bukan dengan mesin yang kaku. Ini dicapai melalui sapaan personal, umpan balik proaktif, dan animasi yang halus.

### **7.2. Anatomi Antarmuka: Tata Letak Tiga Panel**

Antarmuka utama akan dibagi menjadi tiga area fungsional yang dapat disesuaikan untuk memberikan fleksibilitas maksimal kepada pengguna.

*   **Panel Kiri (Sidebar Riwayat):** Berisi riwayat percakapan dan tombol untuk memulai sesi baru. Dapat di-minimize untuk memberikan lebih banyak ruang.
*   **Panel Tengah (Area Interaksi Utama):** Fokus utama pengguna, tempat mereka mengetik query dan menerima hasil analisis dari agent.
*   **Panel Kanan (Panel Data & Detail):** "Ruang bukti" yang berisi data pendukung. Menggunakan sistem tab dan dapat di-minimize/maximize.

```ascii
+----------------------+------------------------------------------+--------------------------------+
| [<<] Sidebar Kiri    |    Area Interaksi Utama (Tengah)         | Panel Kanan (Data & Detail) [>>] |
|----------------------|------------------------------------------|--------------------------------|
| [+] New Chat         | +--------------------------------------+ | + [Data]  [Rencana]  [Log]   + |
|                      | | (Konten Interaksi ditampilkan di sini) | | |                              |
| Riwayat Query:       | +--------------------------------------+ | | (Konten Tab Aktif)           |
|  - Query 1 ✅        |                                          | |                              |
|  - ...               |                                          | |                              |
+----------------------+------------------------------------------+--------------------------------+
```

### **7.3. Dua Fase Pengalaman Pengguna**

Pengalaman pengguna secara dinamis akan berubah antara dua fase utama untuk setiap query yang kompleks.

**Fase 1: Perencanaan (Agent "Berpikir")**
Setelah pengguna mengirim query, antarmuka tidak menampilkan ikon loading yang membosankan. Sebaliknya, ia menampilkan **Daftar Rencana Aksi (To-do List)** yang dibuat oleh agent.

*   **Tampilan:** Sebuah daftar langkah-langkah yang akan dieksekusi agent.
*   **Interaktivitas Real-Time:**
    *   Langkah yang sedang diproses akan ditandai dengan **lingkaran hijau yang berdenyut (pulsing circle)**.
    *   Langkah yang sudah selesai akan ditandai dengan ikon centang hijau (✅).
*   **Tujuan:** Memberikan transparansi penuh dan mengubah waktu tunggu menjadi pengalaman yang menarik dan informatif.

**Fase 2: Hasil (Laporan Disajikan)**
Setelah semua langkah perencanaan selesai, tampilan akan bertransisi dengan mulus untuk menyajikan hasil akhir di Panel Tengah.

*   **Komponen Utama di Panel Tengah:**
    1.  **Ringkasan Eksekutif:** Metrik-metrik kunci ditampilkan dengan visual yang menonjol.
    2.  **Analisis Naratif:** Paragraf penjelasan dalam bahasa alami.
    3.  **Panel Kualitas & Kepercayaan:**
        *   `Skor Kualitas Data: 95/100 ⭐⭐⭐⭐⭐`
        *   `Tingkat Kepercayaan Analisis: [🟩🟩🟩🟩🟩] Tinggi`
    4.  **Peringatan (Warnings):** Catatan penting tentang data (misalnya, `⚠️ Data tidak lengkap`).

### **7.4. Onboarding Pengguna dan "Guardrails"**

Untuk memastikan pengguna baru dapat langsung merasakan manfaat dan tidak frustrasi, antarmuka akan menyediakan panduan secara proaktif.

*   **Saran Query (Suggested Queries):**
    *   Saat sesi baru dimulai, di bawah sapaan hangat ("Selamat pagi!"), akan ditampilkan beberapa tombol dengan contoh query yang bisa diklik.
    *   Contoh: `[ Tampilkan total penjualan bulan ini ]`
    *   **Tujuan:** Menghilangkan kebingungan awal dan memastikan interaksi pertama pengguna berhasil.

*   **Penanganan Error yang Membimbing (Graceful Failure):**
    *   Jika pengguna bertanya sesuatu di luar kemampuan MVP, agent tidak hanya akan berkata "Saya tidak bisa".
    *   Ia akan memberikan respons yang lebih cerdas, contohnya: "Maaf, saya belum bisa membandingkan data. Namun, saya bisa menampilkan data untuk bulan ini terlebih dahulu. Apakah Anda mau?"
    *   **Tujuan:** Mengelola ekspektasi dan menjaga alur percakapan tetap produktif.

### **7.5. Personalisasi dan Sentuhan Akhir**

Detail-detail kecil akan ditambahkan untuk membuat pengalaman terasa premium dan personal.

*   **Sapaan Kontekstual:** Sapaan pembuka yang disesuaikan dengan waktu (pagi/siang/malam).
*   **Animasi Mikro:** Transisi yang halus antar elemen UI, seperti efek *fade-in* atau animasi klik tombol, untuk memberikan kesan responsif dan modern.
*   **Tampilan Data Interaktif:** Tabel di Panel Kanan akan mendukung *sorting* per kolom dan memiliki tombol ekspor ke CSV, memberikan kontrol lebih kepada pengguna.

Desain ini memastikan bahwa antarmuka AI Agent tidak hanya menjadi alat yang kuat, tetapi juga partner dialog yang transparan, cerdas, dan menyenangkan untuk digunakan.

## 8. Intelligent Fallback & Recovery System

### Three-Layer Fallback Strategy

**Layer 1: Schema Fallback (untuk Table/Column Not Found)**
```
Primary Query Failed: "SELECT * FROM customer_payments"
├── Error: Table 'customer_payments' does not exist
├── Fallback Action: Consult GraphDB for similar table names
├── Alternative Found: ['invoices', 'payments', 'customer_invoices']
├── New Approach: Reconstruct using available tables
└── Success Rate: 78% of schema failures recovered

Example Fallback Chain:
1. customer_payments (not found) 
   → 2. invoices + payments (LEFT JOIN)
   → 3. customer_billing (alternative naming)
```

**Layer 2: Data Scope Fallback (untuk No Data Found)**
```
Primary Query Failed: No data for "January 2023"
├── Strategy 1: Expand date range (Dec 2022 - Feb 2023)
├── Strategy 2: Check data availability in adjacent periods  
├── Strategy 3: Suggest alternative time granularity (Q1 2023)
├── User Notification: "Data for Jan 2023 not found, showing Q1 2023"
└── Success Rate: 65% of date range issues resolved

Intelligent Date Expansion:
• Monthly → Quarterly
• Specific dates → Date ranges  
• Current year → Previous year comparison
```

**Layer 3: Query Complexity Fallback (untuk Complex Query Failures)**
```
Primary Query Failed: Complex multi-table JOIN timeout
├── Fallback 1: Simplify to single-table aggregations
├── Fallback 2: Break complex query into smaller parts
├── Fallback 3: Use cached/pre-computed data if available
├── User Communication: Explain complexity reduction
└── Success Rate: 85% of complex queries simplified successfully

Complexity Reduction Pattern:
• 5-table JOIN → 2-table JOIN + manual aggregation
• Complex calculations → Basic SUM/COUNT operations
• Real-time data → Last cached snapshot
```

### Fallback Communication Strategy

**User-Friendly Error Explanations**
```
🤖 Agent Reasoning:

"I couldn't find the exact data you requested, but here's what I found instead:

❌ Original Request: Customer payment data for January 2023
❌ Issue Found: The 'customer_payments' table doesn't exist in your database

✅ Alternative Approach: I analyzed invoice and payment records to calculate outstanding amounts
✅ Data Found: 3 customers with unpaid invoices from that period
✅ Confidence Level: High (same business logic, different data source)

Would you like me to:
• Show the detailed invoice-payment analysis
• Search for payment data in other time periods  
• Explain how I reconstructed the payment status"
```

**Technical Fallback Logging**
```
Fallback Attempt #1:
├── Original Query: SELECT * FROM customer_payments WHERE date = '2023-01'
├── Error: mysql.connector.errors.ProgrammingError: Table doesn't exist
├── GraphDB Consultation: Found alternative tables [invoices, payments]
├── Reconstructed Query: SELECT i.customer_id, SUM(i.amount - COALESCE(p.amount, 0))...
├── Result: SUCCESS - 156 records found
└── User Impact: Minimal (same business meaning, different technical approach)

Fallback Attempt #2: (if #1 failed)
├── Simplified Scope: Expand date range to Q1 2023
├── Alternative Tables: Use billing_summary table
├── Reduced Precision: Monthly → Quarterly aggregation
└── User Notification: Explain scope change and impact
```

## 9. Performance Monitoring & Analytics Infrastructure

### Real-Time Performance Tracking

**Component-Level Performance Monitoring**
```python
class PerformanceMonitor:
    def __init__(self):
        self.timings = {
            "llm_api_calls": [],
            "graphdb_queries": [],
            "sql_execution": [],
            "data_processing": [],
            "context_management": []
        }
        
    def track_component(self, component: str, duration: float):
        self.timings[component].append({
            "duration": duration,
            "timestamp": datetime.now(),
            "context_size": current_context_tokens,
            "query_complexity": complexity_score
        })
        
    def get_performance_summary(self):
        return {
            "total_time": sum(all_durations),
            "breakdown": {
                component: {
                    "avg_time": mean(durations),
                    "percentage": (sum(durations) / total_time) * 100
                }
            },
            "bottlenecks": identify_slowest_components(),
            "optimization_suggestions": generate_optimizations()
        }
```

**Token Usage Analytics**
```
📊 Context Window Analytics

Real-Time Usage:
├── Current Session: 15,240 tokens (78% of limit)
├── Rate of Growth: +245 tokens/query (avg)
├── Projected Capacity: 17 more queries before limit
└── Optimization Potential: 32% reducible content

Token Distribution:
├── Schema Knowledge: 8,950 tokens (58.7%) [Cacheable]
├── Query Results: 4,780 tokens (31.4%) [Archivable]  
├── Conversation History: 1,465 tokens (9.6%) [Compressible]
└── System Context: 45 tokens (0.3%) [Fixed]

Optimization Opportunities:
• Archive old query results: -2,400 tokens
• Compress conversation history: -730 tokens
• Cache stable schema info: -1,200 tokens
• Total Recoverable: 4,330 tokens (28% reduction)
```

**Quality & Success Rate Monitoring**
```
📈 Agent Performance Analytics

Session Statistics:
├── Query Success Rate: 85.7% (6/7 queries successful)
├── Average Response Time: 8.4 seconds (Target: <10s) ✅
├── Data Quality Score: 94.2/100 (Average across all queries)
├── User Satisfaction: Pending feedback
└── Fallback Utilization: 42.9% (3/7 queries used fallbacks)

Trend Analysis:
├── Response Time Trend: Improving (-1.2s over last 5 queries)
├── Success Rate Trend: Stable (85-90% range maintained)
├── Context Efficiency: Declining (need optimization)
└── Query Complexity: Increasing (user getting more advanced)

Optimization Alerts:
⚠️ Context approaching 80% capacity - suggest cleanup
✅ Response times within target range
⚠️ Fallback usage above 40% - check data quality
✅ Schema knowledge cache hit rate: 95%
```

### Adaptive Performance Optimization

**Smart Context Management**
```
🧠 Intelligent Context Optimization

Automatic Optimizations Applied:
├── ✅ Compressed old conversation turns (freed 890 tokens)
├── ✅ Cached frequently accessed schema (saved 1.2s per query)
├── ✅ Archived query results older than 30 minutes
└── ⏳ Scheduled cleanup of temporary calculations

User-Controlled Optimizations:
├── 🔄 Archive Conversation History: Will free 1,465 tokens
├── 🗑️ Clear Old Query Results: Will free 2,780 tokens  
├── ⚙️ Reset Technical State: Will free 680 tokens
└── 🆕 Start Fresh Session: Complete reset (3s reload time)

Predictive Management:
├── Estimated queries until context full: 12-15 queries
├── Suggested cleanup timing: After 5 more queries
├── Performance impact of cleanup: Minimal (<0.5s delay)
└── Data loss risk: None (important data preserved)
```

**Adaptive Query Strategy**
```
🎯 Smart Query Optimization

Learning from Previous Queries:
├── ✅ Invoice-payment JOIN pattern successful → Cached for reuse
├── ✅ Date range expansion (monthly→quarterly) worked → Saved strategy
├── ❌ Complex 5-table JOIN failed → Avoid similar patterns
└── ✅ Customer aging analysis optimized → 40% faster execution

Dynamic Strategy Adjustment:
├── Database Response Time: Fast (avg 0.8s) → Use complex queries
├── Context Usage: High (78%) → Prefer simpler responses
├── User Expertise Level: Intermediate → Balance detail vs clarity
└── Session Duration: Long (15 mins) → Prioritize efficiency

Next Query Predictions:
├── Likely to ask: Follow-up about payment collections (68% confidence)
├── Suggested prep: Cache payment terms and collection policies
├── Expected complexity: Medium (similar to current query)
└── Optimization strategy: Use cached invoice data, minimize LLM calls
```

## 10. Development Phases dengan Monitoring Integration

### Phase 1: Foundation + Basic Monitoring (4-5 hari)
- Setup development environment (LangGraph, Graphiti, FastAPI)
- Implement SQL file parser untuk extract schema dan data
- Basic SQLite in-memory database setup
- **NEW**: Basic performance timing infrastructure
- **NEW**: Token counting dan context tracking
- **NEW**: Simple progress bar untuk process monitoring
- Test koneksi antar komponen dengan timing metrics

### Phase 2: Schema Knowledge Base + Monitoring (3-4 hari)
- Implement Graphiti integration untuk schema storage
- Develop automatic schema analysis dan categorization
- Create knowledge consultation functions
- **NEW**: GraphDB query timing dan optimization
- **NEW**: Schema cache untuk performance improvement
- **NEW**: Real-time schema knowledge loading indicators
- Test schema query capabilities dengan performance benchmarks

### Phase 3: Core Workflow + Fallback System (5-6 hari)
- Implement LangGraph workflow nodes dengan timing tracking
- Develop placeholder system dan template generation
- Create SQL query execution engine dengan validation
- **NEW**: Three-layer fallback mechanism implementation
- **NEW**: Intelligent retry logic dengan user communication
- **NEW**: Fallback success tracking dan analytics
- **NEW**: Real-time process status updates
- Implement placeholder replacement mechanism

### Phase 4: Advanced Monitoring & Analytics (3-4 hari)
- **NEW**: Comprehensive performance monitoring dashboard
- **NEW**: Context window optimization system
- **NEW**: Token usage analytics dan predictions
- **NEW**: Quality scoring dan success rate tracking
- **NEW**: Adaptive query strategy implementation
- **NEW**: User session management dan reset capabilities
- Develop data quality scoring dengan real-time feedback

### Phase 5: User Interface + Real-Time Features (4-5 hari)
- Develop FastAPI endpoints dengan performance monitoring
- Create React frontend dengan real-time progress indicators
- **NEW**: Live process monitoring dashboard
- **NEW**: Context usage meters dan optimization suggestions
- **NEW**: Fallback explanation interface
- **NEW**: Session management controls
- **NEW**: Performance analytics display
- Implement real-time query processing dengan timing breakdown

### Phase 6: Polish, Testing & Optimization (3-4 hari)
- Comprehensive testing dengan performance benchmarking
- **NEW**: Fallback scenario testing (all 3 layers)
- **NEW**: Context optimization testing
- **NEW**: Performance regression testing
- **NEW**: User experience testing dengan monitoring features
- Bug fixes dan edge case handling
- Documentation dan user guides untuk monitoring features

**Total Development Time: 22-28 hari kerja** (increased due to monitoring features)

## 11. Enhanced Success Metrics untuk MVP

### Functional Success Criteria
- ✅ Agent dapat memahami 80% natural language queries tentang sales, customer, employee
- ✅ Zero manual calculations by LLM (semua via SQL aggregations)
- ✅ Raw data table always displayed untuk transparency
- ✅ Placeholder system working 100% (no leaked numbers to LLM)
- ✅ **NEW**: Real-time process monitoring dengan 95% accuracy
- ✅ **NEW**: Fallback system success rate >70% untuk recoverable errors
- ✅ **NEW**: Context optimization suggestions 90% relevant

### Performance Success Criteria
- ✅ **NEW**: Total response time <15 seconds untuk typical queries
- ✅ **NEW**: Individual component timing accuracy ±0.1 seconds
- ✅ **NEW**: Context usage prediction accuracy >85%
- ✅ **NEW**: Token counting accuracy 100%
- ✅ **NEW**: Performance monitoring overhead <5% of total time
- ✅ **NEW**: Fallback execution time <2x original query time

### User Experience Success Criteria
- ✅ **NEW**: Process visibility: User always knows what agent is doing
- ✅ **NEW**: Progress indication accuracy >90%
- ✅ **NEW**: Fallback explanations clear dan actionable untuk 80% users
- ✅ **NEW**: Context optimization suggestions reduce usage by >20%
- ✅ **NEW**: Session management works seamlessly (reset <3s)
- ✅ **NEW**: Performance dashboard provides actionable insights

### Monitoring & Analytics Success Criteria
- ✅ **NEW**: Component timing breakdown accuracy >95%
- ✅ **NEW**: Context usage prediction within 5% margin
- ✅ **NEW**: Fallback pattern recognition >80% accurate
- ✅ **NEW**: Performance bottleneck identification 100% accurate
- ✅ **NEW**: Quality score correlation with user satisfaction >75%
- ✅ **NEW**: Session analytics provide useful optimization insights

## 12. Risk Mitigation dengan Enhanced Monitoring

### Technical Risks
- **Risk**: LLM menggenerate angka palsu
- **Mitigation**: Strict placeholder system, no number exposure to LLM
- **NEW Monitoring**: Real-time placeholder tracking, leak detection alerts

- **Risk**: SQL query gagal atau lambat  
- **Mitigation**: Query validation, fallback simpler queries, timeout handling
- **NEW Monitoring**: Query performance tracking, automatic optimization suggestions

- **Risk**: Context window overflow
- **NEW Mitigation**: Predictive context management, automatic cleanup, usage alerts
- **NEW Monitoring**: Real-time token tracking, optimization recommendations

### Performance Risks
- **NEW Risk**: Monitoring overhead impacts performance
- **NEW Mitigation**: Lightweight tracking, async logging, performance budgets
- **NEW Monitoring**: Self-monitoring of monitoring overhead

- **NEW Risk**: Fallback loops (infinite retry scenarios)
- **NEW Mitigation**: Maximum 3 attempts, circuit breaker pattern, intelligent backoff
- **NEW Monitoring**: Fallback pattern detection, loop prevention alerts

### User Experience Risks
- **Risk**: User confusion about agent capabilities
- **NEW Mitigation**: Clear process visibility, fallback explanations, progress indicators
- **NEW Monitoring**: User interaction analytics, confusion point detection

- **NEW Risk**: Information overload from too much monitoring data
- **NEW Mitigation**: Progressive disclosure, customizable dashboards, smart defaults
- **NEW Monitoring**: User engagement metrics, feature usage analytics

## 11. Future Enhancement Opportunities

### Near-term Enhancements (Post-MVP)
- Support untuk multiple SQL source files
- Advanced data visualization (charts, graphs)
- Query optimization suggestions
- Historical data comparison features

### Long-term Vision
- Integration dengan live database systems
- Advanced AI reasoning untuk complex business questions
- Automated report generation dan scheduling
- Multi-language support untuk international use

Rancangan ini memberikan foundation solid untuk MVP yang fokus pada akurasi, transparency, dan user trust melalui pembagian peran yang jelas antara AI reasoning dan mathematical computation.