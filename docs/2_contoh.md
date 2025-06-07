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
  "intent": "customer_aging_analysis",
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
  "sql_queries": [
    {
      "purpose": "outstanding_details",
      "query": "SELECT c.customer_name, i.invoice_number...",
      "type": "detail_data"
    },
    {
      "purpose": "summary_statistics", 
      "query": "SELECT COUNT(DISTINCT c.customer_id)...",
      "type": "aggregate_data"
    }
  ],
  "response_template": "Template dengan placeholder di atas",
  "placeholder_mapping": {
    "TOTAL_CUSTOMERS_OUTSTANDING": "number",
    "TOTAL_OUTSTANDING_AMOUNT": "currency",
    "AVG_DAYS_OVERDUE": "number_with_decimal"
  }
}
```

---

## 🟦 Node 4: execute_query

### SQL Execution ke SQLite:
```python
# Execute Query 1: Detail Data
detail_results = [
  {
    "customer_name": "PT ABC Corp",
    "invoice_number": "INV-001", 
    "invoice_amount": 15000000,
    "paid_amount": 0,
    "outstanding": 15000000,
    "due_date": "2023-01-15",
    "days_overdue": 45
  },
  {
    "customer_name": "CV XYZ Trading",
    "invoice_number": "INV-002",
    "invoice_amount": 8500000, 
    "paid_amount": 0,
    "outstanding": 8500000,
    "due_date": "2023-01-20", 
    "days_overdue": 40
  },
  {
    "customer_name": "PT DEF Industries",
    "invoice_number": "INV-003",
    "invoice_amount": 12000000,
    "paid_amount": 6000000,
    "outstanding": 6000000,
    "due_date": "2023-01-25",
    "days_overdue": 35
  }
]

# Execute Query 2: Summary Stats  
summary_results = [
  {
    "total_customers_outstanding": 3,
    "total_outstanding_amount": 29500000,
    "avg_days_overdue": 40.0
  }
]
```

### State After Node 4:
```json
{
  // ... previous state ...
  "raw_query_results": [
    // detail_results array di atas
  ],
  "financial_calculations": {
    "TOTAL_CUSTOMERS_OUTSTANDING": 3,
    "TOTAL_OUTSTANDING_AMOUNT": 29500000,
    "AVG_DAYS_OVERDUE": 40.0,
    "TOP_RISK_CUSTOMER": "PT ABC Corp",
    "TOP_OUTSTANDING_AMOUNT": 15000000
  },
  "query_execution_status": "success"
}
```

---

## 🟦 Node 5: validate_results

### Validation Checks:
```python
validation_results = {
  "checks_performed": [
    {
      "check": "negative_outstanding",
      "result": "PASS",
      "message": "No negative outstanding amounts found"
    },
    {
      "check": "null_customer_names", 
      "result": "PASS",
      "message": "All customer names present"
    },
    {
      "check": "future_due_dates",
      "result": "PASS", 
      "message": "All due dates are in the past"
    },
    {
      "check": "reasonable_amounts",
      "result": "WARNING",
      "message": "1 invoice over Rp 10M detected (normal for enterprise)"
    }
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

### Number Formatting:
```python
formatted_values = {
  "TOTAL_CUSTOMERS_OUTSTANDING": "3",
  "TOTAL_OUTSTANDING_AMOUNT": "Rp 29.500.000",
  "AVG_DAYS_OVERDUE": "40",
  "TOP_RISK_CUSTOMER": "PT ABC Corp", 
  "TOP_OUTSTANDING_AMOUNT": "Rp 15.000.000",
  "COLLECTION_RECOMMENDATIONS": "Follow up prioritas untuk customer dengan outstanding > Rp 5M"
}
```

### Template Replacement:
```
Original: "Total Outstanding Amount: {TOTAL_OUTSTANDING_AMOUNT}"
Result:   "Total Outstanding Amount: Rp 29.500.000"
```

### Raw Data Table Formatting:
```python
formatted_table = [
  {
    "Customer Name": "PT ABC Corp",
    "Invoice": "INV-001",
    "Invoice Amount": "Rp 15.000.000",
    "Paid": "Rp 0", 
    "Outstanding": "Rp 15.000.000",
    "Due Date": "15 Jan 2023",
    "Days Overdue": "45 hari"
  },
  {
    "Customer Name": "CV XYZ Trading", 
    "Invoice": "INV-002",
    "Invoice Amount": "Rp 8.500.000",
    "Paid": "Rp 0",
    "Outstanding": "Rp 8.500.000", 
    "Due Date": "20 Jan 2023",
    "Days Overdue": "40 hari"
  },
  {
    "Customer Name": "PT DEF Industries",
    "Invoice": "INV-003", 
    "Invoice Amount": "Rp 12.000.000",
    "Paid": "Rp 6.000.000",
    "Outstanding": "Rp 6.000.000",
    "Due Date": "25 Jan 2023", 
    "Days Overdue": "35 hari"
  }
]
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