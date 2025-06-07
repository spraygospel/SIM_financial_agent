# Detail Alur Kerja Setiap Node LangGraph

## Node 1: understand_query
**Fungsi**: Menganalisis dan memahami pertanyaan user dalam natural language

### Input State:
```
{
  "user_query": "Tunjukkan data sales bulan Januari 2023",
  "session_id": "user_123",
  "conversation_history": []
}
```

### Proses yang Terjadi:
1. **Intent Classification**: Identifikasi tujuan utama query
   - Sales analysis, customer report, employee data, etc.
2. **Entity Extraction**: Tangkap entitas penting
   - "sales" → business domain
   - "Januari 2023" → time period
3. **Metric Identification**: Tentukan metrics yang diminta
   - Total, count, average, trends, etc.
4. **Query Scope Analysis**: Pahami scope dan complexity

### Output State (Added):
```
{
  "intent": "sales_analysis",
  "entities_mentioned": ["sales", "monthly_data"],
  "time_period": {
    "start_date": "2023-01-01", 
    "end_date": "2023-01-31",
    "period_label": "Januari 2023"
  },
  "requested_metrics": ["total_sales", "transaction_count"],
  "query_complexity": "simple"
}
```

---

## Node 2: consult_schema
**Fungsi**: Berkonsultasi dengan Graphiti untuk mendapatkan schema knowledge

### Input dari Node Sebelumnya:
- Intent: "sales_analysis"
- Entities: ["sales", "monthly_data"]

### Proses yang Terjadi:
1. **Table Discovery**: Cari tabel yang relevan dengan intent
   ```
   Query ke Graphiti: "tabel yang berkaitan dengan sales analysis"
   ```
2. **Column Analysis**: Identifikasi kolom finansial dan temporal
3. **Relationship Mapping**: Dapatkan foreign key relationships
4. **Aggregation Planning**: Tentukan kolom mana yang bisa di-aggregate

### Konsultasi ke Graphiti:
```
Request: "Find tables related to sales analysis"
Response: [
  {
    "table_name": "sales_orders",
    "purpose": "transaction recording",
    "columns": {
      "order_date": "temporal",
      "total_amount": "financial_amount",
      "customer_id": "identifier"
    }
  },
  {
    "table_name": "order_lines", 
    "purpose": "transaction details",
    "relationship": "sales_orders.id = order_lines.order_id"
  }
]
```

### Output State (Added):
```
{
  "relevant_tables": ["sales_orders", "order_lines"],
  "table_relationships": [
    {
      "from": "sales_orders",
      "to": "order_lines", 
      "join_key": "order_id"
    }
  ],
  "financial_columns": {
    "sales_orders": ["total_amount"],
    "order_lines": ["unit_price", "quantity"]
  },
  "temporal_columns": {
    "sales_orders": ["order_date"]
  }
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