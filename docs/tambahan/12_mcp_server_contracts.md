
### **Dokumen Teknis: 12_mcp_server_contracts.md**

**Versi Dokumen**: 1.0
**Tanggal**: (Tanggal saat ini)

---

## **Bab 1: Pendahuluan dan Prinsip Desain**

### **1.1. Tujuan Dokumen**

Dokumen ini berfungsi sebagai **"Kontrak Teknis"** atau spesifikasi API untuk setiap **Model Context Protocol (MCP) Server** yang digunakan dalam ekosistem AI Agent kita. Tujuannya adalah untuk mendefinisikan secara jelas dan tegas:

*   *Tools* (fungsi) apa saja yang diekspos oleh setiap server.
*   Struktur data (payload) untuk *request* (permintaan) yang harus dikirim oleh AI Agent (sebagai MCP Client).
*   Struktur data (payload) untuk *response* (jawaban) yang akan diterima oleh AI Agent.

Dokumen ini adalah panduan utama bagi para developer yang akan membangun, memelihara, atau mengintegrasikan MCP Server ini, serta bagi tim yang mengembangkan logika di dalam node-node LangGraph yang akan memanggil server-server ini.

### **1.2. Prinsip Desain Interaksi Client-Server**

Interaksi antara AI Agent (Client) dan MCP Server didasarkan pada prinsip **pendelegasian dan abstraksi** untuk memaksimalkan keamanan dan modularitas.

1.  **Agent sebagai Perencana (The Planner):**
    *   AI Agent Core (LangGraph) bertanggung jawab untuk **perencanaan tingkat tinggi**. Ia memahami permintaan pengguna dan membuat sebuah **rencana abstrak** (misalnya, `DatabaseOperationPlan`).
    *   Agent **tidak tahu dan tidak peduli** bagaimana cara terhubung ke database, bagaimana sintaks ORM bekerja, atau bagaimana query Cypher ditulis. Ia hanya tahu *tool* apa yang harus dipanggil dan format "rencana" apa yang harus dikirim.

2.  **Server sebagai Eksekutor Ahli (The Expert Executor):**
    *   Setiap MCP Server adalah **ahli di domainnya masing-masing**. `sim_testgeluran_server` adalah ahli database MySQL. `graphiti_server` adalah ahli *knowledge graph*.
    *   Server menerima **rencana abstrak** dari agent dan bertanggung jawab penuh untuk menerjemahkannya menjadi perintah teknis yang konkret (query ORM, query Cypher).
    *   Server menyembunyikan semua kompleksitas implementasi dari agent. Agent tidak perlu tahu apakah di balik layar server menggunakan SQLAlchemy, Django ORM, atau pustaka lainnya.

### **1.3. Ilustrasi Prinsip Interaksi**

Alur komunikasi secara konseptual adalah sebagai berikut:

```ascii
+---------------------------------+      +--------------------------------+
|      AI AGENT (MCP Client)      |      |     MCP SERVER (Ahli Domain)   |
|---------------------------------|      |--------------------------------|
| 1. "Saya punya Rencana Kerja   |----->| 4. "Baik, saya terima Rencana   |
|    (JSON) untuk mendapatkan     |      |    Kerja ini."                 |
|    data piutang."               |      |                                |
|                                 |      | 5. (Menerjemahkan Rencana ke   |
|                                 |      |    perintah teknis, misal ORM, |
|                                 |      |    dan mengeksekusinya ke      |
|                                 |      |    sumber data)                |
|                                 |      |                                |
| 3. "Baik, saya terima Laporan   |<-----| 6. "Ini Laporan Hasilnya        |
|    Hasilnya (JSON)."             |      |    (JSON)."                   |
+---------------------------------+      +--------------------------------+
```

Dengan mematuhi kontrak yang didefinisikan dalam dokumen ini, kita memastikan bahwa kedua komponen dapat dikembangkan dan diperbarui secara independen, selama "bahasa" (struktur payload) yang mereka gunakan untuk berkomunikasi tetap sama.
---

## **Bab 2: Kontrak untuk `graphiti_server`**

### **2.1. Deskripsi Umum**

`graphiti_server` bertindak sebagai "Pustakawan" dan "Petugas Loker" untuk AI Agent. Ia memiliki dua tanggung jawab utama:
1.  **Menyediakan "Peta Data" (Skema):** Memberikan informasi tentang struktur database operasional agar agent bisa membuat rencana yang cerdas.
2.  **Mengelola "Memori Kerja" Sesi:** Menyimpan dan mengambil data hasil query untuk setiap sesi percakapan, sehingga `AgentState` tetap ringan.

Server ini mengekspos tiga *tools* utama untuk memenuhi tanggung jawab tersebut.

---

### **2.2. Tool 1: `get_relevant_schema`**

*   **Deskripsi**: Mengambil potongan skema database yang relevan dari *knowledge graph* Neo4j berdasarkan `intent` dan `entities` dari permintaan pengguna.
*   **Dipanggil oleh Node**: `consult_schema_node`.

#### **Request Payload**
```json
{
  "intent": "EXECUTE_QUERY",
  "entities": ["sales", "monthly_data"]
}
```

#### **Response Payload (Sukses)**
```json
{
  "success": true,
  "relevant_tables": [
    {
      "table_name": "sales_orders",
      "purpose": "Mencatat semua transaksi penjualan.",
      "business_category": "financial_transaction",
      "columns": [
        {
          "name": "order_date",
          "type_from_db": "DATE",
          "classification": "temporal",
          "is_aggregatable": false
        },
        {
          "name": "total_amount",
          "type_from_db": "DECIMAL(18, 2)",
          "classification": "financial_amount",
          "is_aggregatable": true
        }
      ]
    }
  ],
  "table_relationships": [
    {
      "from_table": "order_lines",
      "from_column": "order_id",
      "to_table": "sales_orders",
      "to_column": "order_id",
      "relationship_type": "FOREIGN_KEY"
    }
  ]
}
```

#### **Response Payload (Error)**
```json
{
  "success": false,
  "error": "Tidak dapat menemukan skema yang relevan untuk entitas 'xyz'."
}
```

---

### **2.3. Tool 2: `store_session_data`**

*   **Deskripsi**: Menerima satu set data (misalnya, hasil query dari `sim_testgeluran_server`), menyimpannya sebagai `Episode` baru di Graphiti, dan mengembalikan `DataHandle` sebagai referensi (kunci loker).
*   **Dipanggil oleh Node**: `execute_query_node`.

#### **Request Payload**
```json
{
  "session_id": "user_123_session_002",
  "data_to_store": [
    { "customer_name": "PT ABC Corp", "outstanding_amount": 15000000 },
    { "customer_name": "CV XYZ", "outstanding_amount": 8500000 }
  ],
  "metadata": {
    "data_description": "Daftar customer belum lunas",
    "source_operation_id": "get_raw_outstanding_details",
    "column_schema": [
      {"name": "customer_name", "type": "string"},
      {"name": "outstanding_amount", "type": "decimal"}
    ]
  }
}
```
*   **Catatan**: `session_id` akan digunakan sebagai `group_id` di Graphiti untuk isolasi data.

#### **Response Payload (Sukses)**
Mengembalikan objek `DataHandle` yang lengkap.
```json
{
  "success": true,
  "data_handle": {
    "data_handle_id": "ep-raw-uuid-xyz-123",
    "storage_location": "Graphiti",
    "group_id": "user_123_session_002",
    "data_description": "Daftar customer belum lunas",
    "source_operation_id": "get_raw_outstanding_details",
    "row_count": 2,
    "column_schema": [
      {"name": "customer_name", "type": "string"},
      {"name": "outstanding_amount", "type": "decimal"}
    ],
    "created_at": "2024-10-27T10:00:10Z"
  }
}
```

---

### **2.4. Tool 3: `retrieve_session_data`**

*   **Deskripsi**: Menerima `data_handle_id`, menemukannya di Graphiti (memastikan `group_id` cocok dengan `session_id` saat ini untuk keamanan), dan mengembalikan data mentah yang tersimpan.
*   **Dipanggil oleh Node**: `validate_results_node`, `replace_placeholders_node`.

#### **Request Payload**
```json
{
  "session_id": "user_123_session_002",
  "data_handle_id": "ep-raw-uuid-xyz-123"
}
```

#### **Response Payload (Sukses)**
```json
{
  "success": true,
  "retrieved_data": [
    { "customer_name": "PT ABC Corp", "outstanding_amount": 15000000 },
    { "customer_name": "CV XYZ", "outstanding_amount": 8500000 }
  ]
}
```

#### **Response Payload (Error)**
```json
{
  "success": false,
  "error": "Data dengan handle_id 'ep-raw-uuid-xyz-123' tidak ditemukan untuk sesi ini."
}
```
---

Kontrak ini memastikan bahwa `graphiti_server` dapat menjalankan perannya sebagai "Pustakawan" dan "Petugas Loker" dengan andal, memungkinkan agent untuk fokus pada tugas-tugas tingkat tinggi.


## **Bab 3: Kontrak untuk `sim_testgeluran_server`**

### **3.1. Deskripsi Umum**

`sim_testgeluran_server` bertindak sebagai **"Manajer Departemen Database"** yang sangat ahli dan aman. Ini adalah satu-satunya komponen dalam seluruh ekosistem yang memiliki izin untuk berkomunikasi langsung dengan database operasional MySQL `sim_testgeluran`.

Peran utamanya adalah menerima **rencana kerja abstrak** (`DatabaseOperationPlan`) dari AI Agent, menerjemahkannya menjadi query **SQLAlchemy ORM** yang aman, mengeksekusinya, dan mengembalikan hasilnya dalam format JSON yang terstruktur. Server ini sepenuhnya menyembunyikan kompleksitas database dari agent.

Server ini hanya mengekspos satu *tool* yang sangat kuat.

---

### **3.2. Tool 1: `execute_operation_plan`**

*   **Deskripsi**: Menerima satu atau lebih `DatabaseOperation` dalam satu batch, mengeksekusi setiap operasi secara berurutan, dan mengembalikan hasil dari setiap operasi tersebut.
*   **Dipanggil oleh Node**: `execute_query_node`.

#### **Request Payload**

Request payload adalah sebuah objek JSON yang berisi satu kunci utama, `operations`, yang merupakan sebuah *list* dari objek `DatabaseOperation`.

```json
{
  "operations": [
    // Operasi 1: Untuk mengambil data agregat (ringkasan)
    {
      "operation_id": "get_summary_stats",
      "purpose": "Menghitung ringkasan data piutang customer",
      "main_table": "arbook",
      "select_columns": [
        {"field_name": "arbook.CustomerCode", "aggregation": "COUNT_DISTINCT", "alias": "TOTAL_CUSTOMERS_OUTSTANDING"},
        {"field_name": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "aggregation": "SUM", "alias": "TOTAL_OUTSTANDING_AMOUNT", "is_expression": true}
      ],
      "filters": {
        "logical_operator": "AND",
        "conditions": [{"field_or_expression": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "operator": ">", "value": 0, "is_expression": true}]
      },
      "result_key": "SUMMARY_STATS",
      "expected_result_format": "single_value"
    },
    // Operasi 2: Untuk mengambil data mentah (tabel)
    {
      "operation_id": "get_raw_outstanding_details",
      "purpose": "Mengambil daftar detail piutang customer",
      "main_table": "arbook",
      "select_columns": [
          {"field_name": "mastercustomer.Name", "alias": "Customer Name"},
          {"field_name": "arbook.DocNo", "alias": "Invoice Number"},
          {"field_name": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "alias": "Outstanding", "is_expression": true}
      ],
      "joins": [
          {"target_table": "mastercustomer", "type": "INNER", "on_conditions": [{"left_table_field": "arbook.CustomerCode", "right_table_field": "mastercustomer.Code"}]}
      ],
      "filters": {
        "logical_operator": "AND",
        "conditions": [{"field_or_expression": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "operator": ">", "value": 0, "is_expression": true}]
      },
      "order_by_clauses": [{"field_or_expression": "Outstanding", "direction": "DESC"}],
      "limit": 50,
      "result_key": "RAW_DATA_TABLE",
      "expected_result_format": "list_of_dicts"
    }
  ]
}
```
*Catatan: Struktur detail dari `DatabaseOperation` (seperti `select_columns`, `filters`, `joins`) harus mengikuti definisi yang ada di `backend/app/schemas/agent_state.py`.*

#### **Response Payload (Sukses)**

Responsnya adalah sebuah objek JSON yang berisi hasil dari setiap operasi yang diminta. Kunci dari setiap hasil adalah `operation_id` yang dikirim dalam request.

```json
{
  "success": true,
  "results": {
    "get_summary_stats": {
      "status": "success",
      "data": [
        {
          "TOTAL_CUSTOMERS_OUTSTANDING": 3,
          "TOTAL_OUTSTANDING_AMOUNT": 29500000.00
        }
      ]
    },
    "get_raw_outstanding_details": {
      "status": "success",
      "data": [
        {
          "Customer Name": "PT ABC Corp",
          "Invoice Number": "INV-001",
          "Outstanding": 15000000.00
        },
        {
          "Customer Name": "CV XYZ",
          "Invoice Number": "INV-002",
          "Outstanding": 8500000.00
        },
        {
          "Customer Name": "PT DEF Industries",
          "Invoice Number": "INV-003",
          "Outstanding": 6000000.00
        }
      ]
    }
  }
}
```

#### **Response Payload (Error Sebagian atau Total)**

Jika salah satu atau semua operasi gagal, server akan tetap merespons dengan `success: true` di level atas, namun status di dalam setiap hasil operasi akan menunjukkan kegagalan.

```json
{
  "success": true,
  "results": {
    "get_summary_stats": {
      "status": "error",
      "error": "ORM Execution Failed: Unknown column 'arbook.PaymentValueLocal' in 'field list'"
    },
    "get_raw_outstanding_details": {
      "status": "success",
      "data": [
        // ... data yang berhasil diambil ...
      ]
    }
  }
}
```
*   **Jika seluruh panggilan gagal (misalnya, tidak bisa terhubung ke database):**
    ```json
    {
      "success": false,
      "error": "Gagal terhubung ke database MySQL: Connection refused."
    }
    ```

---

Kontrak ini memastikan bahwa `sim_testgeluran_server` menjadi komponen yang kuat dan terdefinisi dengan baik, yang mampu menangani logika eksekusi data yang kompleks sambil menjaga antarmuka yang sederhana dan aman dengan AI Agent.