
### **Dokumen Perencanaan: Struktur Folder Proyek (Final)**

**Versi:** 1.0

```
ai_agent_project_root/
|
├── .env                  # Variabel lingkungan global (di-ignore Git). Berisi semua kredensial.
├── .gitignore            # File untuk mengabaikan folder/file yang tidak perlu di-commit.
├── README.md             # Penjelasan umum proyek, cara setup, dan cara menjalankan.
├── docker-compose.yml    # (Opsional) Untuk menjalankan semua service (backend, db, dll) dengan mudah.
├── requirements.txt      # Dependensi Python untuk seluruh proyek backend.
|
├── backend/              # Semua kode untuk aplikasi backend utama dan server MCP.
│   │
│   ├── app/              # Direktori aplikasi FastAPI inti.
│   │   ├── __init__.py
│   │   ├── main.py       # Entry point aplikasi FastAPI utama (menggabungkan semua router).
│   │   │
│   │   ├── api/          # Modul untuk routing dan endpoint API.
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           └── query.py  # Endpoint untuk /api/v1/query & streaming (SSE).
│   │   │
│   │   ├── core/         # Konfigurasi inti dan utilitas aplikasi.
│   │   │   ├── __init__.py
│   │   │   └── config.py     # Membaca & menyediakan settings dari file .env.
│   │   │
│   │   ├── schemas/      # Semua model Pydantic untuk validasi data.
│   │   │   ├── __init__.py
│   │   │   ├── agent_state.py      # Definisi AgentState LangGraph.
│   │   │   ├── api_models.py       # Skema untuk request/response endpoint FastAPI.
│   │   │   └── graphiti_schema_nodes.py # Definisi node & edge Graphiti.
│   │   │
│   │   ├── services/     # Logika bisnis yang dipisahkan dari API.
│   │   │   ├── __init__.py
│   │   │   └── agent_service.py    # Service untuk mengorkestrasi LangGraph workflow.
│   │   │
│   │   └── langgraph_workflow/ # Semua komponen spesifik LangGraph.
│   │       ├── __init__.py
│   │       ├── graph.py            # Definisi StateGraph, penambahan node, & kompilasi.
│   │       │
│   │       └── nodes/              # Setiap node dalam alur kerja sebagai file terpisah.
│   │           ├── __init__.py
│   │           ├── router.py
│   │           ├── consult_schema.py
│   │           ├── plan_execution.py
│   │           ├── validate_plan.py
│   │           ├── execute_query.py
│   │           ├── validate_results.py
│   │           ├── replace_placeholders.py
│   │           ├── generate_acknowledgement.py
│   │           ├── generate_error_response.py
│   │           └── log_analytics.py
│   │
│   ├── mcp_servers/      # Implementasi MCP Server sebagai aplikasi mandiri.
│   │   ├── __init__.py
│   │   │
│   │   ├── mysql_server/ # MCP Server untuk database sim_testgeluran.
│   │   │   ├── __init__.py
│   │   │   ├── main.py           # FastAPI app untuk MySQL MCP Server.
│   │   │   ├── tools.py          # Implementasi tool execute_operation_plan.
│   │   │   └── db_models/        # Di sinilah model-model ORM Anda akan ditempatkan.
│   │   │       ├── __init__.py
│   │   │       ├── base.py
│   │   │       └── orm_*.py      # (orm_a_e.py, orm_f_h.py, dst.)
│   │   │
│   │   └── graphiti_server/ # MCP Server untuk knowledge graph.
│   │       ├── __init__.py
│   │       ├── main.py           # FastAPI app untuk Graphiti MCP Server.
│   │       └── tools.py          # Implementasi tools get_relevant_schema, store/retrieve data.
│   │
│   └── tests/            # Semua tes otomatis untuk backend.
│       ├── __init__.py
│       ├── test_main.py      # Contoh file tes.
│       └── conftest.py       # Fixtures untuk Pytest.
│
├── data_samples/         # File-file data statis untuk inisialisasi.
│   ├── schema.sql
│   ├── data.sql
│   └── graphiti_semantic_mapping.json
│
├── docs/                 # Semua dokumen perencanaan yang sudah kita buat.
│   ├── 1mvp_ai_agent_rancangan.md
│   ├── ... (dokumen lainnya)
│   └── todo_lists/
│       ├── 1_database_todo.md
│       ├── 2_backend_todo.md
│       └── 3_frontend_todo.md
│
├── frontend/             # Semua kode untuk aplikasi frontend React.
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/   # Komponen-komponen UI React.
│   │   └── services/     # Logika untuk memanggil API backend.
│   ├── package.json
│   └── .env
│
└── scripts/              # Skrip-skrip utilitas untuk development.
    ├── initialize_project.sh      # Skrip shell untuk menjalankan semua skrip inisialisasi.
    ├── initialize_db_mysql.py     # Skrip untuk setup database MySQL dari data_samples.
    ├── run_dev_servers.sh         # Skrip shell untuk menjalankan semua server development.
    └── sync_mysql_to_graphiti.py  # Skrip yang sudah Anda buat.
```

### **Penjelasan dan Rasionalisasi:**

1.  **Top-Level `backend/` dan `frontend/`:** Ini adalah praktik standar untuk memisahkan *concern* antara backend dan frontend. Ini memungkinkan tim yang berbeda (jika ada) untuk bekerja secara independen dan memudahkan proses *build* dan *deployment* yang terpisah.
2.  **Satu `.env` di Root:** Saya menempatkan file `.env` di level root proyek agar semua komponen backend (aplikasi utama dan semua MCP server) bisa berbagi konfigurasi yang sama. Ini menyederhanakan manajemen kredensial.
3.  **`backend/mcp_servers/`:** Setiap server MCP (mysql, graphiti) ditempatkan dalam direktorinya sendiri. Masing-masing memiliki `main.py` sendiri. Ini adalah desain yang sangat modular. Untuk MVP, kita bisa menjalankannya dalam satu proses, tetapi struktur ini memungkinkan kita untuk menjalankannya sebagai *microservice* terpisah di masa depan dengan mudah.
4.  **`db_models/` di dalam `mysql_server/`:** Model ORM Anda sangat spesifik untuk database `sim_testgeluran`. Menempatkannya langsung di dalam `mysql_server` adalah lokasi yang paling logis, karena hanya server inilah yang akan menggunakannya. Ini mengikuti prinsip *encapsulation*.
5.  **`backend/app/langgraph_workflow/nodes/`:** Setiap node LangGraph akan menjadi file Python tersendiri. Ini membuat alur kerja di `graph.py` menjadi sangat bersih dan mudah dibaca, karena hanya akan berisi logika untuk merangkai node, bukan implementasi detail dari setiap node.
6.  **`scripts/`:** Mengumpulkan semua skrip utilitas di satu tempat membuat proses *onboarding* untuk developer baru menjadi sangat mudah. Mereka hanya perlu menjalankan satu skrip (`initialize_project.sh`) untuk menyiapkan seluruh lingkungan kerja.

Struktur ini memberikan keseimbangan yang baik antara organisasi, modularitas, dan kemudahan penggunaan untuk MVP, sambil tetap menyediakan jalur yang jelas untuk skalabilitas di masa depan.
