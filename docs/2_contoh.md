# Contoh Skenario Lengkap: "Customer Belum Bayar"

## User Input
**Query**: "Tunjukkan customer siapa saja yang belum lunas membayar beserta due date nya"

---

## 🟦 Node 1: understand_query

### Input State:
```json
{
  "user_query": "Tunjukkan customer siapa saja yang belum lunas membayar beserta due date nya",
  "session_id": "session_001"
}
```

### LLM Analysis Process:
```
Prompt ke LLM:
"Analyze this query and extract structured information:
Query: 'Tunjukkan customer siapa saja yang belum lunas membayar beserta due date nya'

Extract:
1. Intent (customer_aging, sales_analysis, etc.)
2. Entities mentioned
3. Required data points
4. Time sensitivity"

LLM Response:
{
  "intent": "customer_aging_analysis",
  "entities": ["customer", "payment_status", "due_date"],
  "required_data": ["customer_name", "outstanding_amount", "due_date", "overdue_days"],
  "time_sensitive": true,
  "complexity": "medium"
}
```

### State After Node 1:
```json
{
  "user_query": "Tunjukkan customer siapa saja yang belum lunas membayar beserta due date nya",
  "session_id": "session_001",
  "intent": "EXECUTE_QUERY",
  "entities_mentioned": ["customer", "payment_status", "due_date"],
  "requested_metrics": ["outstanding_amount", "days_overdue"],
  "query_complexity": "medium"
}
```

---

## 🟦 Node 2: consult_schema

### Graphiti Consultation:
```
Query 1 ke Graphiti: "tables related to customer payment tracking"
Response: [
  {
    "table_name": "customers",
    "purpose": "customer master data",
    "category": "operational",
    "key_columns": ["customer_id", "customer_name", "contact_info"]
  },
  {
    "table_name": "invoices", 
    "purpose": "billing tracking",
    "category": "financial",
    "key_columns": ["invoice_id", "customer_id", "invoice_amount", "due_date"]
  },
  {
    "table_name": "payments",
    "purpose": "payment recording", 
    "category": "financial",
    "key_columns": ["payment_id", "invoice_id", "payment_amount", "payment_date"]
  }
]

Query 2 ke Graphiti: "relationships between customers, invoices, payments"
Response: [
  {
    "from_table": "customers",
    "to_table": "invoices",
    "join_condition": "customers.customer_id = invoices.customer_id"
  },
  {
    "from_table": "invoices", 
    "to_table": "payments",
    "join_condition": "invoices.invoice_id = payments.invoice_id",
    "join_type": "LEFT JOIN"
  }
]
```

### State After Node 2:
```json
{
  // ... previous state ...
  "relevant_tables": ["customers", "invoices", "payments"],
  "table_relationships": [
    {
      "from": "customers",
      "to": "invoices",
      "join_key": "customer_id"
    },
    {
      "from": "invoices",
      "to": "payments", 
      "join_key": "invoice_id",
      "type": "LEFT_JOIN"
    }
  ],
  "financial_columns": {
    "invoices": ["invoice_amount"],
    "payments": ["payment_amount"]
  }
}
```

---

## 🟦 Node 3: plan_execution

### LLM Planning Process:
```
Prompt ke LLM:
"Create SQL execution plan for customer aging analysis.
Available tables: customers, invoices, payments
Relationships: customers → invoices → payments (LEFT JOIN)
Goal: Find customers with outstanding payments

Generate:
1. SQL queries for calculations
2. Response template with placeholders
3. Validation rules"

LLM Response: SQL Plan + Template
```

### Generated SQL Queries:
```sql
-- Query 1: Outstanding Amounts Calculation
SELECT 
  c.customer_name,
  i.invoice_number,
  i.invoice_amount,
  COALESCE(p.payment_amount, 0) as paid_amount,
  (i.invoice_amount - COALESCE(p.payment_amount, 0)) as outstanding,
  i.due_date,
  (CURRENT_DATE - i.due_date) as days_overdue
FROM customers c
JOIN invoices i ON c.customer_id = i.customer_id
LEFT JOIN payments p ON i.invoice_id = p.invoice_id
WHERE (i.invoice_amount - COALESCE(p.payment_amount, 0)) > 0
ORDER BY outstanding DESC;

-- Query 2: Summary Statistics
SELECT 
  COUNT(DISTINCT c.customer_id) as total_customers_outstanding,
  SUM(i.invoice_amount - COALESCE(p.payment_amount, 0)) as total_outstanding_amount,
  AVG(CURRENT_DATE - i.due_date) as avg_days_overdue
FROM customers c
JOIN invoices i ON c.customer_id = i.customer_id  
LEFT JOIN payments p ON i.invoice_id = p.invoice_id
WHERE (i.invoice_amount - COALESCE(p.payment_amount, 0)) > 0;
```

### Generated Response Template:
```
📊 **Customer Outstanding Report**

**Summary:**
- Total Customer dengan Outstanding: {TOTAL_CUSTOMERS_OUTSTANDING} customer
- Total Outstanding Amount: {TOTAL_OUTSTANDING_AMOUNT}  
- Rata-rata Days Overdue: {AVG_DAYS_OVERDUE} hari

**Analisis Risiko:**
Customer dengan risiko tertinggi adalah {TOP_RISK_CUSTOMER} dengan outstanding {TOP_OUTSTANDING_AMOUNT}.

**Rekomendasi:**
{COLLECTION_RECOMMENDATIONS}

**Detail terlampir dalam tabel di bawah.**
```

### State After Node 3:
```json
{
  // ... previous state ...
  "database_operations_plan": [
    {
      "operation_id": "get_summary_stats",
      "purpose": "Menghitung ringkasan data piutang customer",
      "main_table": "arbook",
      "select_columns": [
        {"field_name": "arbook.CustomerCode", "aggregation": "COUNT_DISTINCT", "alias": "TOTAL_CUSTOMERS_OUTSTANDING"},
        {"field_name": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "aggregation": "SUM", "alias": "TOTAL_OUTSTANDING_AMOUNT", "is_expression": true},
        {"field_name": "(CURRENT_DATE - arbook.DueDate)", "aggregation": "AVG", "alias": "AVG_DAYS_OVERDUE", "is_expression": true}
      ],
      "filters": {
        "logical_operator": "AND",
        "conditions": [{"field_or_expression": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "operator": ">", "value": 0, "is_expression": true}]
      },
      "result_key": "SUMMARY_STATS",
      "expected_result_format": "single_value"
    }
  ],
  "raw_data_operation_plan": {
      "operation_id": "get_raw_outstanding_details",
      "purpose": "Mengambil daftar detail piutang customer",
      "main_table": "arbook",
      "select_columns": [
          {"field_name": "mastercustomer.Name", "alias": "Customer Name"},
          {"field_name": "arbook.DocNo", "alias": "Invoice Number"},
          {"field_name": "arbook.DocValueLocal", "alias": "Invoice Amount"},
          {"field_name": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "alias": "Outstanding", "is_expression": true},
          {"field_name": "arbook.DueDate", "alias": "Due Date"}
      ],
      "joins": [
          {"target_table": "mastercustomer", "type": "INNER", "on_conditions": [{"left_table_field": "arbook.CustomerCode", "right_table_field": "mastercustomer.Code"}]}
      ],
      "filters": {
        "logical_operator": "AND",
        "conditions": [{"field_or_expression": "(arbook.DocValueLocal - arbook.PaymentValueLocal)", "operator": ">", "value": 0, "is_expression": true}]
      },
      "limit": 50,
      "result_key": "RAW_DATA_TABLE",
      "expected_result_format": "list_of_dicts"
  },
  "response_template": "Template dengan placeholder di atas",
  "placeholder_mapping": {
    "TOTAL_CUSTOMERS_OUTSTANDING": { "type": "number", "label": "Jumlah Customer Outstanding" },
    "TOTAL_OUTSTANDING_AMOUNT": { "type": "currency_IDR", "label": "Total Nilai Outstanding" },
    "AVG_DAYS_OVERDUE": { "type": "number", "precision": 0, "label": "Rata-rata Keterlambatan" }
  }
}
```

---

## 🟦 Node 4: execute_query

### MCP Server Call & Graphiti Storage:
1.  **Panggil MCP Server:** Node `execute_query` mengirimkan `database_operations_plan` dan `raw_data_operation_plan` ke `sim_testgeluran_server`.
2.  **Terima Hasil:** `sim_testgeluran_server` (yang menggunakan ORM) mengembalikan hasil dalam format JSON:
    *   `SUMMARY_STATS`: `{"TOTAL_CUSTOMERS_OUTSTANDING": 3, "TOTAL_OUTSTANDING_AMOUNT": 29500000, "AVG_DAYS_OVERDUE": 40.0}`
    *   `RAW_DATA_TABLE`: `[{"Customer Name": "PT ABC Corp", ...}, ...]` (3 baris data)
3.  **Simpan ke Graphiti:** Node `execute_query` mengambil hasil ini, lalu membuat **episode baru** di Graphiti dengan `group_id` sesi ini. Data tersebut disimpan di dalam episode.
4.  **Buat DataHandle:** Agent membuat "pointer" atau `DataHandle` untuk setiap data yang disimpan.

### State After Node 4:
`AgentState` sekarang berisi `DataHandle`, bukan data mentah.

```json
{
  // ... previous state ...
  "financial_calculations_handles": [
    {
      "data_handle_id": "ep-sum-001",
      "storage_location": "Graphiti",
      "group_id": "session_001",
      "data_description": "Menghitung ringkasan data piutang customer",
      "source_operation_id": "get_summary_stats",
      "row_count": 1
    }
  ],
  "raw_query_results_handle": {
    "data_handle_id": "ep-raw-001",
    "storage_location": "Graphiti",
    "group_id": "session_001",
    "data_description": "Mengambil daftar detail piutang customer",
    "source_operation_id": "get_raw_outstanding_details",
    "row_count": 3
  },
  "query_execution_status": "success"
}
---

## 🟦 Node 5: validate_results

### Data Retrieval and Validation Checks:
1.  **Baca `DataHandle`:** Node mengambil `financial_calculations_handles` dan `raw_query_results_handle` dari `AgentState`.
2.  **Query ke Graphiti:** Menggunakan `data_handle_id`, node ini mengambil data JSON yang sebenarnya dari Graphiti.
3.  **Lakukan Validasi:** Setelah mendapatkan data mentah, proses validasi berjalan seperti sebelumnya:
    *   Memeriksa apakah ada nilai `outstanding` yang negatif.
    *   Memastikan semua nama customer tidak kosong.
    *   Memverifikasi semua tanggal jatuh tempo (`DueDate`) valid.
    *   Memberi peringatan jika ada jumlah tagihan yang sangat besar.
4.  **Hasil Validasi:**
    ```python
    validation_results = {
      "checks_performed": [
        { "check": "negative_outstanding", "result": "PASS", "message": "..." },
        { "check": "null_customer_names", "result": "PASS", "message": "..." },
        { "check": "future_due_dates", "result": "PASS", "message": "..." },
        { "check": "reasonable_amounts", "result": "WARNING", "message": "..." }
      ],
      "quality_score": 95,
      "critical_issues": 0,
      "warnings": 1
    }
    ```

### Decision: CONTINUE (no critical issues)

### State After Node 5:
```json
{
  // ... previous state ...
  "data_quality_checks": {
    "negative_values_found": false,
    "null_values_count": 0,
    "reasonable_amounts": true,
    "dates_valid": true
  },
  "validation_warnings": [
    "ℹ️ Note: 1 invoice over Rp 10M detected (normal for enterprise customers)"
  ],
  "validation_status": "passed_with_notes",
  "quality_score": 95
}
```

---

## 🟦 Node 6: replace_placeholders

### Data Retrieval from Graphiti:
1.  **Baca `DataHandle`:** Node mengambil `financial_calculations_handles` dan `raw_query_results_handle` dari `AgentState`.
2.  **Query ke Graphiti:** Menggunakan `data_handle_id` dari setiap handle, node ini melakukan query ke Graphiti untuk mengambil data JSON yang sebenarnya yang disimpan di Langkah 4.
    *   Hasilnya adalah data yang sama seperti yang diterima dari MCP server sebelumnya.

### Number Formatting & Template Replacement:
Proses pemformatan angka dan penggantian placeholder pada template narasi berjalan seperti sebelumnya, namun menggunakan data yang baru saja diambil dari Graphiti.

### Raw Data Table Formatting:
Proses pemformatan tabel juga berjalan seperti sebelumnya, menggunakan data mentah yang diambil dari Graphiti.
```

---

## 🎯 Final Output ke User

### 📊 Raw Data Table:
| Customer Name | Invoice | Invoice Amount | Paid | Outstanding | Due Date | Days Overdue |
|---------------|---------|----------------|------|-------------|----------|--------------|
| PT ABC Corp | INV-001 | Rp 15.000.000 | Rp 0 | Rp 15.000.000 | 15 Jan 2023 | 45 hari |
| CV XYZ Trading | INV-002 | Rp 8.500.000 | Rp 0 | Rp 8.500.000 | 20 Jan 2023 | 40 hari |
| PT DEF Industries | INV-003 | Rp 12.000.000 | Rp 6.000.000 | Rp 6.000.000 | 25 Jan 2023 | 35 hari |

### 📈 Executive Summary & Analysis:
```
📊 Customer Outstanding Report

Summary:
- Total Customer dengan Outstanding: 3 customer
- Total Outstanding Amount: Rp 29.500.000  
- Rata-rata Days Overdue: 40 hari

Analisis Risiko:
Customer dengan risiko tertinggi adalah PT ABC Corp dengan outstanding Rp 15.000.000.

Rekomendasi:
Follow up prioritas untuk customer dengan outstanding > Rp 5M

Detail terlampir dalam tabel di atas.
```

### ⚠️ Data Quality Notes:
```
✅ Data Quality Score: 95/100
ℹ️ Note: 1 invoice over Rp 10M detected (normal for enterprise customers)
✅ All validations passed
📅 Report generated: 1 Mar 2023, 14:30 WIB
```

---

## Workflow Summary

**Total Processing Time**: ~3-5 detik
**Nodes Executed**: 6/6 successful  
**SQL Queries**: 2 executed
**Records Processed**: 3 outstanding invoices
**Validation Score**: 95/100

**Key Benefits Demonstrated**:
✅ LLM never saw actual numbers (placeholder strategy worked)
✅ All calculations done via SQL aggregations  
✅ Raw data visible for user verification
✅ Comprehensive validation warnings provided
✅ Professional business-ready output format

Alur kerja ini menunjukkan bagaimana agent dapat memproses query kompleks dengan aman, akurat, dan transparent.