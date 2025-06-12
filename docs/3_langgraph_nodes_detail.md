# Detail Alur Kerja Setiap Node LangGraph

## **Node 1: `Router` (Sebelumnya `understand_query`)**

**Fungsi:** Bertindak sebagai "otak" awal atau "pintu gerbang" dari alur kerja. Tugasnya adalah menganalisis pesan baru dari pengguna dalam konteks percakapan yang sedang berlangsung, lalu **menentukan `intent` (maksud) utama** dari pesan tersebut. `Intent` inilah yang akan menentukan alur kerja (jalur) mana yang akan diambil oleh agent selanjutnya.

---

### **Input State:**

Node ini menerima `AgentState` awal, yang berisi:
```json
{
  "user_query": "Coba filter untuk Jakarta saja.",
  "session_id": "user_123_session_002",
  "conversation_history": [
    {
      "role": "user",
      "content": "Tampilkan customer yang belum lunas."
    },
    {
      "role": "assistant",
      "content": "Ditemukan 5 customer yang belum lunas..."
    }
  ],
  "raw_query_results_handle": {
      "data_handle_id": "ep-xyz-789",
      "storage_location": "Graphiti",
      "group_id": "user_123_session_002",
      "data_description": "Daftar customer belum lunas",
      "row_count": 5,
      "column_schema": [
        {"name": "customer_name", "type": "string"},
        {"name": "outstanding_amount", "type": "decimal"}
      ],
      "created_at": "2024-10-27T10:00:00Z"
  }
}
```

### **Proses yang Terjadi:**

1.  **Analisis Kontekstual:** Node mengirimkan pesan terbaru pengguna **BESERTA** riwayat percakapan (`conversation_history`) ke LLM. Konteks ini sangat penting. LLM melihat bahwa pesan "Coba filter untuk Jakarta saja." datang setelah agent memberikan laporan piutang.

2.  **Klasifikasi Intent:** LLM menganalisis dan memilih `intent` yang paling sesuai dari daftar yang telah ditentukan. Dalam contoh di atas, LLM akan menyimpulkan bahwa ini bukan permintaan query baru, melainkan permintaan untuk memodifikasi hasil sebelumnya.
    *   **Intent yang Mungkin Dipilih:**
        *   `EXECUTE_QUERY`: Untuk permintaan data yang benar-benar baru.
        *   `REQUEST_MODIFICATION_OR_FILTER`: Untuk permintaan menyaring, mengurutkan, atau mengubah hasil yang ada.
        *   `ACKNOWLEDGE_RESPONSE`: Untuk basa-basi seperti "terima kasih".
        *   `UNKNOWN_OR_AMBIGUOUS`: Jika permintaan tidak jelas.

3.  **Ekstraksi Entitas (Jika Perlu):** Jika `intent`-nya adalah `EXECUTE_QUERY` atau `REQUEST_MODIFICATION`, LLM juga akan mengekstrak entitas-entitas penting dari pesan.
    *   Untuk `intent: REQUEST_MODIFICATION`, ia akan mengekstrak: `{ "filter_type": "location", "filter_value": "Jakarta" }`.
    *   Untuk `intent: EXECUTE_QUERY`, ia akan mengekstrak entitas seperti pada versi lama (metrik, periode waktu, dll.).

### **Output State (Added/Modified):**

Node ini akan menambahkan field-field berikut ke dalam `AgentState`:
```json
{
  "intent": "REQUEST_MODIFICATION_OR_FILTER",
  "modification_details": {
    "type": "FILTER",
    "conditions": [
      {
        "field_or_expression": "mastercustomer.City",
        "operator": "=",
        "value": "Jakarta"
      }
    ]
  },
  "current_node_name": "Router"
}
```
*Catatan: Struktur `modification_details` bisa bervariasi tergantung pada jenis modifikasi (filter, sort, dll.) dan akan digunakan oleh `plan_execution_node` untuk merevisi rencana.*

### **Logika Selanjutnya (Conditional Edge):**

Setelah node `Router` selesai, `StateGraph` akan memeriksa field `intent` untuk menentukan langkah berikutnya:
*   Jika `intent` == `EXECUTE_QUERY`, lanjut ke `consult_schema`.
*   Jika `intent` == `REQUEST_MODIFICATION_OR_FILTER`, lanjut ke `plan_execution` (dalam mode revisi).
*   Jika `intent` == `ACKNOWLEDGE_RESPONSE`, lanjut ke `generate_acknowledgement`.
*   Jika `intent` == `UNKNOWN_OR_AMBIGUOUS`, lanjut ke `generate_error_response`.

---

## **Node 2: `consult_schema`**

**Fungsi:** Bertindak sebagai **MCP Client** untuk `graphiti_server`. Tugasnya adalah mendapatkan "peta data" (informasi skema yang relevan) yang akan digunakan oleh `plan_execution_node` untuk membuat rencana query. Node ini hanya dijalankan jika `intent` dari `Router` adalah `EXECUTE_QUERY`.

---

### **Input dari Node Sebelumnya:**
- `intent: "EXECUTE_QUERY"`
- `entities_mentioned: ["sales", "monthly_data"]`

### **Proses yang Terjadi:**

1.  **Mempersiapkan Panggilan Tool:** Node ini tidak lagi melakukan query Cypher secara langsung. Sebaliknya, ia mempersiapkan panggilan ke *tool* yang disediakan oleh `graphiti_server`.
    *   **Nama Tool:** `get_relevant_schema`
    *   **Payload Request:** `{ "intent": "EXECUTE_QUERY", "entities": ["sales", "monthly_data"] }`

2.  **Memanggil `graphiti_server` (MCP Interaction):**
    *   Node ini membuat koneksi HTTP ke `graphiti_server`.
    *   Ia mengirim `payload` di atas ke endpoint *tool* `get_relevant_schema`.
    *   Proses ini dicatat dalam `mcp_tool_call_history` di `AgentState`.

3.  **Menerima Respons Skema:**
    *   `graphiti_server` merespons dengan sebuah objek JSON yang berisi daftar tabel, kolom, dan relasi yang relevan.
    *   Respons ini sudah bersih dan terstruktur, siap untuk digunakan.

### **Output State (Added):**

Node ini menerima respons dari `graphiti_server` dan menyimpannya ke `AgentState`:
```json
{
  "relevant_tables": [
    {
      "table_name": "sales_orders",
      "purpose": "transaction recording",
      "columns": [
        {"name": "order_date", "classification": "temporal"},
        {"name": "total_amount", "classification": "financial_amount"}
      ]
    }
  ],
  "table_relationships": [
    {
      "from_table": "order_lines",
      "to_table": "sales_orders",
      "join_key": "order_id"
    }
  ],
  "financial_columns": {
    "sales_orders": ["total_amount"]
  },
  "current_node_name": "consult_schema"
}
```

---

## **Node 3: `execute_query`** (Nama node mungkin akan kita ubah nanti, misal `delegate_execution`)

**Fungsi:** Bertindak sebagai **MCP Client** untuk `sim_testgeluran_server`. Tugasnya adalah **mendelegasikan** eksekusi `DatabaseOperationPlan` yang telah dibuat dan divalidasi, lalu menerima hasilnya. Ia tidak lagi tahu-menahu tentang SQL, ORM, atau koneksi database.

---

### **Input dari Node Sebelumnya:**

- `database_operations_plan: [ ... ]` (Sebuah list dari rencana operasi JSON)
- `raw_data_operation_plan: { ... }` (Satu rencana operasi JSON untuk data mentah)

### **Proses yang Terjadi:**

1.  **Mempersiapkan Panggilan Tool:** Node ini mengambil `DatabaseOperationPlan` dari `AgentState`.
    *   **Nama Tool:** `execute_operation_plan`
    *   **Payload Request:** Seluruh objek `database_operations_plan` dan `raw_data_operation_plan` dibungkus dalam satu request JSON. Contoh:
        ```json
        {
          "operations": [
            { "operation_id": "get_total_sales", ... },
            { "operation_id": "get_transaction_count", ... }
          ],
          "raw_data_operation": { "operation_id": "fetch_raw_table", ... }
        }
        ```

2.  **Memanggil `sim_testgeluran_server` (MCP Interaction):**
    *   Node membuat koneksi HTTP ke `sim_testgeluran_server`.
    *   Ia mengirim `payload` di atas ke endpoint *tool* `execute_operation_plan`.
    *   Proses ini dicatat dalam `mcp_tool_call_history`.

3.  **Menerima Hasil dari Server:**
    *   `sim_testgeluran_server` (yang menggunakan ORM di dalamnya) akan mengeksekusi setiap operasi dan mengembalikan hasilnya dalam satu respons JSON.
    *   Contoh Respons:
        ```json
        {
          "results": {
            "get_total_sales": { "status": "success", "data": 125000000 },
            "get_transaction_count": { "status": "success", "data": 456 }
          },
          "raw_data_result": {
            "status": "success",
            "data": [
              { "order_id": "ORD-001", "total_amount": 150000 },
              ...
            ]
          }
        }
        ```

4.  **Menyimpan Hasil ke Graphiti (Membuat `DataHandle`):**
    *   **PENTING:** Node ini **tidak** menyimpan data mentah di `AgentState`.
    *   Untuk setiap hasil yang diterima (baik kalkulasi maupun data mentah), node ini akan:
        a. Membuat `Episode` baru di Graphiti (via `graphiti_server`) dengan `group_id = session_id`.
        b. Menyimpan data hasil query ke dalam episode tersebut.
        c. Membuat objek **`DataHandle`** (pointer ke data di Graphiti).

### **Output State (Added/Modified):**

Node ini menyimpan **handle**, bukan data mentah, ke `AgentState`:
```json
{
  "financial_calculations_handles": [
    {
      "data_handle_id": "ep-calc-001",
      "data_description": "Total Sales Jan 2023",
      "source_operation_id": "get_total_sales",
      "row_count": 1,
      ...
    },
    {
      "data_handle_id": "ep-calc-002",
      "data_description": "Transaction Count Jan 2023",
      "source_operation_id": "get_transaction_count",
      "row_count": 1,
      ...
    }
  ],
  "raw_query_results_handle": {
    "data_handle_id": "ep-raw-001",
    "data_description": "Raw Sales Data for Jan 2023",
    "source_operation_id": "fetch_raw_table",
    "row_count": 456,
    ...
  },
  "query_execution_status": "success",
  "current_node_name": "execute_query"
}
```
---

## Node 3: plan_execution
**Fungsi**: Membuat rencana eksekusi SQL dan template response dengan placeholder

### Input dari Node Sebelumnya:
- Schema knowledge dari Graphiti
- User intent dan entities

### Proses yang Terjadi:
1. **SQL Query Planning**: Buat query SQL yang aman dan efisien
2. **Template Generation**: Buat response template dengan placeholder
3. **Validation Rules**: Tentukan aturan validasi untuk results
4. **Placeholder Mapping**: Map placeholder ke SQL calculations

### Contoh SQL Plan:
```sql
-- Query 1: Total Sales
SELECT SUM(total_amount) as total_sales_jan_2023
FROM sales_orders 
WHERE order_date >= '2023-01-01' 
AND order_date <= '2023-01-31'

-- Query 2: Transaction Count
SELECT COUNT(*) as count_orders_jan_2023
FROM sales_orders 
WHERE order_date >= '2023-01-01' 
AND order_date <= '2023-01-31'

-- Query 3: Raw Data for Table
SELECT order_id, customer_id, order_date, total_amount
FROM sales_orders 
WHERE order_date >= '2023-01-01' 
AND order_date <= '2023-01-31'
ORDER BY order_date DESC
```

### Template Response (dengan Placeholder):
```
Laporan Penjualan Januari 2023:

📊 Ringkasan Performa:
- Total Penjualan: {TOTAL_SALES_JAN_2023}
- Jumlah Transaksi: {COUNT_ORDERS_JAN_2023} 
- Rata-rata per Transaksi: {AVG_ORDER_VALUE_JAN_2023}

📈 Analisis:
Performa penjualan bulan Januari menunjukkan {PERFORMANCE_TREND}. 
Target bulanan tercapai {ACHIEVEMENT_PERCENTAGE} dari rencana.
```

### Output State (Added):
```
{
  "sql_queries": [
    {
      "purpose": "total_sales_calculation",
      "query": "SELECT SUM(total_amount) as result FROM sales_orders WHERE...",
      "result_key": "TOTAL_SALES_JAN_2023"
    },
    {
      "purpose": "transaction_count", 
      "query": "SELECT COUNT(*) as result FROM sales_orders WHERE...",
      "result_key": "COUNT_ORDERS_JAN_2023"
    }
  ],
  "response_template": "Template dengan placeholder di atas",
  "placeholder_mapping": {
    "TOTAL_SALES_JAN_2023": "format_currency",
    "COUNT_ORDERS_JAN_2023": "format_number"
  },
  "raw_data_query": "SELECT order_id, customer_id... (untuk tabel)"
}
```

---










## **Node 3.5: `validate_plan_node`**

**Fungsi:** Bertindak sebagai **"Quality Gate"** atau pos pemeriksaan untuk `DatabaseOperationPlan` yang dihasilkan oleh `plan_execution_node`. Tujuannya adalah untuk menangkap kesalahan perencanaan **sebelum** dikirim ke `sim_testgeluran_server`, mencegah eksekusi yang pasti gagal dan memungkinkan adanya "repair loop" (perbaikan mandiri).

---

### **Input dari Node Sebelumnya:**

- `database_operations_plan: [ ... ]`
- `raw_data_operation_plan: { ... }`
- `relevant_tables: [ ... ]` (Skema yang digunakan untuk perencanaan)
- `table_relationships: [ ... ]`

### **Proses yang Terjadi:**

Node ini melakukan serangkaian pemeriksaan logis terhadap setiap `DatabaseOperation` dalam rencana, **tanpa** memanggil layanan eksternal.

1.  **Validasi Struktur (Syntactic Validation):**
    *   Memastikan setiap operasi memiliki field wajib seperti `operation_id`, `main_table`, `select_columns`, dan `result_key`.
    *   Memeriksa tipe data: apakah `select_columns` berupa list? Apakah `limit` berupa integer?

2.  **Validasi Skema (Semantic Validation):**
    *   **Pemeriksaan Tabel:** Apakah `main_table` dan semua tabel di dalam `joins` ada di dalam daftar `relevant_tables` yang tersedia?
    *   **Pemeriksaan Kolom:** Untuk setiap kolom yang disebutkan di `select_columns`, `filters`, `joins`, dll., apakah kolom tersebut benar-benar ada di tabel yang bersangkutan sesuai `relevant_tables`?
    *   **Pemeriksaan Agregasi:** Apakah fungsi agregasi (misalnya, `SUM`) diterapkan pada kolom yang ditandai `is_aggregatable: true` dalam metadata skema?

3.  **Validasi Logika Sederhana:**
    *   **Konsistensi `GROUP BY`:** Jika ada fungsi agregasi di `select_columns`, apakah semua kolom non-agregasi lainnya sudah dimasukkan ke dalam `group_by_columns`?
    *   **Kondisi `HAVING`:** Apakah klausa `having_conditions` hanya digunakan jika ada `group_by_columns`?

### **Decision Logic (Conditional Edge):**

Berdasarkan hasil validasi, node ini akan menentukan alur selanjutnya:

*   **Jika semua operasi dalam rencana valid (`status: 'valid'`)**:
    *   **Arahkan ke:** `execute_query`
    *   `AgentState` tidak perlu diubah secara signifikan, mungkin hanya menambahkan `plan_validation_status: 'success'`.

*   **Jika ada satu atau lebih operasi yang tidak valid (`status: 'invalid'`)**:
    *   **Arahkan kembali ke:** `plan_execution` (dengan **mode perbaikan**).
    *   `AgentState` akan diperbarui dengan pesan error yang spesifik untuk membantu LLM melakukan perbaikan.
        ```json
        {
          "plan_validation_status": "failed",
          "plan_validation_errors": [
            {
              "operation_id": "get_total_sales",
              "error": "Kolom 'total_amount' tidak ditemukan di tabel 'customers'. Kolom tersebut ada di tabel 'sales_orders'."
            }
          ],
          "is_repair_loop": true
        }
        ```
    *   Jika "repair loop" gagal setelah beberapa kali (misalnya, 2 kali), alur akan diarahkan ke `generate_error_response`.

### **Output State (Added/Modified):**

Node ini tidak menghasilkan data baru, tetapi memperbarui status dan menambahkan detail error jika diperlukan.
```json
{
  "plan_validation_status": "success", // atau 'failed'
  "plan_validation_errors": [], // atau diisi dengan pesan error
  "current_node_name": "validate_plan"
}
```

Dengan adanya `validate_plan_node`, kita secara signifikan mengurangi risiko mengirimkan rencana yang cacat ke MCP server, membuat keseluruhan sistem lebih tangguh dan andal.


## Node 4: execute_query
**Fungsi**: Eksekusi SQL queries ke SQLite in-memory database

### Input dari Node Sebelumnya:
- SQL queries yang sudah direncanakan
- Placeholder mapping

### Proses yang Terjadi:
1. **SQL Execution**: Jalankan semua planned queries
2. **Result Collection**: Kumpulkan hasil aggregate calculations
3. **Raw Data Retrieval**: Ambil data mentah untuk display table
4. **Error Handling**: Handle query failures gracefully

### Eksekusi ke SQLite:
```python
# Execute aggregate queries
results = {}
for query_plan in sql_queries:
    result = execute_sql(query_plan["query"])
    results[query_plan["result_key"]] = result[0]["result"]

# Execute raw data query
raw_data = execute_sql(raw_data_query)
```

### Output State (Added):
```
{
  "financial_calculations": {
    "TOTAL_SALES_JAN_2023": 125000000.50,
    "COUNT_ORDERS_JAN_2023": 456,
    "AVG_ORDER_VALUE_JAN_2023": 274122.81
  },
  "raw_query_results": [
    {
      "order_id": "ORD-001",
      "customer_id": "CUST-123", 
      "order_date": "2023-01-15",
      "total_amount": 150000
    },
    // ... 455 records lainnya
  ],
  "query_execution_status": "success",
  "rows_processed": 456
}
```

---

## Node 5: validate_results
**Fungsi**: Validasi kualitas data dan consistency checks

### Input dari Node Sebelumnya:
- Financial calculations
- Raw query results

### Proses yang Terjadi:
1. **Data Quality Checks**: Validasi nilai-nilai yang masuk akal
2. **Consistency Validation**: Cross-check antar calculations
3. **Business Logic Validation**: Aturan bisnis spesifik
4. **Warning Generation**: Generate warnings untuk anomalies

### Validation Rules:
```python
# Check for negative sales (should be rare)
if financial_calculations["TOTAL_SALES_JAN_2023"] < 0:
    warnings.append("Warning: Negative total sales detected")

# Check for zero counts
if financial_calculations["COUNT_ORDERS_JAN_2023"] == 0:
    warnings.append("No transactions found for the period")

# Validate average calculation
calculated_avg = total_sales / count_orders
if abs(calculated_avg - stored_avg) > 0.01:
    warnings.append("Average calculation inconsistency detected")

# Check for missing dates in raw data
missing_dates = check_date_gaps(raw_query_results)
if missing_dates:
    warnings.append(f"Data gaps detected: {missing_dates}")
```

### Decision Logic:
```
IF critical_errors > 0:
    → Route to ERROR node
ELSE IF warnings > 0:
    → Continue to next node (with warnings)
ELSE:
    → Continue to next node (clean data)
```

### Output State (Added):
```
{
  "data_quality_checks": {
    "negative_values_found": false,
    "null_values_count": 0,
    "date_range_valid": true,
    "calculations_consistent": true
  },
  "validation_warnings": [
    "Note: 3 small transactions under Rp 10,000 detected",
    "Info: Data complete for entire January period"
  ],
  "validation_status": "passed_with_notes",
  "quality_score": 95
}
```

---

## Node 6: replace_placeholders
**Fungsi**: Replace placeholder dengan nilai aktual dan format final output

### Input dari Node Sebelumnya:
- Response template dengan placeholder
- Financial calculations
- Raw data untuk table
- Validation warnings

### Proses yang Terjadi:
1. **Number Formatting**: Format angka sesuai locale Indonesia
2. **Placeholder Replacement**: Ganti semua placeholder dengan nilai aktual
3. **Table Preparation**: Siapkan raw data untuk display table
4. **Final Assembly**: Gabungkan narasi + table + warnings

### Placeholder Replacement Process:
```python
# Format financial numbers
formatted_numbers = {
    "TOTAL_SALES_JAN_2023": "Rp 125.000.000",
    "COUNT_ORDERS_JAN_2023": "456 transaksi", 
    "AVG_ORDER_VALUE_JAN_2023": "Rp 274.123"
}

# Replace in template
final_narrative = response_template
for placeholder, value in formatted_numbers.items():
    final_narrative = final_narrative.replace(f"{{{placeholder}}}", value)
```

### Output State (Final):
```
{
  "final_narrative": "Laporan Penjualan Januari 2023:\n\n📊 Ringkasan Performa:\n- Total Penjualan: Rp 125.000.000\n- Jumlah Transaksi: 456 transaksi...",
  
  "data_table_for_display": [
    {
      "Order ID": "ORD-001",
      "Customer": "CUST-123",
      "Date": "15 Jan 2023", 
      "Amount": "Rp 150.000"
    },
    // ... formatted table data
  ],
  
  "executive_summary": {
    "total_sales": "Rp 125.000.000",
    "transaction_count": "456",
    "period": "Januari 2023",
    "quality_score": 95
  },
  
  "warnings_for_display": [
    "ℹ️ Note: 3 small transactions under Rp 10,000 detected",
    "✅ Info: Data complete for entire January period"
  ]
}
```

---

## **Node 7: `generate_acknowledgement_node`**

**Fungsi:** Menangani `intent: 'ACKNOWLEDGE_RESPONSE'`. Node ini berada di **jalur pintas (shortcut path)** yang dirancang khusus untuk merespons interaksi sosial sederhana dari pengguna, seperti ucapan terima kasih atau konfirmasi. Tujuannya adalah untuk memberikan respons yang cepat dan relevan secara kontekstual tanpa perlu memicu alur kerja query yang berat.

---

### **Input dari Node Sebelumnya (`Router`):**
- `intent: "ACKNOWLEDGE_RESPONSE"`
- `user_query: "Oke, terima kasih banyak!"`
- `conversation_history: [ ... ]` (Sangat penting untuk konteks)

### **Proses yang Terjadi:**

1.  **Analisis Konteks Sederhana:** Node ini akan melihat pesan terakhir dalam `conversation_history` yang dikirim oleh **agent**. Ini memberikan konteks untuk respons yang akan diberikan.

2.  **Pemanggilan LLM untuk Respons Singkat:** Node memanggil LLM dengan prompt yang sangat terfokus dan ringan.
    *   **Contoh Prompt:**
        ```
        Anda adalah asisten AI yang ramah. Pengguna baru saja mengatakan: '{user_query}'.
        Pesan terakhir yang Anda kirimkan adalah: '{last_assistant_message}'.
        
        Berdasarkan konteks ini, berikan satu kalimat respons yang singkat, sopan, dan terdengar alami. Jangan menawarkan bantuan lebih lanjut kecuali jika relevan.

        Contoh:
        - Jika pesan Anda sebelumnya adalah laporan: "Sama-sama! Senang laporannya bisa membantu."
        - Jika pesan Anda sebelumnya adalah permintaan klarifikasi: "Baik, saya mengerti."
        - Jika pengguna hanya bilang "Oke": Cukup balas dengan "Baik."
        ```

3.  **Menghasilkan Output Final:** LLM akan mengembalikan respons singkat (misalnya, "Sama-sama! Senang bisa membantu."). Node ini akan langsung menempatkan teks ini ke dalam field `final_narrative` di `AgentState`. Tidak ada `DataHandle`, `financial_calculations`, atau `raw_query_results` yang dibuat.

### **Output State (Final untuk alur ini):**

Node ini menghasilkan state yang siap untuk ditampilkan dan kemudian diarahkan ke `log_analytics_node`.
```json
{
  "final_narrative": "Sama-sama! Senang jika laporannya bisa membantu.",
  
  // Field-field lain ini akan kosong atau tidak ada
  "data_table_for_display": [],
  "executive_summary": [],
  "warnings_for_display": [],
  
  "current_node_name": "generate_acknowledgement",
  "workflow_status": "completed" 
}
```

### **Logika Selanjutnya:**

Setelah `generate_acknowledgement_node` selesai, alur kerja akan langsung diarahkan ke **`log_analytics_node`** dan kemudian ke **`END`**. Ini memastikan alur respons sosial sangat cepat dan efisien.

---

## **Node 8: `log_analytics_node`**

**Fungsi:** Bertindak sebagai **"Collector" atau "Pencatat Telemetri"** di akhir setiap siklus alur kerja. Node ini tidak mengubah respons yang akan dilihat pengguna. Tugasnya murni untuk mengumpulkan data-data penting dari `AgentState` setelah sebuah interaksi selesai (baik sukses maupun gagal), memformatnya menjadi log analitik terstruktur, dan menyimpannya untuk analisis di kemudian hari.

---

### **Input dari Node Sebelumnya:**

Node ini adalah titik temu dari beberapa alur, jadi ia bisa menerima `AgentState` dari:
- `replace_placeholders_node` (jika alur query sukses).
- `generate_acknowledgement_node` (jika alur basa-basi sukses).
- `generate_error_response_node` (jika terjadi error di mana pun).

`AgentState` akan berisi semua informasi yang relevan dari alur yang baru saja selesai.

### **Proses yang Terjadi:**

1.  **Ekstraksi Data dari `AgentState`:** Node ini akan membaca dan mengekstrak berbagai metrik dari `AgentState` akhir, seperti:
    *   `session_id`, `user_query`, `detected_intent`.
    *   `workflow_status` ('completed' atau 'error').
    *   Durasi total, durasi per komponen (jika kita melacaknya).
    *   `final_quality_score` (jika ada).
    *   `tables_used` dari `data_source_info` (jika ada).
    *   Informasi error (`error_node`, `error_details`) jika alur gagal.
    *   Apakah `fallback` atau `repair loop` digunakan.

2.  **Pembuatan `AnalyticsLogEntry`:** Data yang diekstrak akan diformat menjadi sebuah objek JSON terstruktur (sesuai skema `AnalyticsLogEntry` yang kita rencanakan).
    *   **Contoh Objek Log:**
        ```json
        {
          "log_id": "log-uuid-12345",
          "session_id": "user_123_session_002",
          "event_timestamp": "2024-10-27T10:00:15Z",
          "user_query": "Tampilkan customer yang belum lunas.",
          "detected_intent": "EXECUTE_QUERY",
          "workflow_status": "completed",
          "final_quality_score": 95,
          "total_duration_ms": 4250,
          "llm_planning_duration_ms": 1800,
          "db_execution_duration_ms": 950,
          "tables_used": ["arbook", "mastercustomer", "customerpaymentd"],
          "error_node": null,
          "error_details": null,
          "was_fallback_used": false
        }
        ```

3.  **Penyimpanan Log:**
    *   Untuk MVP, node ini akan melakukan tindakan penyimpanan yang sederhana, misalnya:
        *   Menulis objek JSON `AnalyticsLogEntry` sebagai satu baris baru ke dalam file `logs/analytics.log`.
        *   Atau, mencetaknya ke konsol (`stdout` atau `stderr`) dengan prefix `[ANALYTICS]`.
    *   Di masa depan, langkah ini bisa diganti dengan mengirimkan log ke ElasticSearch, Datadog, atau database analitik lainnya.

### **Output State:**

Node ini **tidak memodifikasi `AgentState`** yang akan dikembalikan ke pengguna. Ia hanya membaca state dan melakukan aksi "fire and forget" (menulis log). Setelah node ini selesai, alur kerja akan langsung berakhir.

### **Logika Selanjutnya:**

Setelah `log_analytics_node` selesai, alur kerja langsung diarahkan ke **`END`**. Ini adalah titik akhir absolut dari semua percabangan alur kerja.

---

Dengan adanya node ini, kita memastikan bahwa setiap interaksi, baik sukses maupun gagal, akan meninggalkan jejak data yang berharga, memungkinkan kita untuk memantau, menganalisis, dan meningkatkan performa agent secara berkelanjutan.

## Error Handling Flow

### ERROR Node: generate_error_response
**Triggered when**: Critical validation failures or query execution errors

### Error Scenarios:
1. **SQL Query Failed**: Syntax error, table not found, etc.
2. **Data Corruption**: Negative sales, impossible dates, etc.
3. **No Data Found**: Query returns empty results
4. **Schema Mismatch**: Expected columns not found

### Error Response Format:
```
{
  "success": false,
  "error_type": "query_execution_failed",
  "user_message": "Maaf, terjadi kesalahan saat mengambil data penjualan. Silakan periksa format tanggal dan coba lagi.",
  "technical_details": "Table 'sales_orders' not found in database",
  "suggestions": [
    "Periksa apakah data sudah di-load dengan benar",
    "Coba query dengan periode yang berbeda"
  ]
}
```

---

## State Persistence & Recovery

### Checkpointing Strategy:
- Setiap node completion disimpan sebagai checkpoint
- Jika agent crash, bisa resume dari last successful node
- User bisa "rollback" ke node sebelumnya jika tidak puas

### State Evolution Timeline:
```
START → [user_query] 
  → understand_query → [+ intent, entities]
  → consult_schema → [+ tables, columns]  
  → plan_execution → [+ sql_queries, template]
  → execute_query → [+ results, calculations]
  → validate_results → [+ warnings, quality_checks]
  → replace_placeholders → [+ final_output]
END
```

Visualisasi ini menunjukkan bagaimana agent memproses query user step-by-step, dengan setiap node memiliki tanggung jawab spesifik dan state transformation yang jelas.

---


