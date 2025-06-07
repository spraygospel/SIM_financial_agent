Baik, terima kasih atas klarifikasinya! Ini poin yang sangat penting.

**Kita akan memastikan bahwa semua perencanaan dan implementasi MVP difokuskan untuk koneksi langsung ke database MySQL, bukan SQLite.**

Dokumen "Inisialisasi Data dan Skema" yang sebelumnya kita buat akan tetap relevan, namun kita akan menyesuaikan bagian "Proses Inisialisasi Database" agar mengacu pada MySQL, bukan SQLite in-memory. File `schema.sql` dan `data.sql` akan digunakan untuk setup database MySQL development/testing.

Sekarang, mari kita lanjutkan dengan membuat **Dokumen Struktur Folder Proyek**.

---

**Dokumen Perencanaan Tambahan 8: Struktur Folder Proyek**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
2.  Struktur Folder Utama
3.  Deskripsi Folder dan File Kunci
    3.1. `ai_agent_mysql/` (Direktori Root Proyek Backend)
    3.2. `frontend/` (Direktori Root Proyek Frontend)
    3.3. `mcp_servers/`
    3.4. `docs/`
    3.5. `tests/`
    3.6. `scripts/`
    3.7. File Konfigurasi Root
4.  Pertimbangan

---

**1. Pendahuluan**

Dokumen ini mendefinisikan struktur folder yang diusulkan untuk proyek MVP AI Agent. Struktur folder yang baik penting untuk organisasi kode, kemudahan navigasi, skalabilitas, dan kolaborasi tim. Struktur ini dirancang untuk mengakomodasi semua komponen yang telah direncanakan, termasuk backend FastAPI, LangGraph workflow, MCP Servers, dan frontend React.js.

---

**2. Struktur Folder Utama**

```
ai_agent_project_root/
├── backend/                          # Semua kode backend (FastAPI, LangGraph, dll.)
│   ├── app/                          # Direktori utama aplikasi FastAPI
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point aplikasi FastAPI
│   │   ├── api/                      # Modul untuk routing dan endpoint API
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           └── query.py      # Endpoint untuk /api/v1/query
│   │   ├── core/                     # Konfigurasi inti, settings
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── schemas/                  # Pydantic models untuk request/response API & state
│   │   │   ├── __init__.py
│   │   │   ├── mcp_schemas.py    # Skema data untuk interaksi MCP
│   │   │   ├── api_models.py     # Skema data untuk endpoint FastAPI
│   │   │   └── agent_state.py    # Definisi AgentState LangGraph
│   │   ├── services/                 # Logika bisnis, interaksi dengan LangGraph
│   │   │   ├── __init__.py
│   │   │   └── agent_service.py  # Service untuk memproses query via LangGraph
│   │   └── langgraph_workflow/       # Komponen-komponen LangGraph
│   │       ├── __init__.py
│   │       ├── graph.py              # Definisi dan kompilasi graph utama
│   │       ├── nodes/                # Direktori untuk setiap node LangGraph
│   │       │   ├── __init__.py
│   │       │   ├── understand_query.py
│   │       │   ├── consult_schema.py
│   │       │   ├── plan_execution.py
│   │       │   ├── execute_query.py
│   │       │   ├── validate_results.py
│   │       │   ├── replace_placeholders.py
│   │       │   └── generate_error_response.py
│   │       └── utils/                # Fungsi utilitas untuk workflow
│   │           ├── __init__.py
│   │           └── helpers.py
│   ├── mcp_servers/                  # Implementasi MCP Servers
│   │   ├── __init__.py
│   │   ├── graphiti_server/
│   │   │   ├── __init__.py
│   │   │   ├── main.py               # FastAPI app untuk Graphiti MCP Server
│   │   │   └── tools.py              # Implementasi tools Graphiti MCP
│   │   ├── mysql_server/
│   │   │   ├── __init__.py
│   │   │   ├── main.py               # FastAPI app untuk MySQL MCP Server
│   │   │   └── tools.py              # Implementasi tools MySQL MCP
│   │   └── placeholder_system_server/
│   │       ├── __init__.py
│   │       ├── main.py               # FastAPI app untuk Placeholder MCP Server
│   │       └── tools.py              # Implementasi tools Placeholder MCP
│   ├── tests/                        # Tes untuk backend
│   │   ├── __init__.py
│   │   ├── unit/
│   │   └── integration/
│   ├── .env                          # Variabel lingkungan backend (di-ignore Git)
│   ├── Dockerfile                    # Untuk containerisasi backend
│   └── requirements.txt              # Dependensi Python backend
│
├── frontend/                         # Semua kode frontend (React.js)
│   ├── public/
│   ├── src/
│   │   ├── components/               # Komponen UI React (sesuai ai_agent_ui_components.js)
│   │   │   ├── AIAgentDashboard.js
│   │   │   ├── SessionHeader.js
│   │   │   ├── ContextUsageMeter.js
│   │   │   ├── ProcessMonitor.js
│   │   │   ├── PerformanceAnalytics.js
│   │   │   ├── FallbackTracker.js
│   │   │   ├── QueryInterface.js
│   │   │   └── ResultsDisplay.js
│   │   ├── services/                 # Logika untuk memanggil API backend
│   │   │   └── agentApi.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── App.css
│   ├── .env.development              # Variabel lingkungan frontend (dev)
│   ├── .env.production               # Variabel lingkungan frontend (prod)
│   ├── package.json
│   └── Dockerfile                    # Opsional, jika frontend di-containerize terpisah
│
├── docs/                             # Semua dokumen perencanaan
│   ├── 1mvp_ai_agent_rancangan.md
│   ├── 2_contoh.md
│   ├── 3_langgraph_nodes_detail.md
│   ├── perencanaan_tambahan/
│   │   ├── 1_spesifikasi_mcp_server.md
│   │   ├── 2_detail_state_langgraph_nodes.md
│   │   ├── 3_arsitektur_aliran_data.md
│   │   ├── 4_desain_api_backend.md
│   │   ├── 5_strategi_error_fallback.md
│   │   ├── 6_rencana_testing.md
│   │   ├── 7_inisialisasi_data_skema.md
│   │   └── 8_struktur_folder_proyek.md (dokumen ini)
│
├── scripts/                          # Skrip-skrip pendukung
│   ├── initialize_db.py            # Skrip untuk inisialisasi DB MySQL & Graphiti (dari schema.sql, data.sql)
│   ├── run_dev_servers.sh          # Skrip untuk menjalankan semua server development
│
├── data_samples/                     # File data sampel untuk inisialisasi
│   ├── schema.sql
│   └── data.sql
│
├── .gitignore
├── README.md
└── docker-compose.yml                # Opsional, untuk menjalankan semua service (backend, frontend, db, graphiti) secara lokal
```

---

**3. Deskripsi Folder dan File Kunci**

**3.1. `backend/` (Direktori Root Proyek Backend)**
*   **`app/`**: Kode utama aplikasi FastAPI.
    *   **`main.py`**: Titik masuk aplikasi FastAPI, tempat semua *router* dan konfigurasi global dimuat.
    *   **`api/v1/endpoints/query.py`**: Implementasi *endpoint* `POST /api/v1/query` dan (jika ada) `GET /api/v1/stream_updates/{session_id}`.
    *   **`core/config.py`**: Pengaturan konfigurasi aplikasi (misalnya, URL database MySQL, URL Graphiti, kunci API LLM).
    *   **`schemas/`**: Berisi semua model Pydantic.
        *   `mcp_schemas.py`: Model untuk request/response tool MCP.
        *   `api_models.py`: Model untuk request/response endpoint FastAPI.
        *   `agent_state.py`: Definisi `TypedDict` atau Pydantic model untuk `AgentState` LangGraph.
    *   **`services/agent_service.py`**: Berisi logika untuk menerima request dari API, memanggil LangGraph workflow, dan memformat respons.
    *   **`langgraph_workflow/`**: Semua yang terkait dengan LangGraph.
        *   `graph.py`: Tempat `StateGraph` didefinisikan, node ditambahkan, dan graph di-*compile*.
        *   `nodes/`: Setiap file Python di sini akan mengimplementasikan logika satu node LangGraph.
*   **`mcp_servers/`**: Sub-direktori untuk setiap implementasi MCP Server.
    *   Setiap sub-direktori (misal, `graphiti_server/`) akan berisi aplikasi FastAPI kecilnya sendiri (`main.py`) yang mengekspos *tools* MCP (`tools.py`). Ini memungkinkan setiap MCP server dijalankan sebagai proses terpisah jika diperlukan.
*   **`tests/`**: Tes unit dan integrasi untuk backend.
*   **`.env`**: Menyimpan variabel lingkungan sensitif (misalnya, kredensial database). **JANGAN di-commit ke Git.**
*   **`Dockerfile`**: Untuk membangun image Docker aplikasi backend utama.
*   **`requirements.txt`**: Daftar dependensi Python untuk backend.

**3.2. `frontend/` (Direktori Root Proyek Frontend)**
*   Struktur standar proyek React (misalnya, yang dibuat dengan `create-react-app` atau Vite).
*   **`src/components/`**: Berisi file-file komponen UI React seperti `AIAgentDashboard.js` dan lainnya yang telah Anda rencanakan.
*   **`src/services/agentApi.js`**: Fungsi untuk melakukan panggilan API ke backend FastAPI.

**3.3. `mcp_servers/` (di dalam `backend/`)**
*   Seperti dijelaskan di atas, ini adalah tempat implementasi kode untuk masing-masing MCP Server. Setiap MCP Server bisa menjadi aplikasi FastAPI mandiri atau modul Python yang diimpor oleh aplikasi FastAPI utama jika dijalankan dalam satu proses (kurang ideal untuk skalabilitas). Untuk MVP, menjalankan mereka sebagai FastAPI apps terpisah (meski mungkin pada port berbeda di mesin yang sama) lebih baik untuk modularitas.

**3.4. `docs/`**
*   Tempat semua dokumen perencanaan proyek disimpan, termasuk dokumen ini.

**3.5. `tests/` (di dalam `backend/`)**
*   Pengujian otomatis untuk backend.
*   `unit/`: Tes untuk fungsi atau kelas individual.
*   `integration/`: Tes untuk interaksi antar komponen backend (misalnya, `agent_service` dengan `langgraph_workflow`).

**3.6. `scripts/`**
*   **`initialize_db.py`**: Skrip untuk menjalankan `schema.sql` dan `data.sql` pada database MySQL development/testing, dan untuk mempopulasi Graphiti dengan metadata skema.
*   **`run_dev_servers.sh`**: Skrip shell untuk memudahkan menjalankan semua server yang dibutuhkan selama development (FastAPI utama, MCP servers, mungkin Graphiti jika dijalankan lokal).

**3.7. File Konfigurasi Root**
*   **`.gitignore`**: Mengabaikan file dan folder yang tidak perlu di-commit (misalnya, `__pycache__`, `.env`, `node_modules`, `build`).
*   **`README.md`**: Informasi umum tentang proyek, cara setup, dan cara menjalankan.
*   **`docker-compose.yml` (Opsional)**: Jika Anda ingin menggunakan Docker Compose untuk mengelola semua service (backend, frontend, database MySQL, Graphiti) secara lokal selama development.

---

**4. Pertimbangan**

*   **Monorepo vs. Multirepo**: Struktur di atas adalah pendekatan *monorepo* (satu repository untuk backend dan frontend). Jika proyek berkembang sangat besar, pemisahan menjadi repository terpisah bisa dipertimbangkan.
*   **MCP Server Deployment**: Untuk MVP, MCP Server bisa dijalankan sebagai bagian dari proses backend utama atau sebagai proses terpisah di mesin yang sama. Untuk produksi, mereka idealnya adalah layanan mikro terpisah.
*   **Skalabilitas**: Struktur ini mencoba memisahkan *concerns*, yang akan membantu skalabilitas di masa depan.
*   **Konfigurasi**: Penggunaan file `.env` dan `core/config.py` (untuk backend) serta `.env.development` / `.env.production` (untuk frontend) penting untuk manajemen konfigurasi yang baik.

---
