### **Dokumen Konteks Proyek Komprehensif: AI Agent untuk Query Database MySQL**

**Versi Dokumen**: 1.0
**Tanggal Pembuatan Dokumen Ini**: (Tanggal saat ini Anda membaca ini)

---

## **Bab 1: Pendahuluan dan Tujuan Proyek**

### **1.1 Peran Anda sebagai Asisten LLM dalam Proyek Ini**

Selamat datang dalam proyek pengembangan "AI Agent untuk Query Database MySQL". Peran Anda dalam proyek ini adalah sebagai **Asisten Pengembangan AI yang Ahli, Teliti, dan Proaktif**. Anda bertugas untuk membantu developer utama (saya) dalam berbagai aspek siklus pengembangan, termasuk:
*   Menulis, merevisi, dan men-debug kode Python (khususnya untuk FastAPI, SQLAlchemy ORM, dan LangGraph).
*   Membantu merancang dan menyempurnakan prompt untuk Model Bahasa Besar (LLM).
*   Memberikan analisis terhadap error dan menyarankan solusi berdasarkan informasi yang ada.
*   Membantu menyusun dan memperbarui dokumentasi proyek ini.
*   Memahami dan mengikuti arsitektur, prinsip desain, serta rencana pengembangan yang telah ditetapkan.

**Instruksi Kunci untuk Anda (Asisten LLM):**

1.  **Acuan Utama**: Dokumen Konteks Proyek Komprehensif ini adalah sumber pengetahuan utama Anda. Harap selalu merujuk ke sini terlebih dahulu sebelum memberikan saran atau memulai tugas.
2.  **Permintaan File Kode Spesifik**: Jika Anda memerlukan detail implementasi dari file kode tertentu untuk melakukan revisi, memahami konteks lebih dalam, atau memberikan solusi yang akurat, **mintalah saya untuk mengunggah HANYA file yang relevan tersebut**. Jangan meminta seluruh codebase.
    *   *Contoh Permintaan*: "Untuk melanjutkan refactoring `execute_query_node` agar menggunakan ORM, saya perlu melihat isi file `backend/app/langgraph_workflow/nodes/execute_query.py` (versi saat ini) dan definisi `DatabaseOperationPlan` dari `backend/app/schemas/agent_state.py`."
3.  **Gaya Revisi dan Pemberian Kode**:
    *   **Prioritaskan Traceback**: Jika saya melaporkan error, selalu minta dan analisis *traceback error Python lengkap* dari terminal saya sebagai langkah pertama.
    *   **Perubahan Terisolasi (Jika Memungkinkan)**: Untuk perbaikan kecil, berikan hanya bagian kode yang perlu diubah, idealnya dengan format "Sebelum Perbaikan:" dan "Sesudah Perbaikan:", atau dengan instruksi jelas "Ubah X menjadi Y". Ini memudahkan saya melakukan copy-paste.
        *Contoh:*
        *Ubah baris berikut di `namafile.py` pada class `NamaKelas` fungsi `nama_fungsi`:*
        *Sebelum Perbaikan:*
        ```python
        # return some_value + another_value # Contoh baris salah
        ```
        *Menjadi ini:*
        ```python
        return some_value - another_value
        ```
    *   **File Utuh untuk Perubahan Luas**: Jika revisi melibatkan banyak bagian file, refactoring signifikan, atau pembuatan file baru, Anda boleh memberikan seluruh konten file yang diperbarui. Namun, selalu sertakan ringkasan perubahan utama yang dilakukan.
    *   **Path File di Awal Blok Kode**: Selalu sertakan path file di baris paling atas blok kode yang Anda berikan (misalnya, `# backend/app/db_models/master_data_models.py`).
    *   **Tanpa Komentar Kode Internal Tambahan**: Hindari menambahkan komentar `#` atau `//` baru di dalam kode yang Anda berikan, kecuali jika itu adalah bagian dari konvensi yang sudah ada di file tersebut atau sangat krusial untuk menjelaskan baris tertentu yang sangat kompleks (dan itupun, gunakan dengan hemat).
    *   **Jelaskan Alasan Perubahan**: Berikan justifikasi singkat mengapa perubahan tersebut diperlukan dan bagaimana itu mengatasi masalah atau memenuhi permintaan.
    *   **Minta Konfirmasi dan Hasil**: Setelah memberikan solusi atau kode baru, selalu minta saya untuk menerapkan perubahan dan melaporkan hasilnya (log terminal, output Postman, atau status terbaru).
    *   **Jika Bingung atau Butuh Info Lebih Lanjut**: Jika Anda merasa buntu, informasi kurang, atau menghadapi masalah desain yang kompleks, jangan ragu untuk:
        *   Meminta file kode spesifik tambahan.
        *   Meminta klarifikasi mengenai bagian tertentu dari dokumen ini.
        *   Meminta saya untuk merujuk pada dokumentasi library spesifik (misalnya, "Untuk memastikan penggunaan `primaryjoin` yang benar pada kasus FK komposit ini, bisakah Anda meminta AI Agent Researcher untuk memberikan contoh sintaks dari dokumentasi SQLAlchemy versi X.Y terkait `relationship` dengan kondisi join komposit?").
        *   Membantu saya menyusun pertanyaan yang jelas dan terstruktur yang bisa saya ajukan kepada "AI Agent Researcher" (pakar manusia) saya.
4.  **Pahami Konteks MVP**: Meskipun kita mungkin membahas fitur lanjutan, selalu ingat bahwa fokus utama adalah menyelesaikan fungsionalitas MVP terlebih dahulu sesuai rencana.
5.  **Ketelitian**: Periksa kembali setiap saran kode, nama file, path, dan logika untuk meminimalkan kesalahan.

### **1.2 Tujuan Utama Proyek MVP (Most Viable Product)**

Tujuan utama dari proyek ini adalah membangun sebuah **AI Agent MVP** yang memiliki kemampuan sebagai berikut:

1.  **Memahami Pertanyaan Bisnis Pengguna**: Menerima input dari pengguna berupa pertanyaan dalam bahasa alami (Bahasa Indonesia) mengenai data yang tersimpan dalam database operasional perusahaan (MySQL bernama `sim_testgeluran`).
2.  **Konsultasi Metadata Skema**: Menggunakan Graphiti (Neo4j sebagai backend) untuk mengambil metadata skema yang relevan dan diperkaya secara semantik guna memahami struktur data yang akan di-query.
3.  **Merencanakan Operasi Database (Bukan SQL Langsung)**: Mampu menganalisis query pengguna dan, dengan bantuan metadata skema, merencanakan serangkaian operasi database terstruktur (dalam format JSON, disebut `DatabaseOperationPlan`) yang diperlukan untuk mengambil data yang relevan. LLM bertanggung jawab untuk perencanaan ini.
4.  **Membangun dan Mengeksekusi Query ORM secara Aman**: Mengonversi `DatabaseOperationPlan` menjadi query yang valid dan aman menggunakan SQLAlchemy ORM di sisi Python, lalu mengeksekusinya ke database MySQL `sim_testgeluran`.
5.  **Menyajikan Hasil dengan Jelas dan Transparan**: Menampilkan hasil kepada pengguna dalam beberapa bentuk:
    *   **Analisis Naratif**: Memberikan ringkasan atau penjelasan dalam bahasa alami yang mudah dimengerti. Angka dalam narasi ini diisi melalui *placeholder strategy* (nilai dihitung oleh Python/DB, LLM hanya membuat template narasi).
    *   **Tabel Data Mentah/Detail**: Menyajikan data pendukung yang diambil langsung dari database untuk transparansi dan verifikasi pengguna.
    *   **Ringkasan Eksekutif**: Poin-poin kunci dari hasil analisis.
    *   **Informasi Sumber Data**: Memberikan informasi mengenai tabel mana saja yang digunakan untuk menghasilkan jawaban dan bagaimana tabel-tabel tersebut digabungkan.
6.  **Penanganan Error yang Baik**: Memberikan feedback yang informatif kepada pengguna jika terjadi kesalahan dalam pemrosesan query.

### **1.3 Prinsip Desain Kunci Proyek**

Pengembangan MVP ini berpegang pada beberapa prinsip desain fundamental:

*   **LLM sebagai Perencana, Python/ORM sebagai Eksekutor**: Model Bahasa Besar (LLM) **tidak** menulis string query SQL secara langsung. LLM bertugas untuk pemahaman bahasa alami (NLU), perencanaan operasi database dalam format terstruktur (`DatabaseOperationPlan`), dan pembuatan template narasi dengan placeholder. Kode Python, dengan bantuan SQLAlchemy ORM, bertanggung jawab untuk menerjemahkan `DatabaseOperationPlan` menjadi query ORM yang valid dan aman, lalu mengeksekusinya.
*   **Zero Manual Calculation by LLM**: Semua kalkulasi angka (finansial, kuantitatif) harus dilakukan oleh database (melalui query ORM yang dibangun Python) atau oleh sistem Python secara deterministik. LLM tidak boleh melakukan perhitungan matematis.
*   **Transparency First**: Semua data mentah yang digunakan untuk menghasilkan analisis atau angka dalam narasi harus dapat ditampilkan kepada pengguna. Informasi sumber data (tabel, logika join utama) juga harus disertakan dalam respons.
*   **Placeholder Strategy untuk Narasi**: LLM menghasilkan template narasi yang berisi placeholder (misalnya, `{{TOTAL_SALES_JANUARI}}`). Sistem Python akan mengganti placeholder ini dengan nilai aktual yang telah dihitung dan diformat sebelum ditampilkan ke pengguna.
*   **Keamanan dan Keandalan Query**: Penggunaan ORM (SQLAlchemy) ditujukan untuk meningkatkan keamanan (mencegah SQL injection melalui parameterisasi otomatis) dan keandalan (mengurangi error sintaks SQL) dibandingkan membangun string SQL secara manual.
*   **Fokus Fungsionalitas MVP**: Prioritas utama adalah pada akurasi data, alur kerja end-to-end yang andal untuk skenario query yang telah ditentukan untuk MVP, dan penanganan error yang baik.

### **1.4 Stack Teknologi Utama**

Proyek ini menggunakan kombinasi teknologi berikut:

*   **Bahasa Pemrograman Utama**: Python (versi 3.10+)
*   **Backend API Server**: FastAPI
*   **Workflow Orchestration (AI Agent Core)**: LangGraph
*   **Natural Language Understanding & Planning**: LLM DeepSeek (diakses melalui API yang kompatibel dengan OpenAI).
*   **Database Operasional**: MySQL (Database target bernama `sim_testgeluran`).
*   **Object-Relational Mapper (ORM)**: SQLAlchemy (untuk interaksi dengan MySQL).
*   **Knowledge Graph (Metadata Skema)**: Graphiti (dengan Neo4j sebagai database backend-nya, diakses melalui driver Python Neo4j untuk sinkronisasi dan konsultasi skema oleh agent).
*   **Manajemen Konfigurasi**: File `.env` dan modul `config.py`.
*   **Definisi Skema Data/State**: Pydantic dan `typing.TypedDict`.
*   **Frontend Interface (Akan Datang)**: React.js (JavaScript).
*   **Testing**: Skrip Python kustom (untuk tes ORM dan logika), dan potensi penggunaan `pytest` untuk unit/integration testing di masa depan jika diperlukan.
*   **Abstraksi Tools/Layanan Eksternal (Konsep)**: Meskipun arsitektur awal merencanakan Model Context Protocol (MCP) Servers terpisah, untuk MVP saat ini, logika interaksi dengan Neo4j (untuk skema) dan MySQL (untuk eksekusi data dengan ORM) serta sistem placeholder diimplementasikan **secara inline** di dalam node-node LangGraph yang relevan untuk menyederhanakan pengembangan awal.

---

## **Bab 2: Arsitektur Sistem Keseluruhan**

Bab ini menjelaskan arsitektur umum dari sistem AI Agent, komponen-komponen utamanya, alasan penggunaan ORM, dan bagaimana data mengalir di antara mereka. Pemahaman arsitektur ini penting untuk mengetahui bagaimana setiap bagian berkontribusi pada fungsionalitas keseluruhan.

### **2.1 Komponen Utama Sistem**

Sistem AI Agent MVP terdiri dari beberapa komponen utama yang saling berinteraksi:

1.  **Pengguna (User)**: Entitas eksternal (misalnya, seorang analis bisnis, manajer) yang berinteraksi dengan sistem melalui antarmuka pengguna untuk mengajukan pertanyaan bisnis.
2.  **Frontend (React.js - Akan Datang)**: Antarmuka pengguna berbasis web yang bertanggung jawab untuk:
    *   Menerima input query dari pengguna.
    *   Mengirimkan query ke Backend API Server.
    *   Menerima dan menampilkan respons (narasi, tabel data, informasi sumber data, ringkasan, peringatan) dari backend.
3.  **Backend API Server (FastAPI - Python)**: Bertindak sebagai gerbang utama dan lapisan orkestrasi permintaan. Tugasnya meliputi:
    *   Mengekspos endpoint API (misalnya, `POST /api/v1/query`) untuk menerima permintaan dari Frontend.
    *   Memvalidasi permintaan masuk menggunakan model Pydantic.
    *   Memanggil dan mengelola eksekusi LangGraph Workflow melalui `AgentService`.
    *   Memformat hasil dari LangGraph Workflow menjadi respons API standar untuk Frontend.
    *   Menangani error umum dan mengirimkan respons error yang sesuai.
4.  **LangGraph Workflow (AI Agent Core - Python)**: Ini adalah inti logika AI agent, diimplementasikan menggunakan `langgraph.graph.StateGraph`. Bertanggung jawab untuk mengorkestrasi serangkaian langkah (node) yang diperlukan untuk memproses query pengguna, dengan mengelola `AgentState`. Node-node utamanya adalah:
    *   `understand_query_node`: Memahami query pengguna menggunakan LLM.
    *   `consult_schema_node`: Mengambil metadata skema dari Graphiti (Neo4j).
    *   `plan_execution_node`: Merencanakan `DatabaseOperationPlan` dan template respons menggunakan LLM.
    *   `execute_query_node`: Menerjemahkan `DatabaseOperationPlan` menjadi query SQLAlchemy ORM, lalu mengeksekusinya ke database MySQL.
    *   `validate_results_node`: Memvalidasi hasil query.
    *   `replace_placeholders_node`: Mengisi template respons dengan data, menyiapkan output akhir.
    *   `generate_error_response_node`: Menangani pembuatan respons error.
5.  **Model Bahasa Besar (LLM - DeepSeek)**: Digunakan oleh node `understand_query_node` dan `plan_execution_node` untuk tugas pemahaman bahasa alami, ekstraksi entitas, dan perencanaan `DatabaseOperationPlan`.
6.  **Database Operasional (MySQL - `sim_testgeluran`)**: Sumber data utama yang berisi data bisnis aktual. AI agent akan melakukan query `SELECT` (melalui SQLAlchemy ORM) ke database ini.
7.  **Knowledge Graph (Graphiti - Neo4j sebagai backend)**: Menyimpan metadata skema database MySQL `sim_testgeluran` yang diperkaya dengan informasi semantik (seperti `purpose`, `classification`, `is_aggregatable`, dan definisi relasi dari `graphiti_semantic_mapping.json`). Ini adalah sumber informasi krusial bagi agent untuk memahami struktur data.
8.  **SQLAlchemy ORM Layer (Python)**: Lapisan abstraksi antara logika agent (khususnya `execute_query_node`) dan database MySQL. Ini adalah komponen kunci yang sedang kita implementasikan secara komprehensif.
    *   **Definisi Model**: Kelas-kelas Python di `backend/app/db_models/` yang merepresentasikan tabel-tabel di `sim_testgeluran`.
    *   **Engine & Session**: Dikelola di `backend/app/db/session.py` untuk koneksi dan transaksi database.

### **2.2 Mengapa Menggunakan Object-Relational Mapper (ORM) - SQLAlchemy?**

Sebelumnya, AI Agent kita menggunakan pendekatan di mana LLM Planner (di `plan_execution_node`) menghasilkan sebuah `DatabaseOperationPlan` (struktur JSON), kemudian node `execute_query_node` memiliki fungsi Python kustom (`_build_sql_from_operation`) yang membangun string query SQL secara dinamis dari rencana tersebut untuk dieksekusi ke MySQL.

Meskipun pendekatan ini lebih baik daripada LLM menghasilkan SQL mentah, kita menghadapi tantangan:
1.  **Kompleksitas Fungsi Pembangun SQL Kustom**: Fungsi `_build_sql_from_operation` menjadi sangat kompleks dan rentan terhadap kesalahan jika `DatabaseOperationPlan` dari LLM memiliki variasi yang belum sepenuhnya tertangani, atau jika kita perlu mendukung operasi SQL yang lebih canggih.
2.  **Presisi `DatabaseOperationPlan` dari LLM**: Memastikan LLM secara konsisten menghasilkan `DatabaseOperationPlan` yang 100% benar dan lengkap untuk semua jenis query (terutama agregasi kompleks atau join multi-tabel) adalah tugas yang sulit dan memerlukan *prompt engineering* yang sangat detail dan iteratif.

Untuk mengatasi tantangan ini, kita mengintegrasikan **SQLAlchemy ORM** dengan tujuan utama:
*   **Meningkatkan Keandalan dan Keamanan**: Memanfaatkan kemampuan SQLAlchemy yang sudah teruji dalam membangun query SQL yang valid dan aman. SQLAlchemy secara otomatis menangani parameterisasi query, yang merupakan pertahanan utama terhadap SQL injection.
*   **Menyederhanakan Logika Pembangunan Query**: Mengurangi kompleksitas dan potensi bug pada fungsi kustom `_build_sql_from_operation`. Tugas berat membangun sintaks SQL yang benar diserahkan kepada ORM. `execute_query_node` akan lebih fokus pada menerjemahkan semantik `DatabaseOperationPlan` ke konstruksi ORM yang lebih tinggi levelnya.
*   **Meningkatkan Kemudahan Pemeliharaan dan Keterbacaan Kode**: Kode interaksi database menjadi lebih Pythonic, menggunakan objek dan metode, yang cenderung lebih mudah dipahami dan dipelihara oleh developer Python.
*   **Potensi Menyederhanakan `DatabaseOperationPlan` di Masa Depan**: Setelah ORM terimplementasi dengan baik, LLM Planner mungkin bisa menghasilkan rencana operasi yang lebih abstrak atau semantik, karena detail implementasi SQL spesifik sudah ditangani oleh ORM. Ini bisa mengurangi beban kognitif pada LLM untuk menghasilkan struktur rencana yang sangat rinci.

Dengan ORM, kita memindahkan sebagian besar beban "penerjemahan rencana ke SQL" ke library yang sudah matang dan teruji, sehingga kita bisa lebih fokus pada kualitas perencanaan (`DatabaseOperationPlan`) oleh LLM dan logika bisnis di sekitarnya.

### **2.3 Diagram Aliran Data (DFD) Level 0: Konteks Sistem (dengan ORM)**
```mermaid
graph LR
    User([Pengguna]) -->|1. User Query via Frontend| AI_System{AI Agent System (Backend & LangGraph)};
    AI_System -->|2. Laporan & Analisis via Frontend| User;
    AI_System -- Komunikasi via SQLAlchemy ORM -->|3. Akses Data Aktual| ERP_MySQL[(Database ERP MySQL - sim_testgeluran)];
    AI_System -- Komunikasi via Python Driver Neo4j -->|4. Akses Metadata Skema| Graphiti_KG[(Graphiti Knowledge Graph - Neo4j)];
    AI_System -- Komunikasi via API -->|5. Interaksi NLU & Planning| LLM_DeepSeek[LLM DeepSeek];

    style User fill:#d3f8d3,stroke:#333,stroke-width:2px
    style AI_System fill:#c3ddf9,stroke:#333,stroke-width:2px
    style ERP_MySQL fill:#f9e79f,stroke:#333,stroke-width:2px
    style Graphiti_KG fill:#f5cba7,stroke:#333,stroke-width:2px
    style LLM_DeepSeek fill:#f8cdda,stroke:#333,stroke-width:2px
```
*   **Perubahan Utama**: Aliran data ke `ERP_MySQL` sekarang dimediasi oleh SQLAlchemy ORM di dalam `AI_System`.

### **2.4 Diagram Aliran Data (DFD) Level 1: Alur Proses Utama dalam AI Agent System (dengan ORM)**
```mermaid
graph TD
    A[User Query via Frontend] --> B{Backend API (FastAPI)};
    B --> C[Memulai LangGraph Workflow dengan AgentState Awal \n (via AgentService)];
    
    subgraph LangGraph Workflow (State: AgentState)
        direction LR
        N1[Node: understand_query \n (Call LLM DeepSeek)] --> N2[Node: consult_schema \n (Query Neo4j Python Driver)];
        N2 --> N3[Node: plan_execution \n (Call LLM DeepSeek -> DatabaseOperationPlan)];
        N3 --> N4[Node: execute_query \n (DatabaseOperationPlan -> SQLAlchemy ORM Query -> Eksekusi ke MySQL)];
        N4 --> N5[Node: validate_results];
        N5 -- Validasi Sukses/Peringatan --> N6[Node: replace_placeholders \n (Logika Formatting Inline)];
        N6 --> F[Hasil Akhir (Narasi, Tabel, dll.) \n ditambahkan ke AgentState];
        
        %% Jalur Error (Sederhana)
        N1 -->|Error| NE[Node: generate_error_response];
        N2 -->|Error| NE;
        N3 -->|Error| NE;
        N4 -->|Error| NE;
        N5 -- Validasi Gagal Kritis --> NE; 
        NE --> G[Respons Error \n ditambahkan ke AgentState];
    end

    F --> H{AgentService di Backend API};
    G --> H;
    H --> I[Respons API (Sukses/Error) ke Frontend];
    I --> J[Tampilan ke Pengguna];

    style A fill:#e8daef,stroke:#333,stroke-width:1px
    style B fill:#e8daef,stroke:#333,stroke-width:1px
    style C fill:#c3ddf9,stroke:#333,stroke-width:1px
    style N1 fill:#e1effa,stroke:#333,stroke-width:1px
    style N2 fill:#e1effa,stroke:#333,stroke-width:1px
    style N3 fill:#e1effa,stroke:#333,stroke-width:1px
    style N4 fill:#e1effa,stroke:#333,stroke-width:1px
    style N5 fill:#e1effa,stroke:#333,stroke-width:1px
    style N6 fill:#e1effa,stroke:#333,stroke-width:1px
    style NE fill:#fadbd8,stroke:#c0392b,stroke-width:1px
    style F fill:#c3ddf9,stroke:#333,stroke-width:1px
    style G fill:#c3ddf9,stroke:#333,stroke-width:1px
    style H fill:#e8daef,stroke:#333,stroke-width:1px
    style I fill:#e8daef,stroke:#333,stroke-width:1px
    style J fill:#d3f8d3,stroke:#333,stroke-width:1px
```
*   **Perubahan Utama**: Deskripsi Node N4 (`execute_query`) sekarang secara eksplisit menyebutkan penerjemahan `DatabaseOperationPlan` ke query SQLAlchemy ORM sebelum eksekusi ke MySQL.

### **2.5 Penjelasan Interaksi Komponen Utama (dengan ORM)**

*   **Frontend - Backend API**: Komunikasi standar HTTP (request/response).
*   **Backend API (`AgentService`) - LangGraph Workflow**: `AgentService` menyiapkan `AgentState` awal dan memulai eksekusi alur LangGraph. Ia kemudian memproses `AgentState` akhir.
*   **LangGraph Nodes - LLM DeepSeek**: Node `understand_query_node` dan `plan_execution_node` membuat panggilan API HTTP ke LLM DeepSeek.
*   **`consult_schema_node` - Graphiti (Neo4j)**: Menggunakan driver Python `neo4j` untuk query metadata skema.
*   **`execute_query_node` - MySQL (via SQLAlchemy ORM)**:
    *   Node ini akan menerima `DatabaseOperationPlan` dari `plan_execution_node`.
    *   Menggunakan model-model ORM yang didefinisikan di `backend/app/db_models/` dan sesi SQLAlchemy dari `backend/app/db/session.py`.
    *   Menerjemahkan setiap `DatabaseOperation` menjadi konstruksi query SQLAlchemy (misalnya, `session.query(Model).filter(...).join(...).all()`).
    *   SQLAlchemy kemudian menghasilkan SQL yang sebenarnya dan mengeksekusinya ke database MySQL.
    *   Hasil dari ORM (biasanya list objek model atau tuple) dikonversi kembali ke format `List[Dict[str, Any]]` untuk `AgentState`.

Pemahaman arsitektur yang telah diperbarui ini, terutama peran dan manfaat ORM, akan menjadi dasar penting untuk langkah pengembangan selanjutnya.

Tentu. Saya telah menyiapkan Bab 3. Saya sudah melakukan double-check untuk memastikan struktur folder dan deskripsi file sesuai dengan kondisi terakhir proyek kita dan rencana ke depan.

---

## **Bab 3: Struktur Folder Proyek dan Deskripsi Komponen File**

Bab ini mendefinisikan struktur folder proyek AI Agent dan memberikan deskripsi untuk setiap direktori serta file Python kunci di dalamnya. Tujuannya adalah untuk memberikan peta navigasi kode bagi Asisten LLM dan developer.

### **3.1 Struktur Folder Utama (Backend Fokus, Frontend Placeholder)**

```
ai_agent_project_root/ (D:\3_Wings_mySQL)
├── backend/                          # Semua kode backend (FastAPI, LangGraph, SQLAlchemy ORM, dll.)
│   ├── app/                          # Direktori utama aplikasi FastAPI
│   │   ├── __init__.py
│   │   ├── api/                      # Modul untuk routing dan endpoint API
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           └── query.py      # Endpoint untuk /api/v1/query
│   │   ├── core/                     # Konfigurasi inti, settings
│   │   │   ├── __init__.py
│   │   │   └── config.py             # Settings aplikasi & konfigurasi LLM, DB, Neo4j
│   │   ├── db/                       # Konfigurasi dan sesi database SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   └── session.py            # Engine SQLAlchemy, SessionLocal, get_db_session
│   │   ├── db_models/                # Definisi model-model ORM SQLAlchemy
│   │   │   ├── __init__.py           # Impor & konfigurasi semua model dari file-file di bawah ini
│   │   │   ├── base.py               # Base = declarative_base()
│   │   │   ├── master_data_models.py # Model untuk tabel master (customer, material, dll.)
│   │   │   ├── sales_models.py       # Model untuk tabel sales & piutang (SalesOrder, Arbook, dll.)
│   │   │   ├── inventory_models.py   # Model untuk tabel inventaris (GoodsIssue, StockBalance, dll.)
│   │   │   ├── purchase_models.py    # Model untuk tabel pembelian (PurchaseOrder, Apbook, dll.)
│   │   │   ├── production_models.py  # Model untuk tabel produksi (JobOrder, MaterialUsage, dll.)
│   │   │   ├── finance_models.py     # Model untuk tabel finansial umum (GeneralJournal, dll.)
│   │   │   ├── hr_models.py          # Model untuk tabel HR (MasterEmployeeH, dll.)
│   │   │   ├── logistics_models.py   # Model untuk tabel logistik (Shipment, dll.)
│   │   │   └── system_models.py      # Model untuk tabel sistem (User, Role, dll.)
│   │   ├── schemas/                  # Pydantic models & TypedDicts untuk validasi dan state
│   │   │   ├── __init__.py
│   │   │   ├── api_models.py         # Model untuk request/response FastAPI (QueryRequest, QueryResponse)
│   │   │   ├── agent_state.py        # Definisi AgentState LangGraph & DatabaseOperationPlan
│   │   │   └── graphiti_schema_nodes.py # (Tidak digunakan lagi jika consult_schema langsung ke Neo4j)
│   │   ├── services/                 # Logika bisnis, interaksi dengan LangGraph
│   │   │   ├── __init__.py
│   │   │   └── agent_service.py      # Service untuk memproses query via LangGraph
│   │   └── langgraph_workflow/       # Komponen-komponen LangGraph
│   │       ├── __init__.py
│   │       ├── graph.py              # Definisi dan kompilasi graph utama LangGraph
│   │       └── nodes/                # Direktori untuk setiap node LangGraph
│   │           ├── __init__.py
│   │           ├── understand_query.py
│   │           ├── consult_schema.py
│   │           ├── plan_execution.py
│   │           ├── execute_query.py  # Akan direfactor untuk menggunakan ORM
│   │           ├── validate_results.py 
│   │           ├── replace_placeholders.py 
│   │           ├── generate_error_response.py
│   │           └── planning_prompts/ # Template prompt spesifik intent untuk plan_execution
│   │               ├── __init__.py
│   │               ├── customer_report_plan_prompt.py
│   │               └── default_plan_prompt.py
│   ├── .env                          # Variabel lingkungan backend (di-ignore Git)
│   └── requirements.txt              # Dependensi Python backend
│
├── frontend/                         # (Akan datang) Semua kode frontend (React.js)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│
├── docs/                             # Semua dokumen perencanaan
│   ├── 0_this_document_context.md    # (Dokumen ini)
│   ├── 1mvp_ai_agent_rancangan.md
│   ├── ... (dokumen perencanaan lain yang relevan)
│   └── sim_testgeluran_schema_report.txt
│
├── scripts/                          # Skrip-skrip pendukung
│   ├── extract_mysql_schema.py
│   ├── sync_mysql_to_graphiti.py
│   ├── convert_semantic_mapping_to_text.py
│   └── generate_orm_blueprint.py     # Skrip untuk membuat blueprint ORM dari model
│
├── data_samples/                     # File data sampel
│   ├── graphiti_semantic_mapping.json
│   ├── metadata.txt
│   ├── schema.sql
│   └── data.sql
│
├── tests/                            # Direktori untuk semua tes
│   ├── __init__.py
│   └── orm/                          # Tes spesifik untuk ORM
│       ├── __init__.py
│       ├── run_all_orm_tests.py      # Skrip untuk menjalankan semua tes ORM
│       ├── setup_test_schema.py      # Skrip untuk membuat skema di database tes
│       ├── data_factory.py           # Kelas TestDataFactory
│       ├── orm_blueprint.json        # File blueprint yang dihasilkan skrip
│       ├── test_orm_master_data.py
│       ├── test_orm_sales.py
│       └── test_orm_inventory.py     # Contoh file tes per kategori model
│   └── nodes/                        # Tes untuk node LangGraph (akan datang)
│       └── ...
│
├── .gitignore
└── README.md                         # Informasi umum proyek
```

### **3.2 Deskripsi Direktori Kunci di `backend/`**

   **3.2.1 `backend/app/`**
    *   **Tujuan**: Direktori utama aplikasi FastAPI yang berisi logika inti AI agent.
    *   **`main.py`**: Titik masuk aplikasi FastAPI.
        *   Fungsi/Kelas Utama: `app = FastAPI()`, pendaftaran router.
    *   **`api/v1/endpoints/query.py`**: Implementasi endpoint API.
        *   Fungsi/Kelas Utama: `router = APIRouter()`, `async def process_query_endpoint(...)`.
    *   **`core/config.py`**: Manajemen konfigurasi aplikasi.
        *   Fungsi/Kelas Utama: `class Settings`, `settings = Settings()`.
    *   **`db/session.py`**: Pengaturan koneksi dan sesi database SQLAlchemy.
        *   Fungsi/Kelas Utama: `engine`, `SessionLocal`, `engine_test`, `SessionTestLocal`, `def get_db_session()`, `def get_test_db_session()`.
    *   **`db_models/`**: Direktori untuk definisi model ORM SQLAlchemy.
        *   **`base.py`**: `Base = declarative_base()`.
        *   **`__init__.py`**: Titik pusat yang **mengimpor semua model** dari file-file kategori, lalu memanggil `configure_mappers()` untuk menyelesaikan semua relasi.
        *   **`master_data_models.py`**: Berisi kelas-kelas model ORM untuk tabel master data (misalnya, `MasterCustomer`, `MasterMaterial`). Setiap kelas merepresentasikan tabel, dengan `Column` untuk kolom dan `relationship` untuk relasi.
        *   **`sales_models.py`**: Berisi kelas-kelas model ORM untuk tabel transaksi penjualan dan piutang (misalnya, `SalesOrderH`, `Arbook`).
        *   (File model lainnya per kategori): Struktur serupa.
    *   **`schemas/`**: Model Pydantic dan `TypedDict` untuk validasi data dan struktur state.
        *   **`api_models.py`**: `QueryRequest`, `QueryResponseSuccess`, `QueryResponseError`, dll., untuk endpoint API.
        *   **`agent_state.py`**: Definisi `TypedDict` untuk `AgentState` LangGraph, termasuk struktur `DatabaseOperationPlan` dan sub-komponennya.
    *   **`services/agent_service.py`**: Logika bisnis, jembatan antara API dan LangGraph.
        *   Fungsi/Kelas Utama: `class AgentService` dengan metode `async def process_query(...)`.
    *   **`langgraph_workflow/`**: Komponen-komponen LangGraph.
        *   **`graph.py`**: Definisi `StateGraph`, penambahan node dan edge, kompilasi graph menjadi `app_graph`.
        *   **`nodes/`**: Setiap file `.py` di sini mengimplementasikan fungsi node LangGraph (misalnya, `understand_query_node`, `execute_query_node`).
            *   `planning_prompts/`: Sub-direktori berisi template prompt untuk LLM planner.

### **3.3 Deskripsi Direktori Lainnya**
*   **`docs/`**: Semua dokumen perencanaan dan referensi proyek, termasuk dokumen ini.
*   **`scripts/`**: Skrip Python utilitas untuk tugas seperti ekstraksi skema MySQL (`extract_mysql_schema.py`), sinkronisasi skema ke Graphiti (`sync_mysql_to_graphiti.py`), dan yang terpenting, **`generate_orm_blueprint.py`**.
*   **`data_samples/`**: File data penting seperti `graphiti_semantic_mapping.json` dan `metadata.txt`.
*   **`tests/orm/`**: Direktori untuk pengujian spesifik ORM.
    *   **`run_all_orm_tests.py`**: Skrip pusat untuk menjalankan semua file tes ORM.
    *   **`setup_test_schema.py`**: Skrip untuk membuat/menghapus skema tabel di database tes.
    *   **`data_factory.py`**: Kelas `TestDataFactory` yang menjadi "Pabrik Data" kita.
    *   **`orm_blueprint.json`**: "Blueprint" yang dihasilkan oleh `generate_orm_blueprint.py` dan digunakan oleh `TestDataFactory`.
    *   **`test_orm_*.py`**: File-file tes yang terisolasi untuk setiap modul (`master_data`, `sales`, `inventory`, dll.).

### **3.4 Koneksi Antar File dan Folder (Contoh Utama):**
*   `tests/orm/run_all_orm_tests.py` mengimpor dan memanggil fungsi dari `test_orm_master_data.py`, `test_orm_sales.py`, dll.
*   Semua file `test_orm_*.py` mengimpor `get_test_db_session` dari `backend/app/db/session.py` dan `TestDataFactory` dari `tests/orm/data_factory.py`.
*   `tests/orm/data_factory.py` membaca `tests/orm/orm_blueprint.json` dan mengimpor semua model dari `backend.app.db_models`.
*   `scripts/generate_orm_blueprint.py` mengimpor paket `backend.app.db_models` untuk memicu `__init__.py`.
*   `backend/app/db_models/__init__.py` adalah pusatnya, ia mengimpor semua model dari sub-modulnya lalu memanggil `configure_mappers()`.
*   Semua file node (misalnya, `execute_query.py`) akan mengimpor `AgentState` dan, setelah refactoring, akan mengimpor `get_db_session` dan model-model dari `backend.app.db_models`.

Struktur ini dirancang untuk modularitas, kejelasan, dan mendukung strategi testing otomatis yang baru kita rancang.

Tentu. Saya telah menyiapkan Bab 4. Saya sudah memeriksa ulang untuk memastikan detail definisi `AgentState` dan `DatabaseOperationPlan` konsisten dengan tujuan kita, serta alur kerja yang akan kita implementasikan, terutama pada node `execute_query` yang akan menggunakan ORM.

---

## **Bab 4: Detail Implementasi Inti (LangGraph Workflow dengan ORM)**

Bab ini akan menggali lebih dalam mengenai alur kerja (workflow) LangGraph yang merupakan inti dari AI Agent. Kita akan membahas struktur `AgentState` yang relevan, `DatabaseOperationPlan` yang menjadi target output LLM planner, alur antar node, dan detail operasional untuk setiap node, dengan penekanan pada bagaimana interaksi dengan SQLAlchemy ORM akan diintegrasikan, khususnya pada `execute_query_node`.

### **4.1 Definisi `AgentState` dan `DatabaseOperationPlan`**

   **4.1.1 `AgentState`**
    *   **Lokasi File Definisi**: `backend/app/schemas/agent_state.py`
    *   **Tipe Implementasi**: `typing.TypedDict` dengan `total=False`.
    *   **Tujuan**: Struktur data utama yang mengalir dan dimodifikasi melalui berbagai node dalam LangGraph. Membawa semua informasi dari input awal hingga output final.
    *   **Struktur Utama `AgentState` (Ringkasan Field Kunci)**:
        *   **Input & Konteks**: `user_query`, `session_id`, `conversation_history`.
        *   **Hasil NLU (`understand_query_node`)**: `intent`, `entities_mentioned`, `time_period`, `requested_metrics`, `query_complexity`.
        *   **Hasil Konsultasi Skema (`consult_schema_node`)**: `relevant_tables` (dari Neo4j), `table_relationships`, `financial_columns`, `temporal_columns`, `schema_consultation_warnings`.
        *   **Hasil Perencanaan Eksekusi (`plan_execution_node`)**:
            *   `database_operations_plan: Optional[List[DatabaseOperation]]` (Ini adalah rencana utama yang akan diproses oleh ORM).
            *   `raw_data_operation_plan: Optional[DatabaseOperation]` (Rencana untuk mengambil data mentah/detail, juga akan diproses ORM).
            *   `response_template: Optional[str]`
            *   `placeholder_mapping: Optional[Dict[str, Dict[str, Any]]]`
            *   `data_source_info: Optional[Dict[str, Any]]`
        *   **Hasil Eksekusi Query (`execute_query_node` dengan ORM)**:
            *   `financial_calculations: Optional[Dict[str, Any]]` (Hasil agregasi/kalkulasi dari query ORM).
            *   `raw_query_results: Optional[List[Dict[str, Any]]]` (Data mentah dari query ORM, sudah dalam format list of dict).
            *   `query_execution_status: Optional[str]`
            *   `query_execution_errors: Optional[List[Dict[str, str]]]`
        *   **Hasil Validasi (`validate_results_node`)**: `validation_status`, `validation_warnings`, `quality_score`.
        *   **Output Final (`replace_placeholders_node`)**: `final_narrative`, `data_table_for_display`, `executive_summary`, `warnings_for_display`.
        *   **Logging & Status Internal**: `current_node_name`, `error_message_for_user`, `technical_error_details`, `workflow_status`.

   **4.1.2 `DatabaseOperationPlan` (Struktur Kunci untuk Interaksi LLM -> ORM)**
    *   **Lokasi File Definisi**: `backend/app/schemas/agent_state.py` (sebagai bagian dari `AgentState` atau `TypedDict` terpisah yang diimpor).
    *   **Tujuan**: Ini adalah output JSON terstruktur yang dihasilkan oleh LLM di `plan_execution_node`. Node `execute_query_node` akan menerjemahkan setiap `DatabaseOperation` dalam rencana ini menjadi query SQLAlchemy ORM.
    *   **Struktur `DatabaseOperation` (`TypedDict`)**:
        ```python
        # Contoh dari backend/app/schemas/agent_state.py
        class SelectColumn(TypedDict, total=False):
            field_name: str  # Nama kolom (misal, "mastercustomer.Name" atau "arbook.DocValueLocal")
            aggregation: Optional[str]  # Opsional: "SUM", "COUNT", "AVG", "MAX", "MIN", "COUNT_DISTINCT"
            alias: Optional[str] # Opsional: Nama alias untuk kolom hasil

        class JoinCondition(TypedDict, total=False):
            left_table_field: str # misal, "arbook.CustomerCode"
            operator: str # misal, "=="
            right_table_field: str # misal, "mastercustomer.Code"

        class JoinClause(TypedDict, total=False):
            target_table: str # Nama tabel yang akan di-join (misal, "mastercustomer")
            join_type: str # "INNER", "LEFT", "RIGHT", "FULL"
            on_conditions: List[JoinCondition] # List kondisi untuk join multi-kolom atau kompleks

        class FilterCondition(TypedDict, total=False):
            field_or_expression: str # Nama kolom atau ekspresi (misal, "arbook.DueDate" atau "arbook.DocValueLocal - arbook.PaymentValueLocal")
            operator: str # misal, "==", ">", "<=", "IN", "NOT IN", "LIKE", "NOT LIKE", "IS_NULL", "IS_NOT_NULL"
            value: Any # Nilai untuk perbandingan. Bisa list untuk operator "IN" / "NOT IN".
            value_type: Optional[str] # "string", "number", "date", "boolean" (untuk membantu parsing/casting)

        class LogicalFilterGroup(TypedDict, total=False):
            logical_operator: str # "AND" atau "OR"
            conditions: List[Union[FilterCondition, 'LogicalFilterGroup']] # Bisa berisi FilterCondition atau grup filter bersarang

        class OrderByClause(TypedDict, total=False):
            field_name: str
            direction: str # "ASC" atau "DESC"

        class DatabaseOperation(TypedDict, total=False):
            operation_id: str # ID unik untuk operasi ini (misal, "get_total_outstanding")
            description: Optional[str] # Deskripsi tujuan operasi
            main_table: str # Nama tabel utama untuk query (misal, "arbook")
            select_columns: List[SelectColumn]
            joins: Optional[List[JoinClause]]
            filters: Optional[LogicalFilterGroup] # Klausa WHERE
            group_by_columns: Optional[List[str]] # List nama kolom untuk GROUP BY
            having_conditions: Optional[LogicalFilterGroup] # Klausa HAVING
            order_by_clauses: Optional[List[OrderByClause]]
            limit: Optional[int]
            offset: Optional[int]
            result_key: str # Kunci untuk menyimpan hasil di financial_calculations atau RAW_DATA_TABLE
            expected_result_format: str # "single_value", "list_of_dicts", "raw_table_data"
        ```
        *Catatan: `execute_query_node` akan memetakan nama tabel string (misalnya `main_table: "arbook"`) ke kelas model ORM yang sesuai (`Arbook`).*

### **4.2 Alur Kerja LangGraph (`backend/app/langgraph_workflow/graph.py`)**
*   Alur kerja yang didefinisikan (Entry Point, Node, Edge, Conditional Edge, END) tetap sama seperti yang dijelaskan di Bab 2.4. Perubahan utama terjadi di *dalam* `execute_query_node`.

### **4.3 Detail Operasional Node LangGraph (dengan Penekanan pada Integrasi ORM)**

   **4.3.1 Node: `understand_query_node`**
    *   **Tujuan dan Proses**: Tidak ada perubahan signifikan. Tetap menggunakan LLM untuk NLU.
    *   **Output**: `intent`, `entities_mentioned`, `time_period`, `requested_metrics`, `query_complexity`.

   **4.3.2 Node: `consult_schema_node`**
    *   **Tujuan dan Proses**: Tidak ada perubahan signifikan. Tetap mengambil metadata skema yang relevan dari Graphiti (Neo4j) menggunakan driver Python Neo4j inline.
    *   **Output**: `relevant_tables`, `table_relationships`, `financial_columns`, `temporal_columns`.

   **4.3.3 Node: `plan_execution_node`**
    *   **Tujuan dan Proses**: Perubahan signifikan pada *target output* LLM.
        *   Menggunakan LLM DeepSeek dengan template prompt spesifik-intent (dari `planning_prompts/`).
        *   Prompt menginstruksikan LLM untuk menghasilkan output JSON yang berisi:
            *   `database_operations_plan: List[DatabaseOperation]` (sesuai struktur di atas).
            *   `raw_data_operation_plan: DatabaseOperation` (untuk data detail).
            *   `response_template: str` (template narasi).
            *   `placeholder_mapping: Dict[str, Dict[str, Any]]` (aturan format placeholder).
            *   `data_source_info: Dict[str, Any]` (informasi sumber data).
    *   **Output**: `database_operations_plan`, `raw_data_operation_plan`, `response_template`, `placeholder_mapping`, `data_source_info`.
    *   **Penting**: Kualitas prompt di `planning_prompts/` sangat krusial untuk memastikan LLM menghasilkan `DatabaseOperationPlan` yang benar dan dapat diterjemahkan ke ORM.

   **4.3.4 Node: `execute_query_node` (Direfactor untuk ORM)**
    *   **Lokasi File**: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **Tujuan**: Menerima `database_operations_plan` dan `raw_data_operation_plan`, menerjemahkannya menjadi query SQLAlchemy ORM, mengeksekusinya, dan memformat hasilnya.
    *   **Input State Relevan**: `database_operations_plan`, `raw_data_operation_plan`.
    *   **Proses Utama**:
        1.  Set `current_node_name`.
        2.  Dapatkan sesi SQLAlchemy (`db: Session`) melalui `get_db_session()`.
        3.  Siapkan `models_map: Dict[str, Type[Base]]` yang memetakan nama tabel string (misalnya, "arbook") ke kelas model SQLAlchemy yang sesuai (misalnya, `Arbook`).
        4.  Untuk setiap `DatabaseOperation` dalam `database_operations_plan` dan `raw_data_operation_plan`:
            *   Panggil fungsi helper baru, misalnya `_build_and_execute_orm_query(operation: DatabaseOperation, db: Session, models_map: Dict[str, Type[Base]]) -> Any`:
                *   **Identifikasi Model Utama**: Dapatkan kelas model utama dari `operation.main_table` menggunakan `models_map`.
                *   **Bangun Query Awal**: `query = db.query()`.
                *   **Proses `select_columns`**:
                    *   Untuk setiap `SelectColumn`: dapatkan objek kolom ORM (misalnya, `models_map["mastercustomer"].Name`).
                    *   Jika ada `aggregation` (SUM, COUNT, dll.), bungkus kolom dengan fungsi SQLAlchemy yang sesuai (`func.sum(column_obj)`).
                    *   Jika ada `alias`, gunakan `.label(alias)`.
                    *   Tambahkan entitas yang akan di-select ke `query`.
                *   **Proses `joins`**:
                    *   Untuk setiap `JoinClause`: dapatkan model target dari `models_map`. Bangun kondisi join (`on_conditions`) secara dinamis. Terapkan `query.join()`. (Manfaatkan `relationship` jika `on_conditions` tidak diberikan).
                *   **Proses `filters` (WHERE)**: Rekursif memproses `LogicalFilterGroup` dan `FilterCondition` menjadi ekspresi filter SQLAlchemy. Terapkan `query.filter()`.
                *   **Proses `group_by_columns`**: Terapkan `query.group_by()`.
                *   **Proses `having_conditions`**: Terapkan `query.having()`.
                *   **Proses `order_by_clauses`**: Terapkan `query.order_by()`.
                *   **Proses `limit` dan `offset`**: Terapkan `query.limit()` dan `query.offset()`.
                *   **Eksekusi Query**: Jalankan `.all()`, `.first()`, atau `.scalar_one_or_none()` sesuai `expected_result_format`.
                *   **Konversi Hasil**: Konversi hasil ORM (list of RowProxy atau objek model) menjadi format `List[Dict[str, Any]]` yang bersih.
            *   Simpan hasil yang sudah dikonversi ke `financial_calculations` atau `raw_query_results` menggunakan `operation.result_key`.
        5.  Set `query_execution_status` dan `query_execution_errors`.
        6.  Tutup sesi SQLAlchemy.
    *   **Output**: `financial_calculations`, `raw_query_results`, `query_execution_status`, `query_execution_errors`.

   **4.3.5 Node: `validate_results_node`**
    *   **Tujuan dan Proses**: Tidak ada perubahan signifikan pada logikanya. Tetap memvalidasi data di `financial_calculations` dan `raw_query_results`.
    *   **Output**: `validation_status`, `validation_warnings`, `quality_score`.

   **4.3.6 Node: `replace_placeholders_node`**
    *   **Tujuan dan Proses**: Tidak ada perubahan signifikan. Tetap menggunakan `response_template`, `financial_calculations`, `placeholder_mapping` untuk menghasilkan `final_narrative`, `data_table_for_display`, dll. Logika formatting inline.
    *   **Output**: `final_narrative`, `data_table_for_display`, `executive_summary`, `warnings_for_display`, `workflow_status = "completed"`.

   **4.3.7 Node: `generate_error_response_node`**
    *   **Tujuan dan Proses**: Tidak ada perubahan.
    *   **Output**: Field error di `AgentState`, `workflow_status = "error"`.

Integrasi ORM akan sangat mengubah "jeroan" dari `execute_query_node`, membuatnya lebih bergantung pada kualitas `DatabaseOperationPlan` dan definisi model ORM, tetapi juga lebih aman dan potensial lebih mudah dipelihara.


---

## **Bab 5: Konfigurasi, Inisialisasi Sistem, dan Skrip Pendukung**

Bab ini merinci bagaimana konfigurasi sistem dikelola, bagaimana data dan skema awal diinisialisasi untuk lingkungan development dan testing (termasuk database tes untuk ORM), serta peran skrip-skrip pendukung.

### **5.1 File Konfigurasi `.env`**
*   **Lokasi**: `backend/.env`
*   **Tujuan**: Menyimpan semua konfigurasi sensitif dan spesifik lingkungan yang tidak boleh di-commit ke Git.
*   **Variabel Kunci yang Diharapkan (sesuai `backend/app/core/config.py`):**
    *   **LLM**:
        *   `DEEPSEEK_API_KEY`
        *   `DEEPSEEK_API_BASE_URL`
        *   `DEEPSEEK_MODEL`
    *   **Database MySQL Utama (`sim_testgeluran`)**:
        *   `MYSQL_HOST`
        *   `MYSQL_USER`
        *   `MYSQL_PASSWORD`
        *   `MYSQL_DATABASE` (harus `sim_testgeluran`)
        *   `MYSQL_PORT` (default 3306)
    *   **Database MySQL Tes (`sim_testgeluran_test`)**:
        *   `TEST_MYSQL_HOST` (bisa sama dengan `MYSQL_HOST`)
        *   `TEST_MYSQL_USER` (bisa user khusus tes atau sama)
        *   `TEST_MYSQL_PASSWORD` (password untuk user tes)
        *   `TEST_MYSQL_DATABASE` (harus `sim_testgeluran_test`)
        *   `TEST_MYSQL_PORT` (bisa sama dengan `MYSQL_PORT`)
    *   **Database Neo4j (untuk Graphiti)**:
        *   `NEO4J_URI` (misalnya, "bolt://localhost:7687")
        *   `NEO4J_USER`
        *   `NEO4J_PASSWORD`
        *   `NEO4J_DATABASE` (database di Neo4j yang digunakan)
        *   `SCHEMA_GROUP_ID` (misalnya, "sim_testgeluran_schema_v1", untuk mengelompokkan node skema di Graphiti)
    *   **Aplikasi**:
        *   `PROJECT_NAME`
        *   `PROJECT_VERSION`

### **5.2 File Pengaturan Aplikasi (`backend/app/core/config.py`)**
*   **Tujuan**: Memuat variabel dari `backend/.env` menggunakan `python-dotenv` dan menyediakannya sebagai atribut dari class `Settings`. Instance `settings` dari class ini digunakan di seluruh aplikasi backend.
*   **Fungsi Utama**:
    *   `load_dotenv()` untuk memuat `.env`.
    *   Definisi `class Settings` yang mengambil nilai dari variabel lingkungan (dengan nilai default jika ada).
    *   Pengecekan saat startup untuk memastikan variabel-variabel krusial (seperti API key LLM, kredensial DB utama dan tes, kredensial Neo4j) telah diset, dan memberikan peringatan jika tidak. Termasuk peringatan jika `TEST_DB_NAME` sama dengan `DB_NAME`.

### **5.3 Inisialisasi Database MySQL Utama (`sim_testgeluran`)**
*   **Tujuan**: Menyiapkan database operasional utama dengan skema dan data sampel awal untuk development.
*   **Sumber**:
    *   File `data_samples/schema.sql` (opsional, jika digunakan untuk setup skema awal).
    *   File `data_samples/data.sql` (opsional, jika digunakan untuk mengisi data sampel awal).
    *   Database `sim_testgeluran` yang sudah ada dengan data aktual.
*   **Proses Inisialisasi (Manual/Semi-Otomatis)**:
    1.  Pastikan MySQL server berjalan.
    2.  Jika menggunakan `schema.sql` dan `data.sql`:
        *   Buat database `sim_testgeluran` jika belum ada.
        *   Jalankan `schema.sql` untuk membuat struktur tabel.
        *   Jalankan `data.sql` untuk mengisi data sampel.
    3.  Jika menggunakan database yang sudah ada, pastikan skemanya sesuai dengan yang diharapkan oleh model ORM dan `graphiti_semantic_mapping.json`.
*   **Catatan**: AI Agent saat runtime hanya melakukan operasi baca (SELECT) terhadap database ini.

### **5.4 Inisialisasi Graphiti Knowledge Graph (Neo4j)**
*   **Tujuan**: Mempopulasi Neo4j dengan metadata skema `sim_testgeluran` yang diperkaya secara semantik, yang akan digunakan oleh `consult_schema_node`.
*   **Sumber Data Utama**:
    *   `data_samples/graphiti_semantic_mapping.json`: File JSON krusial yang mendefinisikan pemetaan semantik (purpose, classification, is_aggregatable, deskripsi kolom/tabel, dan definisi relasi logis) untuk setiap tabel dan kolom dari `sim_testgeluran`.
*   **Skrip Sinkronisasi**: `scripts/sync_mysql_to_graphiti.py`
    *   **Fungsi**:
        1.  Membaca `graphiti_semantic_mapping.json`.
        2.  Terhubung ke Neo4j menggunakan konfigurasi dari `settings`.
        3.  Membuat atau memperbarui (MERGE) node `:DatabaseTable` dan `:DatabaseColumn` di Neo4j. Setiap node diberi `uuid` deterministik dan `group_id`.
        4.  Membuat atau memperbarui relasi `:HAS_COLUMN` dan `:REFERENCES`.
    *   **Proses Inisialisasi**: Jalankan skrip ini setelah `graphiti_semantic_mapping.json` diperbarui atau untuk setup awal.

### **5.5 Inisialisasi Database Tes (`sim_testgeluran_test`) untuk ORM**
*   **Tujuan**: Menyediakan lingkungan database yang bersih dan terkontrol untuk pengujian model ORM dan logika query.
*   **Proses Inisialisasi**:
    1.  **Pembuatan Database (Sekali Manual)**: Buat database kosong `sim_testgeluran_test` di MySQL. Buat user tes jika perlu.
    2.  **Pembuatan/Pembaruan Skema Tabel (Otomatis via Skrip)**:
        *   Skrip `tests/orm/setup_test_schema.py` menggunakan `Base.metadata.drop_all(bind=engine_test)` dan `Base.metadata.create_all(bind=engine_test)` untuk menghapus skema lama dan membuat skema baru berdasarkan definisi model ORM di `backend/app/db_models/`.
        *   **Skrip ini harus dijalankan setiap kali ada perubahan pada definisi model ORM** untuk memastikan skema database tes selalu sinkron.
    3.  **Pengisian Data Dummy (Otomatis via Skrip Tes)**:
        *   Setiap file tes (misalnya, `tests/orm/test_orm_master_data.py`) bertanggung jawab untuk membuat data dummy spesifik yang relevan untuk tes di file tersebut menggunakan `TestDataFactory` atau secara manual, dalam sesi yang terisolasi.

### **5.6 Skrip Utilitas Pendukung Lainnya**
*   **`scripts/extract_mysql_schema.py`**:
    *   **Tujuan**: Menghasilkan `docs/sim_testgeluran_schema_report.txt`. Berguna untuk memverifikasi skema dan sebagai dasar membuat `graphiti_semantic_mapping.json` dan model ORM.
*   **`scripts/generate_orm_blueprint.py`**:
    *   **Tujuan**: Mengonversi semua model ORM yang telah terdefinisi menjadi file `tests/orm/orm_blueprint.json` yang akan dibaca oleh `TestDataFactory`.
*   **`tests/orm/run_all_orm_tests.py`**:
    *   **Tujuan**: Skrip pusat untuk menjalankan semua file tes ORM (`test_orm_*.py`) secara berurutan.

### **Alur Inisialisasi Keseluruhan untuk Lingkungan Development/Testing:**
1.  Siapkan dan jalankan server MySQL dan Neo4j.
2.  Buat database `sim_testgeluran` (isi dengan data) dan `sim_testgeluran_test` (kosong).
3.  Isi file `backend/.env` dengan semua kredensial dan konfigurasi yang benar.
4.  Pastikan `data_samples/graphiti_semantic_mapping.json` sudah lengkap.
5.  Jalankan `scripts/sync_mysql_to_graphiti.py` untuk mempopulasi/update Neo4j.
6.  Jalankan `scripts/generate_orm_blueprint.py` untuk membuat/memperbarui blueprint JSON.
7.  Jalankan `tests/orm/setup_test_schema.py` untuk membuat/memperbarui tabel-tabel di database tes.
8.  Setelah semua ini, aplikasi backend FastAPI dan skrip tes siap dijalankan.

---

## **Bab 6: Strategi Pengujian Komprehensif**

Bab ini menguraikan pendekatan pengujian yang akan digunakan untuk memastikan kualitas, fungsionalitas, dan keandalan MVP AI Agent, dengan penekanan pada pengujian model ORM dan integrasinya ke dalam alur kerja.

### **6.1 Filosofi Pengujian: Membangun Kepercayaan dari Pondasi**

Mengikuti analogi pembangunan rumah, strategi pengujian kita bertujuan untuk membangun kepercayaan pada setiap lapisan sistem, dimulai dari "pondasi" hingga "atap".
1.  **Pondasi (Definisi Model ORM & Koneksi DB)**: Ini adalah dasar interaksi kita dengan data. Kita harus memastikan model ORM didefinisikan dengan benar, semua relasi valid, dan koneksi ke database (baik development maupun tes) stabil. Kesalahan di sini akan meruntuhkan semua yang dibangun di atasnya.
2.  **Struktur Dasar (Unit Tes untuk Fungsi Kunci)**: Fungsi-fungsi individual, seperti penerjemah `DatabaseOperationPlan` ke query ORM di `execute_query_node`, atau parser output LLM, harus diuji secara terisolasi. Ini seperti memastikan setiap tiang dan balok kuat.
3.  **Integrasi Lantai (Integration Tests)**: Bagaimana model ORM bekerja dengan sesi database? Bagaimana node LangGraph berinteraksi? Bagaimana `AgentService` memanggil LangGraph? Ini adalah pengujian sambungan antar komponen.
4.  **Rumah Jadi (End-to-End Tests)**: Menguji seluruh alur dari input pengguna di API hingga respons akhir, melibatkan semua komponen utama yang terintegrasi. Ini memastikan rumah secara keseluruhan berfungsi.
5.  **Inspeksi Pemilik Rumah (User Acceptance Tests - UAT)**: Memastikan rumah yang jadi sesuai dengan kebutuhan dan harapan pengguna.

### **6.2 Level Pengujian**

*   **Unit Testing**:
    *   **Fokus**: Menguji unit kode terkecil (fungsi, metode, kelas ORM individual) secara terisolasi.
    *   **Contoh**:
        *   Tes definisi model ORM: memastikan kolom, tipe, PK, FK benar (dilakukan secara implisit oleh `setup_test_schema.py`).
        *   Tes `TestDataFactory`: memastikan ia bisa membuat objek model yang valid.
        *   Tes logika internal node LangGraph (dengan mock dependensi eksternal seperti LLM call atau sesi DB).
*   **Integration Testing**:
    *   **Fokus**: Menguji interaksi antar komponen/modul.
    *   **Contoh**:
        *   **ORM & DB**: Menguji apakah model ORM dapat melakukan query (SELECT, JOIN sederhana) ke database tes yang berisi data dummy dan mengembalikan hasil yang diharapkan. (Ini yang sedang kita fokuskan di `tests/orm/`).
        *   Node LangGraph & Sesi DB: Menguji `execute_query_node` dengan sesi DB asli (ke DB tes) dan `DatabaseOperationPlan` sederhana.
        *   API Endpoint & `AgentService`.
*   **End-to-End (E2E) System Testing**:
    *   **Fokus**: Menguji sistem secara keseluruhan dari input hingga output, mencakup semua komponen utama yang terintegrasi.
    *   **Contoh**: Mengirim `QueryRequest` ke API `POST /api/v1/query` dan memverifikasi `QueryResponseSuccess` atau `QueryResponseError` yang dihasilkan.
*   **User Acceptance Testing (UAT)**:
    *   **Fokus**: Dilakukan oleh perwakilan pengguna atau product owner untuk memastikan sistem memenuhi kebutuhan bisnis dan mudah digunakan.

### **6.3 Lingkungan Pengujian**

1.  **Database MySQL Utama (`sim_testgeluran`)**:
    *   **Penggunaan**: Digunakan oleh aplikasi saat berjalan normal (development/produksi). **TIDAK** untuk tes otomatis yang destruktif.
    *   **Data**: Data riil atau data sampel development yang representatif.
2.  **Database MySQL Tes (`sim_testgeluran_test`)**:
    *   **Penggunaan**: **KHUSUS** untuk semua tes otomatis yang melibatkan interaksi database (`tests/orm/`).
    *   **Skema**: Dibuat dan diperbarui secara otomatis oleh `tests/orm/setup_test_schema.py` berdasarkan model ORM di `backend/app/db_models/`. Ini memastikan skema tes selalu sinkron dengan definisi model.
    *   **Data**: Dihapus dan dibuat ulang oleh setiap fungsi tes untuk memastikan **isolasi tes** yang sempurna. Setiap tes dimulai dengan database yang bersih.
3.  **Graphiti (Neo4j)**:
    *   Menggunakan instance development yang dipopulasi oleh `scripts/sync_mysql_to_graphiti.py`. Tes yang melibatkan `consult_schema_node` akan berinteraksi dengan instance ini.
4.  **LLM (DeepSeek)**:
    *   Untuk unit test node yang menggunakan LLM (`understand_query_node`, `plan_execution_node`), panggilan LLM akan di-*mock* untuk memastikan prediktabilitas dan menghindari biaya/dependensi eksternal.
    *   Untuk E2E testing, panggilan LLM akan dilakukan secara live.

### **6.4 Tools Pengujian**

*   **Skrip Python Kustom**: Untuk pengujian model ORM dan logika spesifik (seperti `tests/orm/run_all_orm_tests.py` dan file `test_orm_*.py` di dalamnya). Memberikan kontrol penuh atas output log.
*   **SQLAlchemy**: Digunakan dalam skrip tes untuk membuat sesi ke database tes dan melakukan query ORM.
*   **`unittest.mock` (Python built-in)**: Untuk *mocking* dependensi eksternal (LLM API, panggilan layanan lain) selama unit testing.
*   **Postman/Insomnia**: Untuk pengujian API backend secara manual selama development dan E2E testing.
*   **LangSmith (jika digunakan)**: Untuk memantau dan men-debug alur kerja LangGraph selama E2E testing.

### **6.5 Strategi Pengujian Spesifik untuk ORM (Dengan "Pabrik Data")**

Ini adalah "pondasi" kita yang sekarang sudah menggunakan strategi baru yang lebih robust.
*   **Verifikasi Definisi Model dan Relasi**:
    *   **Tujuan**: Memastikan semua kelas model ORM dan `relationship` didefinisikan dengan benar dan SQLAlchemy dapat membuat skema database darinya tanpa error.
    *   **Metode**: Skrip `tests/orm/setup_test_schema.py` yang menjalankan `Base.metadata.create_all(bind=engine_test)` adalah tes utamanya. Jika skrip ini berhasil, berarti semua definisi model dan relasi kita valid secara sintaksis.
*   **Verifikasi Pembuatan Data (Integration Test ORM & DB)**:
    *   **Tujuan**: Memastikan bahwa "Pabrik Data" (`TestDataFactory`) dapat membuat instance dari setiap model ORM yang kompleks dan menyimpannya ke database tes tanpa melanggar aturan `ForeignKey` atau `NOT NULL`.
    *   **Metode**: Setiap fungsi tes di dalam `test_orm_*.py` (seperti `test_master_customer_creation`):
        1.  Memulai sesi database yang bersih.
        2.  Membuat instance `TestDataFactory`.
        3.  Memanggil `factory.create("NamaModel", ...)` untuk membuat data yang dibutuhkan. Pabrik akan secara otomatis menangani pembuatan data prasyarat.
        4.  Menyimpan ke database dengan `db.session.commit()`.
        5.  Mengambil kembali data yang baru disimpan dan melakukan `assert` untuk memverifikasi datanya benar.
        6.  Sesi ditutup, dan tes berikutnya dimulai dengan sesi baru yang bersih.

### **6.6 Kriteria Keberhasilan Pengujian MVP Awal (Fokus ORM & Backend)**
*   Skrip `setup_test_schema.py` berhasil berjalan tanpa error.
*   Semua fungsi tes di dalam direktori `tests/orm/` berhasil dijalankan oleh `run_all_orm_tests.py` dengan hasil `✅ SEMUA TES ORM BERHASIL.`.
*   (Menuju STEP 3) `execute_query_node` berhasil direfactor untuk menggunakan ORM dan dapat mengeksekusi `DatabaseOperationPlan` sederhana hingga menengah untuk query penjualan dan piutang.
*   E2E test dasar melalui API (Postman) untuk query utama MVP menghasilkan data yang akurat dan narasi yang benar.

---

Tentu. Berikut adalah Bab 7. Saya telah memastikan bab ini merangkum secara detail semua tantangan teknis yang telah kita hadapi dan atasi bersama, serta praktik terbaik yang kita terapkan sebagai hasilnya. Ini akan menjadi "peta jebakan" yang sangat berharga untuk pengembangan di masa depan.

---

## **Bab 7: Pembelajaran Teknis, Penanganan Error, dan Praktik Terbaik**

Bab ini bertujuan untuk merangkum pembelajaran teknis penting, strategi penanganan error yang telah diadopsi atau perlu dipertimbangkan, dan praktik terbaik yang muncul selama proses pengembangan MVP AI Agent. Ini berfungsi sebagai "knowledge base" internal untuk proyek.

### **7.1 Pembelajaran Teknis dari Pengembangan dan Debugging**

   **7.1.1 Masalah Impor Python (`ModuleNotFoundError`, `ImportError`)**
    *   **Deskripsi**: Error terjadi ketika Python tidak dapat menemukan modul atau nama spesifik yang diimpor. Sering disebabkan oleh path yang salah, struktur package yang tidak benar (lupa `__init__.py`), typo, atau *circular import*.
    *   **Penyebab Utama Error Berulang**: Khususnya *circular import* saat mendefinisikan model ORM SQLAlchemy yang saling merujuk di file terpisah (misalnya, `sales_models.py` mengimpor `master_data_models` dan sebaliknya).
    *   **Solusi yang Berhasil Diterapkan**:
        1.  **Gunakan String untuk Target `relationship`**: Ini adalah praktik terbaik dan solusi paling ampuh. Dengan mendefinisikan relasi sebagai `relationship("NamaModelLain", ...)` daripada `relationship(NamaModelLain, ...)` SQLAlchemy menunda resolusi relasi hingga semua model telah dimuat, sehingga memutus lingkaran impor.
        2.  **Pusatkan Konfigurasi di `__init__.py`**: Membuat file `backend/app/db_models/__init__.py` yang mengimpor semua modul model (`master_data_models`, `sales_models`, dll.) lalu memanggil `configure_mappers()` secara eksplisit. Ini memastikan semua model dan relasi "terdaftar" dan "tersambung" di satu tempat sebelum digunakan oleh bagian lain dari aplikasi.
        3.  **Impor Package, Bukan Modul Individual**: Skrip eksternal (seperti skrip tes atau `generate_orm_blueprint.py`) harus mengimpor seluruh paket (`from backend.app import db_models`) untuk memicu eksekusi `__init__.py` dan proses konfigurasi mapper.

   **7.1.2 Error Konfigurasi Mapper SQLAlchemy (`ArgumentError`, `InvalidRequestError`, `NoForeignKeysError`)**
    *   **Deskripsi**: Serangkaian error yang muncul saat SQLAlchemy mencoba membangun "mapper" dan menemukan ketidaksesuaian atau ambiguitas dalam definisi model dan relasi.
    *   **Penyebab Utama Error Berulang**:
        1.  **Nama `back_populates` Tidak Cocok**: Relasi di Model A menunjuk ke `back_populates="relasi_x"`, tetapi di Model B relasi baliknya bernama `relasi_y`.
        2.  **`ForeignKey` Hilang**: Mencoba membuat `relationship` antara dua model tanpa mendefinisikan `ForeignKey` pada kolom yang sesuai di salah satu model.
        3.  **Ambiguitas `ForeignKey`**: Satu model memiliki beberapa `ForeignKey` ke tabel yang sama, atau `ForeignKey` komposit tidak didefinisikan dengan benar, membuat SQLAlchemy bingung bagaimana cara melakukan join.
    *   **Solusi yang Berhasil Diterapkan**:
        1.  **Konsistensi `back_populates`**: Selalu pastikan nama yang digunakan di `back_populates` di satu sisi relasi adalah nama atribut `relationship` yang benar di sisi lainnya.
        2.  **`ForeignKey` Eksplisit**: Selalu definisikan `ForeignKey('nama_tabel.nama_kolom')` pada kolom yang benar di model sisi "many".
        3.  **`ForeignKeyConstraint` untuk Kunci Komposit**: Untuk `ForeignKey` yang melibatkan lebih dari satu kolom, definisikan `ForeignKeyConstraint` di dalam `__table_args__` pada model "child".
        4.  **`foreign_keys` Eksplisit pada `relationship`**: Saat mendefinisikan `relationship` yang melibatkan `ForeignKey` komposit atau ambigu, secara eksplisit tentukan kolom mana yang harus digunakan dengan argumen `foreign_keys=[Model.kolom1, Model.kolom2]`.

   **7.1.3 Error Integritas Database (`IntegrityError`, `DataError`) saat Testing**
    *   **Deskripsi**: Terjadi saat `db.commit()` dijalankan, dan data yang kita coba masukkan melanggar aturan database (`NOT NULL`, `UNIQUE`, `FOREIGN KEY`, panjang data).
    *   **Penyebab Utama Error Berulang**:
        1.  **`Data too long`**: Nilai dummy yang di-generate oleh pabrik data lebih panjang dari batasan `VARCHAR(x)` di kolom database.
        2.  **`Column cannot be null`**: Pabrik data lupa memberikan nilai untuk kolom yang `NOT NULL`, terutama kolom `primary_key` atau kolom audit (`CreatedBy`).
        3.  **`FOREIGN KEY constraint fails`**: Pabrik data mencoba membuat data "child" sebelum data "parent" yang direferensikan benar-benar tersimpan di database dalam sesi transaksi yang sama. Ini sering terjadi pada relasi ke diri sendiri (`self-referencing`).
    *   **Solusi yang Berhasil Diterapkan**:
        1.  **Perbaiki `TestDataFactory`**: Mengajarkan `generate_value` untuk membaca batasan panjang dari blueprint dan selalu mengisi kolom audit.
        2.  **`setup_test_schema.py`**: Membuat skrip ini untuk memastikan skema database tes **selalu sinkron** dengan definisi model ORM, terutama setelah mengubah `nullable=True` pada suatu kolom. Menjalankan `Base.metadata.drop_all()` sebelum `create_all()` adalah kunci untuk sinkronisasi.
        3.  **Commit Bertahap untuk Data Prasyarat**: Dalam skrip tes, kita menggunakan pendekatan manual di mana data induk (misalnya `MasterCountry`) dibuat dan di-`commit` terlebih dahulu sebelum membuat data anak (misalnya `MasterCustomer`) yang bergantung padanya. Ini adalah cara paling andal untuk menangani `ForeignKey`.

### **7.2 Praktik Terbaik yang Diterapkan atau Dianjurkan**

*   **Struktur Kode Modular**: Memisahkan model ORM ke dalam file-file per modul bisnis (`master_data_models.py`, `sales_models.py`, dll.) adalah praktik yang baik untuk keterbacaan dan pemeliharaan.
*   **Pengujian Berbasis Database Tes**: Menggunakan database tes terpisah (`sim_testgeluran_test`) dengan skema yang dibuat dari model ORM dan data dummy yang terkontrol adalah fundamental untuk pengujian ORM yang andal dan tidak merusak data utama.
*   **Isolasi Tes**: Merancang setiap fungsi tes agar independen (membuat sesi DB dan pabrik datanya sendiri) mencegah masalah dari "sisa data" tes sebelumnya dan membuat debugging lebih mudah.
*   **Pengurutan Atribut Model ORM**: Mengurutkan kolom dan `relationship` secara alfabetis dalam definisi kelas model meningkatkan keterbacaan dan kemudahan maintenance.
*   **Peringatan (`SAWarning`)**: Meskipun tidak menghentikan program, peringatan dari SQLAlchemy (seperti `SAWarning` tentang relasi yang tumpang tindih) harus dicatat. Solusinya seringkali melibatkan penggunaan `viewonly=True` pada salah satu relasi untuk memberitahu SQLAlchemy bahwa relasi tersebut hanya untuk membaca, bukan untuk menulis.

Dengan mendokumentasikan pembelajaran ini, kita berharap dapat membangun AI Agent yang lebih robust dan mempercepat proses debugging di masa depan.

---
Tentu. Berikut adalah Bab 8 dan Bab 9. Saya telah memeriksa ulang untuk memastikan isinya akurat, mencerminkan progres terakhir kita, menetapkan langkah selanjutnya yang jelas, dan memberikan panduan yang tepat untuk penggunaan dokumen ini.

---

## **Bab 8: Progres Pengembangan dan Rencana Selanjutnya (To-Do List Dinamis)**

Bab ini merangkum status progres pengembangan MVP AI Agent hingga saat ini, berdasarkan To-Do List komprehensif yang telah kita susun (Revisi 5), dan menguraikan langkah-langkah selanjutnya yang akan diambil.

### **8.1 Ringkasan Progres Terkini (Berdasarkan To-Do List Revisi 5)**

*   **STEP 0: Persiapan Struktur Proyek dan Lingkungan (Dasar ORM)**
    *   **Status**: ✅ **SELESAI**
    *   **Detail**: Direktori model ORM, file `base.py`, `config.py`, dan `session.py` telah disiapkan dan dikonfigurasi dengan benar untuk database utama dan tes.

*   **STEP 1: Definisi dan Pengujian Model Database SQLAlchemy**
    *   **Status**: ⏳ **SEDANG DIKERJAKAN**
    *   **Detail Progres**:
        *   **Definisi Model**: Kerangka dasar untuk semua modul model yang relevan (`master_data`, `sales`, `inventory`, `purchase`) telah dibuat. Relasi-relasi kunci antar model ini sudah mulai didefinisikan.
        *   **Penyelesaian Masalah Kritis**: Kita telah berhasil mengatasi serangkaian masalah konfigurasi ORM yang kompleks, termasuk `Circular Imports`, `NoForeignKeysError`, `IntegrityError` (untuk kolom `NOT NULL` dan `self-referencing FK`), dan `DataError`. Ini membuktikan arsitektur ORM dan strategi testing kita sudah valid.
        *   **Pabrik Data (`TestDataFactory`)**: Sistem untuk membuat data tes secara otomatis telah dibuat dan disederhanakan.
        *   **Pengujian Awal**: Skrip `test_orm_master_data.py` berhasil dieksekusi, membuktikan bahwa kita bisa membuat objek kompleks seperti `MasterCustomer` dan `MasterMaterial` beserta semua dependensi data masternya.

*   **STEP 2: Konfigurasi dan Inisialisasi Engine serta Session SQLAlchemy**
    *   **Status**: ✅ **SELESAI**
    *   **Detail**: File `backend/app/db/session.py` telah dikonfigurasi untuk menangani sesi database utama dan tes. Skrip `tests/orm/setup_test_schema.py` berhasil membuat skema database tes dari model ORM.

*   **STEP 3 - STEP 9**:
    *   **Status**: ⚪ **BELUM DIMULAI** (Menunggu penyelesaian dan stabilisasi seluruh model ORM yang relevan untuk MVP di STEP 1).

### **8.2 Status Detail per STEP/Sub-STEP (Fokus pada yang Aktif)**

*   **STEP 1.1 (Model Master Data)**: Sebagian besar model kunci di `master_data_models.py` sudah stabil.
*   **STEP 1.2 (Model Sales)**: Kerangka model di `sales_models.py` sudah ada dan relasi dasarnya terhubung. Perlu dilengkapi lebih detail.
*   **STEP 1.3 (Model Inventory)**: Kerangka model di `inventory_models.py` sudah ada. Perlu dilengkapi dan diuji.
*   **STEP 1.4 (Model Purchase)**: Kerangka model di `purchase_models.py` sudah ada. Perlu dilengkapi dan diuji.

### **8.3 Masalah Utama yang Sedang Dihadapi Saat Ini:**
*   Tidak ada error yang *blocker*. Fokus utama adalah melanjutkan implementasi model ORM yang tersisa secara metodis.
*   Peringatan `SAWarning` tentang relasi yang tumpang tindih masih muncul. Ini tidak menghentikan program, tetapi perlu ditangani nanti untuk "membersihkan" output.

### **8.4 Rencana Jangka Pendek dan Menengah Berikutnya**

1.  **(Jangka Pendek - Prioritas Utama) Melengkapi dan Menguji Model Per Modul**:
    *   **Tugas**: Kita akan melanjutkan proses yang sudah terbukti berhasil. Kita akan melengkapi semua kolom dan relasi untuk model-model di `purchase_models.py`, lalu membuat file tes `tests/orm/test_orm_purchase.py` untuk memvalidasinya.
    *   Setelah itu, kita akan melakukan hal yang sama untuk modul-modul lain yang relevan untuk MVP (`production`, `finance`, dll.) satu per satu.
    *   **File yang akan dikerjakan selanjutnya**: `backend/app/db_models/purchase_models.py` dan `tests/orm/test_orm_purchase.py`.

2.  **(Jangka Menengah) Mengatasi `SAWarning`**:
    *   Setelah semua model utama selesai dan teruji, kita akan melakukan sesi khusus untuk mengatasi peringatan `SAWarning` dengan menambahkan parameter `viewonly=True` atau `overlaps` pada relasi yang tumpang tindih, sesuai petunjuk dari peringatan tersebut.

3.  **(Jangka Menengah) Memulai STEP 3 - Refactoring `execute_query_node`**:
    *   Setelah fondasi ORM untuk semua tabel yang relevan dengan MVP sudah matang dan teruji, barulah kita akan mulai mengintegrasikannya ke dalam alur kerja LangGraph.

Tujuan kita adalah memiliki definisi ORM yang solid dan teruji untuk semua tabel yang akan disentuh oleh query MVP sebelum kita mulai mengintegrasikannya ke dalam logika agent.

---

## **Bab 9: Panduan Penggunaan Dokumen Ini oleh Asisten LLM**

Bab ini adalah panduan khusus untuk Anda, Asisten LLM, mengenai cara terbaik memanfaatkan Dokumen Konteks Proyek Komprehensif ini untuk membantu pengembangan proyek AI Agent secara efektif dan efisien. Keberhasilan Anda dalam membantu akan sangat bergantung pada pemahaman Anda terhadap dokumen ini, yang berfungsi sebagai "memori jangka panjang" dan "sumber kebenaran tunggal" untuk proyek ini.

### **9.1 Misi Utama Anda sebagai Asisten Pengembangan AI**

Misi utama Anda adalah bertindak sebagai **asisten pengembangan AI yang proaktif, teliti, akurat, dan kolaboratif**. Anda diharapkan untuk:

1.  **Memahami Konteks Proyek Secara Mendalam**: Menggunakan informasi dalam dokumen ini untuk memiliki pemahaman yang komprehensif tentang tujuan proyek MVP, arsitektur sistem, stack teknologi yang digunakan, struktur kode yang ada (terutama definisi model ORM, struktur `AgentState`, dan alur LangGraph), progres pengembangan terkini, rencana selanjutnya, serta pembelajaran teknis yang telah didapat.
2.  **Membantu Implementasi Kode Python**: Memberikan bantuan dalam menulis, merevisi, men-debug, dan mengoptimalkan kode Python, khususnya yang berkaitan dengan:
    *   SQLAlchemy ORM (definisi model, relasi, query).
    *   FastAPI (endpoint, model Pydantic).
    *   LangGraph (definisi graph, node, state management).
    *   Interaksi dengan database (MySQL melalui ORM, Neo4j melalui driver Python).
    *   Logika pemrosesan data dan algoritma dalam node agent.
    *   Membantu merancang dan menyempurnakan prompt untuk LLM (DeepSeek).
3.  **Mengikuti Prinsip Desain dan Rencana Proyek**: Selalu ingat dan terapkan prinsip-prinsip desain utama proyek (seperti yang dijelaskan di Bab 1.3) serta rencana implementasi ORM dan To-Do List dinamis (Bab 8) dalam setiap saran atau kode yang Anda berikan.
4.  **Menghindari Kesalahan Berulang dan Menerapkan Praktik Terbaik**: Memanfaatkan Bab 7 (Pembelajaran Teknis, Penanganan Error, dan Praktik Terbaik) untuk menghindari pengulangan kesalahan yang pernah terjadi dan untuk mempromosikan kualitas kode yang lebih baik.
5.  **Berkomunikasi Secara Efektif dan Kolaboratif**: Mengikuti gaya interaksi dan format revisi kode yang dijelaskan dalam Bab 1.1. Proaktif dalam meminta klarifikasi jika ada ambiguitas.

### **9.2 Cara Efektif Menggunakan dan Menavigasi Dokumen Ini**

*   **Acuan Pertama dan Utama**: Sebelum memberikan jawaban, saran, atau memulai tugas baru, selalu pertimbangkan apakah informasi yang relevan sudah ada dan dijelaskan dalam dokumen ini.
*   **Navigasi antar Bab**: Gunakan struktur bab untuk menemukan informasi spesifik dengan cepat:
    *   **Bab 1 & 2**: Untuk gambaran umum, tujuan proyek, prinsip desain, arsitektur sistem, dan peran ORM.
    *   **Bab 3**: Untuk detail struktur file dan direktori, serta deskripsi fungsi utama file-file Python kunci. Penting untuk mengetahui di mana kode tertentu berada.
    *   **Bab 4**: Untuk detail logika inti LangGraph Workflow, definisi `AgentState` dan `DatabaseOperationPlan`, serta bagaimana `execute_query_node` akan menggunakan ORM.
    *   **Bab 5**: Untuk memahami konfigurasi sistem (`.env`, `config.py`) dan proses inisialisasi data/skema.
    *   **Bab 6**: Untuk strategi pengujian yang diadopsi, termasuk peran database tes dan `TestDataFactory`.
    *   **Bab 7**: Sangat penting untuk dibaca ulang secara berkala. Berisi rangkuman error yang pernah terjadi dan solusinya, serta praktik terbaik untuk diikuti.
    *   **Bab 8**: Ini adalah bab yang paling dinamis, berisi progres terkini dan To-Do List yang detail. Selalu periksa bab ini untuk mengetahui apa yang sedang dikerjakan dan apa langkah berikutnya.
*   **Keterkaitan dengan Dokumen Perencanaan Lain**: Jika developer secara spesifik merujuk ke dokumen lain di direktori `docs/` (misalnya, `sim_testgeluran_schema_report.txt` atau `metadata.txt` untuk detail skema saat membuat model ORM), Anda harus bisa memprosesnya jika developer mengunggah konten file tersebut.

### **9.3 Cara Meminta Informasi Tambahan (File Kode Spesifik)**

*   **Prinsip**: **Minta hanya file yang benar-benar Anda butuhkan untuk tugas saat ini.** Hindari meminta developer mengunggah seluruh direktori atau codebase. Jadilah spesifik.
*   **Contoh Permintaan yang Baik**:
    *   "Untuk melanjutkan pembuatan model `PurchaseOrderH` di `purchase_models.py`, saya perlu melihat kembali bagian terkait `purchaseorderh` dari `docs/sim_testgeluran_schema_report.txt` dan `data_samples/metadata.txt` untuk memastikan semua kolom, tipe data, dan relasi FK terdefinisi dengan benar."
*   **Jelaskan Mengapa Anda Membutuhkan File Tersebut**: Ini membantu developer memahami konteks permintaan Anda.

### **9.4 Mengingat Konteks dan Progres Antar Sesi (Peran Dokumen Ini)**

*   Dokumen Konteks Proyek Komprehensif ini adalah "memori eksternal" utama Anda untuk proyek ini. Setiap kali sesi baru dimulai, developer akan mencoba memberikan versi terbaru dari dokumen ini.
*   **Bab 8 (Progres Pengembangan dan Rencana Selanjutnya)** adalah acuan utama untuk mengetahui apa yang *sedang* dikerjakan dan apa langkah *berikutnya*.

### **9.5 Berpikir Kritis, Memberikan Saran, dan Meminta Bantuan**

Meskipun peran utama Anda adalah membantu implementasi berdasarkan rencana yang ada, kemampuan Anda untuk berpikir kritis sangat dihargai:

*   **Identifikasi Potensi Masalah atau Inkonsistensi**: Jika Anda menemukan sesuatu dalam rencana, kode yang ada, atau permintaan developer yang tampaknya bertentangan dengan prinsip desain, sampaikanlah dengan sopan.
*   **Sarankan Perbaikan atau Praktik Terbaik**: Jika relevan, Anda boleh menyarankan perbaikan terkait keamanan, efisiensi, atau kejelasan kode, selama masih dalam lingkup MVP.
*   **Minta Klarifikasi atau Bantuan Lebih Lanjut**: Jika instruksi developer kurang jelas atau Anda menghadapi masalah yang sangat kompleks, jangan ragu untuk membantu developer menyusun pertanyaan yang terstruktur untuk diajukan kepada "AI Agent Researcher" (pakar manusia).

---
Tentu. Saya akan membuat Bab 10. Saya telah memeriksa kembali rencana kita dan konten dari file `9_TodoList.md` yang relevan untuk memastikan lampiran ini akurat dan berguna.

---

## **Bab 10: Lampiran**

Bab ini berisi dokumen-dokumen pendukung atau salinan dari file-file kunci yang berfungsi sebagai referensi cepat untuk pengembangan.

### **Lampiran A: To-Do List Pengembangan (Revisi 5)**

Berikut adalah salinan dari file `9_TodoList.md` yang berfungsi sebagai panduan pengembangan utama kita. Ini merinci semua langkah yang diperlukan untuk menyelesaikan MVP, dengan fokus pada implementasi SQLAlchemy ORM.

---

**To-Do List (Revisi 5 - Paling Lengkap): Implementasi ORM (SQLAlchemy) untuk AI Agent**

**Versi Dokumen**: 4.0
**Tanggal**: (Tanggal saat ini)

**Pendahuluan**:
Dokumen ini adalah panduan pengembangan terperinci untuk MVP AI Agent, dengan penekanan kuat pada implementasi Object-Relational Mapper (ORM) menggunakan SQLAlchemy. Strategi utamanya adalah mendefinisikan dan menguji model ORM secara menyeluruh untuk tabel-tabel yang relevan dengan MVP sebelum merefactor logika eksekusi query. Pengujian dilakukan secara bertahap untuk setiap set model dan relasi yang didefinisikan.

---

**STEP 0: Persiapan Struktur Proyek dan Lingkungan (Dasar ORM)**
*   **Status**: ✅ **SELESAI**
    *   **0.1**: Verifikasi direktori `backend/app/db_models/` sudah ada.
    *   **0.2**: Verifikasi file `backend/app/db_models/base.py` sudah dibuat dan berisi `Base = declarative_base()`.
    *   **0.3**: Verifikasi file-file Python kosong untuk kategori model (`master_data_models.py`, `sales_models.py`, `inventory_models.py`, `purchase_models.py`, `production_models.py`, `finance_models.py`, `hr_models.py`, `logistics_models.py`, `system_models.py`) sudah dibuat di `backend/app/db_models/`.
    *   **0.4**: Verifikasi file `backend/app/db_models/__init__.py` sudah dibuat (berisi impor awal untuk `Base` dan model-model yang sudah didefinisikan).
    *   **0.5**: **TESTING (STEP 0)**: Verifikasi impor dasar dari struktur package `db_models` berhasil (telah dilakukan dengan `python test_orm_definitions.py`).

---

**STEP 1: Definisi dan Pengujian Model Database SQLAlchemy (Komprehensif untuk Cakupan MVP)**
*Tujuan: Mendefinisikan semua model ORM yang relevan untuk skenario query MVP (penjualan, piutang, dan tabel pendukungnya) dengan relasi yang akurat, dan mengujinya secara iteratif.*
*Panduan Umum untuk Setiap Sub-Langkah di STEP 1:*
    *   Untuk setiap model baru: definisikan kolom (urut abjad), `ForeignKey` (sesuai `sim_testgeluran_schema_report.txt`), `ForeignKeyConstraint` (untuk FK komposit), `relationship` (dengan `back_populates` yang konsisten, dan `primaryjoin` atau `foreign_keys` eksplisit untuk relasi kompleks/komposit). Gunakan `metadata.txt` untuk komentar dan konfirmasi relasi logis. Atribut (kolom dan relasi) diurutkan secara alfabetis.
    *   Setelah setiap set model signifikan didefinisikan atau direvisi, update `backend/app/db_models/__init__.py` dengan mengimpor kelas model baru dan menambahkannya ke list `__all__`.
    *   Segera lakukan **TESTING** menggunakan `python test_orm_definitions.py` (untuk cek impor & konfigurasi mapper awal). Jika `test_orm_definitions.py` menjadi terlalu besar, buat file tes ORM per kategori (misalnya, `tests/db/test_orm_master_data.py`) yang melakukan query sederhana dan menguji relasi baru terhadap database `sim_testgeluran` sampel.

*   **1.1**: **Selesaikan dan Uji Model untuk Master Data (`master_data_models.py`)**:
    *   **Status**: ⏳ **SEDANG DIKERJAKAN**
    *   **1.1.1**: **Finalisasi Model Master Dasar dan Relasinya yang Sudah Dimulai**:
        *   Review dan finalisasi `MasterCountry`, `MasterCity`, `MasterUnit`, `MasterCurrency`.
        *   Selesaikan dan uji `MasterAccountGroup` beserta relasi `accounts` ke `MasterAccount`.
        *   Selesaikan dan uji `MasterDepartment`.
        *   Selesaikan dan uji `MasterAccount` beserta relasi `account_group_ref` ke `MasterAccountGroup`, `department_ref` ke `MasterDepartment`, `currency_ref` ke `MasterCurrency`, dan relasi self-referential `ParentNo` (gunakan `remote_side` dan dua `relationship` terpisah jika diimplementasikan).
        *   Selesaikan dan uji `MasterTransactionType` beserta relasi `master_account_ref` ke `MasterAccount`.
        *   **Selesaikan dan uji relasi komposit antara `MasterMaterialGroup1` (`material_group2_children`), `MasterMaterialGroup2` (`group1_as_parent`, `material_group3_children`), dan `MasterMaterialGroup3` (`group2_parent_ref`) secara tuntas menggunakan `ForeignKeyConstraint` dan `primaryjoin`/`foreign_keys` yang tepat.** (Ini adalah fokus kita saat ini dan beberapa iterasi terakhir).
        *   Selesaikan dan uji `MasterMaterialType`.
        *   Selesaikan dan uji `MasterEmployeeH`.
        *   Selesaikan dan uji `MasterSales` beserta relasi `employee_data_ref` ke `MasterEmployeeH`.
        *   Selesaikan dan uji `MasterLocation` beserta relasi `country_location_ref` ke `MasterCountry`.
        *   **Selesaikan dan uji relasi komposit antara `MasterSalesArea1` (`sales_area2_children`), `MasterSalesArea2` (`area1_parent_ref`, `sales_area3_children`), dan `MasterSalesArea3` (`area2_ref`) secara tuntas menggunakan `ForeignKeyConstraint` dan `primaryjoin`/`foreign_keys` yang tepat.** (Ini adalah error terakhir yang kita hadapi).
        *   Selesaikan dan uji `MasterCustomer` beserta semua relasi ke `MasterCountry`, `MasterCurrency`, `MasterCustomerGroup`, `MasterPriceListType`, `MasterSalesArea1`, `MasterTransactionType`.
        *   Selesaikan dan uji `MasterMaterial` beserta semua relasi ke `MasterUnit`, `MasterMaterialGroup1`, `MasterMaterialType`, `MasterCurrency`, `MasterTransactionType`, dan self-referential `Substitute`.
        *   Selesaikan dan uji `MasterCustomerPartner` beserta relasi kompositnya ke `MasterCustomer`.
        *   Selesaikan dan uji `MasterUnitConversion` beserta relasinya ke `MasterMaterial` dan `MasterUnit`.
        *   Selesaikan dan uji `MasterSupplier` beserta relasinya ke `MasterCountry`, `MasterCurrency`, `MasterCity`, `MasterTransactionType`.
        *   File terkait: `backend/app/db_models/master_data_models.py` (direview, disempurnakan, diuji)
    *   **1.1.2**: **Implementasi dan Uji Model Master Data Tambahan** (berdasarkan `metadata.txt` dan relevansi MVP):
        *   Contoh: `MasterBank`, `MasterCollector`, `MasterVehicle`, `MasterVehicleType`, `MasterRoute`, `MasterPaymentType` (jika ada), `MasterSeriesDocument` (jika diperlukan untuk relasi).
        *   Definisikan kolom dan relasi, urutkan atribut.
        *   File terkait: `backend/app/db_models/master_data_models.py` (ditambahkan)
    *   **1.1.3**: Update `backend/app/db_models/__init__.py` untuk semua model master.
        *   File terkait: `backend/app/db_models/__init__.py` (diperbarui)
    *   **1.1.4**: **TESTING (Master Data Models)**:
        *   Jalankan `python test_orm_definitions.py` setelah setiap perubahan signifikan.
        *   Buat/Update `tests/db/test_orm_master_data.py`: Tambahkan tes untuk query sederhana (`.first()`, `.count()`) pada setiap model master baru/yang direvisi. Tambahkan tes yang secara spesifik menguji setiap `relationship` penting dengan melakukan join atau mengakses atribut relasi.

*   **1.2**: **Definisi dan Uji Model untuk Sales & Piutang (`sales_models.py`)**:
    *   **Status**: ⚪ **BELUM DIMULAI/DIREVIEW ULANG SECARA MENYELURUH SETELAH FONDASI MASTER STABIL**
    *   **1.2.1**: **Implementasi dan Uji Model Sales & Piutang Kunci**:
        *   Definisikan/Review `ArRequestListH` (relasi ke `MasterCollector`, `CustomerPaymentH`).
        *   Definisikan/Review `GoodsIssueH` (relasi ke `SalesOrderH`, `MasterCustomer`, `MasterLocation`).
        *   Definisikan/Review `SalesOrderH` (relasi ke `MasterCustomer`, `MasterSales`, `MasterCurrency`, `GoodsIssueH`, `SalesInvoiceH`, `SalesOrderD`).
        *   Definisikan/Review `SalesOrderD` (relasi ke `SalesOrderH`, `MasterMaterial`, `MasterUnit`).
        *   Definisikan/Review `SalesInvoiceH` (relasi ke `SalesOrderH`, `GoodsIssueH`, `MasterCustomer`, `MasterSales`, `MasterCurrency`, `MasterLocation`, `SalesInvoiceD`, `Arbook`).
        *   Definisikan/Review `SalesInvoiceD` (relasi ke `SalesInvoiceH`, `MasterMaterial`, `MasterUnit`).
        *   Definisikan/Review `Arbook` (relasi ke `MasterCustomer`, `MasterTransactionType`, `MasterCurrency`, dan `SalesInvoiceH`).
        *   Definisikan/Review `CustomerPaymentH` (relasi ke `ArRequestListH`, `CustomerPaymentD`).
        *   Definisikan/Review `CustomerPaymentD` (relasi ke `CustomerPaymentH`, `MasterTransactionType`, `MasterCustomer`, `MasterCurrency`; perhatikan relasi `ARDocNo`).
        *   File terkait: `backend/app/db_models/sales_models.py` (dibuat/diisi/direview)
    *   **1.2.2**: Implementasikan Model Sales & Piutang Tambahan jika relevan untuk MVP (misalnya, `ArDownpayment`, `SalesReturnH/D`).
        *   File terkait: `backend/app/db_models/sales_models.py` (ditambahkan)
    *   **1.2.3**: Pastikan semua atribut diurutkan secara alfabetis.
    *   **1.2.4**: Update `backend/app/db_models/__init__.py`.
    *   **1.2.5**: **TESTING (Sales Models)**:
        *   Jalankan `python test_orm_definitions.py`.
        *   Buat/Update `tests/db/test_orm_sales.py`: Tes query sederhana per model, tes semua relasi penting (ke master data dan antar model sales).

*   **1.3**: **Definisi dan Uji Model untuk Inventaris (`inventory_models.py`)**:
    *   **Status**: ⚪ **BELUM DIMULAI**
    *   **1.3.1**: Implementasikan model ORM untuk tabel inventaris kunci: `GoodsIssueD`, `GoodsReceiptH`, `GoodsReceiptD`, `StockBalance`, `Stock`, `Batch`, `AdjustInH/D`, `AdjustOutH/D`, `StockTransferH/D`, dll. Definisikan relasi. Atribut diurutkan.
        *   File terkait: `backend/app/db_models/inventory_models.py` (dibuat/diisi)
    *   **1.3.2**: Update `backend/app/db_models/__init__.py`.
    *   **1.3.3**: **TESTING (Inventory Models)**:
        *   Jalankan `python test_orm_definitions.py`.
        *   Buat/Update `tests/db/test_orm_inventory.py`: Tes query dan relasi.

*   **1.4 - 1.x (Prioritas Lebih Rendah untuk MVP Awal, kecuali ada dependensi kuat dari query utama penjualan/piutang)**:
    *   **Purchase Models (`purchase_models.py`)**
    *   **Production Models (`production_models.py`)**
    *   **Finance Models (GL Umum) (`finance_models.py`)**
    *   (Lakukan Definisi Model, Update `__init__.py`, TESTING untuk masing-masing jika diperlukan)

*   **1.8**: **Final Review dan Pengujian Impor serta Relasi Model ORM Menyeluruh untuk Cakupan MVP**:
    *   **Status**: ⚪ **BELUM DIMULAI**
    *   **1.8.1**: Lakukan review menyeluruh terhadap semua definisi model dan relasi yang dibuat untuk cakupan query MVP.
    *   **1.8.2**: Jalankan `python test_orm_definitions.py` dan semua file tes ORM spesifik (`test_orm_master_data.py`, `test_orm_sales.py`, `test_orm_inventory.py`, dll.). Pastikan semua tes berhasil.

---

**STEP 2: Konfigurasi dan Inisialisasi Engine serta Session SQLAlchemy**
*   **Status**: ✅ **SELESAI** (file `session.py` sudah dibuat dan tes koneksi dasar berhasil).
    *   **2.1 - 2.4**: Implementasi `DATABASE_URL`, `engine`, `SessionLocal`, `get_db_session()`.
    *   **2.5**: **TESTING (STEP 2 Lanjutan)**:
        *   **2.5.1**: (Sudah direncanakan) Buat direktori `tests/db/` dan file tes ORM spesifik per kategori (misalnya, `test_orm_master_data.py`, `test_orm_sales.py`).
        *   **2.5.2**: (Akan dilakukan setelah STEP 1.8 selesai) Di setiap file tes ORM per kategori, tulis dan jalankan tes yang melakukan query representatif (SELECT, FILTER sederhana, JOIN melalui relasi) pada model-model di kategori tersebut menggunakan sesi DB asli ke `sim_testgeluran` sampel. Verifikasi tipe data hasil dan tidak adanya error eksekusi.

---

**STEP 3: Refactoring `execute_query_node` untuk Menggunakan ORM**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **3.1**: Rencanakan struktur fungsi baru `_build_and_execute_orm_query(plan: DatabaseOperation, db_session: Session, models_map: dict)` di `execute_query.py`. `models_map` akan memetakan nama tabel string ke objek kelas model SQLAlchemy.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.2**: Modifikasi fungsi `execute_query_node` utama untuk:
        *   Mendapatkan sesi SQLAlchemy (misalnya, dengan memanggil `get_db_session()` atau menerimanya dari `agent_service`).
        *   Membuat `models_map` yang berisi semua model ORM yang sudah diimpor dari `backend.app.db_models`.
        *   Memanggil `_build_and_execute_orm_query` untuk setiap operasi dalam `database_operations_plan` dan `raw_data_operation_plan`.
        *   Menangani penutupan sesi SQLAlchemy.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.3**: Implementasikan logika detail di `_build_and_execute_orm_query` untuk:
        *   **3.3.1**: Menerjemahkan `plan.select_columns` menjadi argumen untuk `db_session.query(*selectable_entities)`. Tangani alias (`.label()`) dan fungsi agregasi (`func.sum()`, `func.count()`, dll.). Dapatkan objek model dari `models_map` berdasarkan `main_table`.
        *   **3.3.2**: Menerapkan `JOIN` (`.join(TargetModel, join_condition, isouter=...)`) berdasarkan `plan.joins`. Dapatkan `TargetModel` dari `models_map`. Bangun `join_condition` secara dinamis dari `on_conditions`.
        *   **3.3.3**: Menerapkan `FILTER` (`.filter(filter_expression)`) berdasarkan `plan.filters` dan struktur `LogicalFilterGroup`/`FilterCondition`. Gunakan `and_`, `or_` SQLAlchemy.
        *   **3.3.4**: Menerapkan `GROUP BY` (`.group_by(*group_by_expressions)`) berdasarkan `plan.group_by_columns`.
        *   **3.3.5**: Menerapkan `HAVING` (`.having(having_expression)`) berdasarkan `plan.having_conditions`.
        *   **3.3.6**: Menerapkan `ORDER BY` (`.order_by(*order_by_expressions)`) berdasarkan `plan.order_by_clauses`. Tangani `asc` dan `desc`.
        *   **3.3.7**: Menerapkan `LIMIT` (`.limit()`) dan `OFFSET` (`.offset()`).
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.4**: Implementasikan eksekusi query ORM (`.all()`, `.first()`, `.scalar_one_or_none()`) dan konversi hasilnya (list of RowProxy atau objek model) menjadi format `List[Dict[str, Any]]` atau nilai tunggal yang diharapkan oleh `AgentState`.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.5**: Hapus fungsi lama `_build_sql_from_operation` dan semua referensinya.
        *   File terkait: `backend/app/langgraph_workflow/nodes/execute_query.py`
    *   **3.6**: **TESTING (STEP 3)**:
        *   Buat file `tests/nodes/test_execute_query_orm.py`.
        *   Tulis unit test ekstensif untuk fungsi `_build_and_execute_orm_query` dengan *mock* `db_session` dan berbagai `DatabaseOperationPlan` untuk setiap klausa SQL. Verifikasi objek query SQLAlchemy yang dibangun (sebelum eksekusi) sudah benar.
        *   Tulis integration test untuk `execute_query_node` secara keseluruhan, memanggilnya dengan `AgentState` yang berisi `DatabaseOperationPlan` representatif untuk query penjualan dan piutang. Gunakan sesi DB asli ke `sim_testgeluran` sampel. Verifikasi `financial_calculations`, `raw_query_results`, dan `query_execution_status` di `AgentState` output.

---

**STEP 4: Pengujian End-to-End Awal dengan ORM**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **4.1**: Jalankan alur kerja LangGraph secara end-to-end (melalui API `POST /api/v1/query` menggunakan Postman/Insomnia atau tes API otomatis) untuk skenario query penjualan sederhana dan piutang customer sederhana.
    *   **4.2**: Analisis log, `DatabaseOperationPlan` yang dihasilkan `plan_execution_node`, dan output `AgentState` dari `execute_query_node` (yang kini menggunakan ORM) dan `replace_placeholders_node`.
    *   **4.3**: Identifikasi dan perbaiki bug pada penerjemahan `DatabaseOperationPlan` ke ORM, eksekusi query ORM, atau pada pemrosesan hasil.
    *   **4.4**: **TESTING (STEP 4)**:
        *   E2E test untuk beberapa query dasar (agregasi tunggal, filter tanggal, join sederhana).
        *   Verifikasi `final_narrative`, `data_table_for_display`, dan `executive_summary` yang dihasilkan akurat.
        *   Periksa log untuk memastikan tidak ada error tak terduga dari SQLAlchemy atau node-node lain.

---

**STEP 5: Penyesuaian `plan_execution_node` dan Prompt LLM (Optimalisasi untuk ORM)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **5.1**: Berdasarkan pengalaman di STEP 3 & 4, evaluasi apakah struktur `DatabaseOperationPlan` saat ini sudah optimal untuk diterjemahkan ke query ORM atau apakah ada penyederhanaan yang bisa dilakukan pada `DatabaseOperationPlan` (dan pada prompt LLM di `plan_execution_node`) karena ORM kini menangani banyak detail SQL. (Contoh: LLM mungkin hanya perlu menyebutkan nama relasi untuk join).
    *   **5.2**: Jika diputuskan untuk menyesuaikan `DatabaseOperationPlan`, perbarui definisi `DatabaseOperationPlan` dan sub-komponennya di `backend/app/schemas/agent_state.py`.
    *   **5.3**: Perbarui template prompt LLM (di `backend/app/langgraph_workflow/nodes/planning_prompts/`) untuk menghasilkan `DatabaseOperationPlan` dengan struktur baru/yang dioptimalkan.
    *   **5.4**: Sesuaikan logika di `_build_and_execute_orm_query` di `execute_query_node` untuk mengakomodasi struktur `DatabaseOperationPlan` yang baru (jika ada perubahan).
    *   **5.5**: **TESTING (STEP 5)**:
        *   Uji ulang `plan_execution_node` untuk memastikan ia menghasilkan `DatabaseOperationPlan` sesuai format baru.
        *   Uji ulang `execute_query_node` dengan `DatabaseOperationPlan` format baru.
        *   Uji ulang E2E untuk query-query yang relevan.

---

**STEP 6: Implementasi Dukungan untuk Query Lebih Kompleks dengan ORM (Skenario MVP)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **6.1**: Fokus pada implementasi dan pengujian skenario query MVP yang lebih kompleks (misalnya, piutang customer dengan berbagai filter dan agregasi, analisis penjualan dengan multiple join dan group by, query yang memerlukan subquery jika `DatabaseOperationPlan` bisa merepresentasikannya) menggunakan ORM.
    *   **6.2**: Lakukan pengujian E2E untuk semua skenario query piutang customer dan analisis penjualan yang telah ditentukan sebagai target MVP.
    *   **6.3**: Iterasi pada prompt LLM (`plan_execution_node`) dan logika `_build_and_execute_orm_query` (`execute_query_node`) sampai semua skenario query target MVP berhasil diimplementasikan dan menghasilkan data yang akurat.
    *   **6.4**: **TESTING (STEP 6)**:
        *   E2E test menyeluruh untuk semua skenario query utama MVP.
        *   Validasi akurasi data output secara ketat terhadap database sampel.
        *   Pastikan penanganan error (misalnya, jika LLM menghasilkan rencana yang tidak bisa diterjemahkan ORM dengan benar) berfungsi dengan baik dan menghasilkan pesan error yang informatif bagi pengguna.

---

**STEP 7: Pengembangan Frontend (React.js)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **7.1**: Implementasikan komponen UI React dasar: `QueryInterface` (input teks untuk query pengguna, tombol submit), `ResultsDisplay` (untuk menampilkan `final_narrative` dan `data_table_for_display`), `ExecutiveSummaryDisplay`, `WarningsDisplay`, `DataSourceInfoDisplay`.
        *   File terkait: `frontend/src/components/`
    *   **7.2**: Implementasikan logika di `frontend/src/services/agentApi.js` untuk mengirim request `POST /api/v1/query` ke backend FastAPI dan menerima respons.
    *   **7.3**: Hubungkan komponen-komponen di `frontend/src/App.js` atau `AIAgentDashboard.js` untuk alur dasar: input query -> kirim ke backend -> tampilkan hasil (narasi, tabel, ringkasan, peringatan, info sumber data).
    *   **7.4**: Implementasikan komponen UI monitoring (jika diputuskan untuk MVP awal, meskipun bisa ditunda): `SessionHeader`, `ContextUsageMeter`, `ProcessMonitor`, `PerformanceAnalytics`, `FallbackTracker` dengan data statis atau *mocked* terlebih dahulu.
    *   **7.5**: Styling dasar untuk semua komponen UI agar mudah digunakan.
    *   **7.6**: **TESTING (STEP 7)**:
        *   Unit test untuk komponen React individual menggunakan Jest & React Testing Library (misalnya, apakah input ter-render, apakah tabel menampilkan data mock dengan benar).
        *   Integration test Frontend: Tes pengiriman query dari `QueryInterface` dan penampilan hasil di `ResultsDisplay` dengan *mocking* API call ke backend (menggunakan `msw` atau library serupa).
        *   Tes manual UI dasar.

---

**STEP 8: Integrasi End-to-End Penuh (Backend + Frontend) dan Pemolesan MVP**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **8.1**: Hubungkan Frontend React.js yang sudah berfungsi dengan Backend FastAPI yang sudah menggunakan ORM dan telah diuji.
    *   **8.2**: Jika menggunakan SSE/WebSocket untuk update status real-time, implementasikan koneksi dan logika update di komponen UI monitoring Frontend. Jika tidak, pastikan informasi monitoring (jika ada) dari respons API final ditampilkan dengan benar.
    *   **8.3**: Lakukan pengujian E2E menyeluruh dari UI Frontend: masukkan berbagai query (sukses, error, data tidak ada), verifikasi tampilan hasil, narasi, tabel, ringkasan, peringatan, dan info sumber data.
    *   **8.4**: Perbaiki *bug* yang ditemukan pada integrasi Frontend-Backend dan lakukan pemolesan UI/UX berdasarkan feedback.
    *   **8.5**: Pastikan penanganan error dari backend ditampilkan dengan pesan yang ramah dan informatif di frontend.
    *   **8.6**: Buat atau lengkapi dokumentasi `README.md` yang menjelaskan cara setup lengkap (backend & frontend) dan menjalankan proyek.
    *   **8.7**: **TESTING (STEP 8)**:
        *   Jalankan semua kasus uji E2E yang telah didefinisikan (dari Dokumen Rencana Testing).
        *   Lakukan User Acceptance Testing (UAT) dengan perwakilan pengguna (atau Anda sendiri sebagai pengguna awal) untuk memastikan sistem memenuhi kebutuhan dasar MVP.
        *   Verifikasi semua fitur MVP berfungsi seperti yang diharapkan di lingkungan yang terintegrasi.
        *   Pastikan tidak ada *bug* kritis/mayor.

---

**STEP 9: Persiapan Deployment (Dasar)**
*   **Status**: ⚪ **BELUM DIMULAI**
    *   **9.1**: Buat `Dockerfile` untuk meng-containerize aplikasi backend FastAPI.
        *   File terkait: `backend/Dockerfile`
    *   **9.2**: Buat `Dockerfile` untuk meng-containerize aplikasi frontend React (misalnya, build statis yang di-serve oleh Nginx atau server statis lainnya).
        *   File terkait: `frontend/Dockerfile`
    *   **9.3**: Buat file `docker-compose.yml` untuk memudahkan menjalankan semua service (backend, frontend, database MySQL `sim_testgeluran`, Neo4j/Graphiti) secara lokal dalam container.
        *   File terkait: `docker-compose.yml`
    *   **9.4**: Tulis skrip atau instruksi untuk setup database dan Graphiti di dalam lingkungan Docker (misalnya, menggunakan skrip inisialisasi yang dijalankan saat container DB/Graphiti pertama kali start).
    *   **9.5**: **TESTING (STEP 9)**:
        *   Verifikasi aplikasi backend dan frontend bisa di-build menjadi image Docker.
        *   Verifikasi semua service bisa dijalankan bersamaan menggunakan `docker-compose up`.
        *   Lakukan tes fungsionalitas dasar pada aplikasi yang berjalan di Docker untuk memastikan semua koneksi antar service (Frontend -> Backend, Backend -> DB, Backend -> Neo4j, Backend -> LLM) berfungsi.




