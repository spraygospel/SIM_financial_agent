# Rancangan MVP AI Agent untuk Query SQL Source File

## 1. Konsep Dasar & Tujuan MVP

### Tujuan Utama
Membangun AI agent yang dapat memahami pertanyaan bisnis dalam bahasa natural dan menghasilkan laporan finansial akurat dari SQL source file. Agent harus dapat menampilkan data mentah dalam tabel dan memberikan analisis naratif yang dapat dipercaya.

### Prinsip Desain MVP
- **Fokus Fungsionalitas**: Prioritas pada akurasi data dan kemampuan query, bukan keamanan
- **Zero Manual Calculation by LLM**: LLM dilarang keras melakukan perhitungan angka
- **Transparency First**: Semua data mentah ditampilkan untuk verifikasi user
- **Placeholder Strategy**: LLM bekerja dengan template, angka diisi oleh system

## 2. Arsitektur Sistem

### Stack Teknologi
- **LangGraph**: Framework untuk state management dan workflow orchestration
- **Graphiti**: Knowledge graph untuk menyimpan metadata schema database
- **SQLite In-Memory**: Runtime database untuk execute query dari SQL source file
- **FastAPI**: Backend API server
- **React.js**: Frontend interface untuk display tabel dan narasi
- **Pandas**: Data manipulation dan analysis

### Komponen Utama
1. **SQL File Processor**: Membaca dan parse SQL source file ke in-memory database
2. **Schema Knowledge Manager**: Interface ke Graphiti untuk schema consultation
3. **Query Execution Engine**: Tool untuk execute SQL query dengan validasi
4. **Placeholder Manager**: System untuk generate dan replace placeholder
5. **LangGraph Workflow**: State machine untuk orchestrate seluruh proses
6. **Validation Engine**: Multi-layer validation untuk data quality

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

## 4. Penanganan SQL Source File

### Data Loading Strategy
1. **Parse SQL File**: Extract CREATE TABLE statements untuk mendapatkan struktur schema
2. **Schema Registration**: Simpan informasi tabel dan kolom ke Graphiti sebagai knowledge base
3. **Data Loading**: Execute INSERT statements ke SQLite in-memory database
4. **Metadata Enrichment**: Analisis otomatis untuk kategorisasi kolom (financial, temporal, descriptive)

### Schema Knowledge Storage di Graphiti
Untuk setiap tabel, simpan informasi:
- **Table Purpose**: "sales tracking", "customer management", "product catalog"
- **Business Category**: "financial", "operational", "master_data"
- **Column Classification**: financial_amount, identifier, temporal, descriptive
- **Aggregation Capability**: apakah kolom bisa di-SUM, AVG, COUNT
- **Relationship Mapping**: foreign key relationships antar tabel

### Contoh Knowledge Graph Structure
```
Table: sales_orders
- Purpose: "transaction recording"
- Category: "financial"
- Columns:
  - order_id (type: identifier, aggregatable: false)
  - customer_id (type: identifier, aggregatable: false)
  - order_date (type: temporal, aggregatable: false)
  - total_amount (type: financial_amount, aggregatable: true)
  - status (type: descriptive, aggregatable: false)

Relationships:
- sales_orders.customer_id → customers.customer_id
- sales_orders.order_id ← order_lines.order_id
```

## 5. LangGraph Workflow Design

### State Structure
```
AgentState:
  # Input & User Context
  - user_query: string
  - session_id: string
  - conversation_history: list
  
  # Query Understanding
  - intent: string (sales_analysis, customer_aging, etc.)
  - entities_mentioned: list (customer, product, date_range)
  - time_period: dict (start_date, end_date)
  - requested_metrics: list (total, average, count)
  
  # Schema Knowledge
  - relevant_tables: list
  - table_relationships: list
  - financial_columns: dict
  - aggregation_plan: dict
  
  # Execution Planning
  - sql_queries: list
  - response_template: string (with placeholders)
  - placeholder_mapping: dict
  
  # Results & Validation
  - raw_query_results: list
  - financial_calculations: dict
  - data_quality_checks: dict
  - validation_warnings: list
  
  # Output Generation
  - data_table_for_display: list
  - final_narrative: string
  - visualization_config: dict
```

### Enhanced Workflow dengan Real-Time Monitoring

**Node 1: Understand User Query (Target: <1s)**
```
UI Status: 🔄 Understanding your request...
Process Monitor:
├── 🧠 LLM Intent Analysis: 0.6s
├── 📝 Entity Extraction: 0.2s  
└── ⚙️ Context Update: +45 tokens

Progress: [████████████████████████░] 96%
```
- Parse natural language query dengan timing precision
- Identify business intent (sales analysis, customer report, etc.)
- Extract entities (customer names, date ranges, product categories)
- Real-time token counting dan context impact estimation

**Node 2: Consult Schema Knowledge (Target: <2s)**
```
UI Status: 🗄️ Consulting database schema knowledge...
Process Monitor:
├── 🔍 GraphDB Query: 1.2s
├── 📊 Schema Analysis: 0.3s
├── 🔗 Relationship Mapping: 0.4s
└── ⚙️ Context Update: +2,850 tokens

Fallback Status: Primary approach successful ✅
```
- Query Graphiti dengan detailed timing metrics
- Build "execution roadmap" dengan fallback options prepared
- Real-time schema knowledge loading dengan progress indication

**Node 3: Plan Query Execution (Target: <2s)**
```
UI Status: ⚙️ Planning database queries and response format...
Process Monitor:
├── 🧠 LLM Query Planning: 1.4s
├── 📝 Template Generation: 0.3s
├── 🔍 Validation Prep: 0.2s
└── ⚙️ Context Update: +1,240 tokens

Placeholder Count: 7 placeholders prepared
```
- Generate SQL plan dengan fallback strategies included
- Create response template dengan comprehensive placeholder mapping
- Prepare validation rules dengan estimated execution time

**Node 4: Execute SQL Queries dengan Fallback (Target: <3s)**
```
UI Status: 🔍 Executing database queries (Attempt 1/3)...
Process Monitor:
├── 💾 Primary Query: Failed (0.8s) ❌
├── 🔄 Fallback Query #1: Success (1.2s) ✅
├── 📊 Data Processing: 0.4s
└── ⚙️ Context Update: +4,780 tokens

Fallback Reason: Table 'customer_payments' not found → Used invoice-payment JOIN
```
- Maximum 3 retry attempts dengan intelligent fallback strategies
- Real-time query execution monitoring dengan error explanations
- Detailed timing breakdown per query attempt

**Node 5: Validate & Process Results (Target: <1s)**
```
UI Status: 🔍 Validating data quality and consistency...
Process Monitor:
├── ✅ Data Quality Checks: 0.3s
├── ⚠️ Business Rule Validation: 0.2s
├── 📊 Statistical Analysis: 0.4s
└── ⚙️ Context Update: +680 tokens

Quality Score: 95/100 ⭐⭐⭐⭐⭐
```
- Comprehensive validation dengan quality scoring
- Real-time anomaly detection dengan user-friendly explanations
- Warning generation dengan business context

**Node 6: Replace Placeholders & Generate Output (Target: <1s)**
```
UI Status: 📝 Generating final response and formatting...
Process Monitor:
├── 🔄 Placeholder Replacement: 0.2s
├── 💰 Currency Formatting: 0.1s
├── 📊 Table Preparation: 0.3s
└── ⚙️ Context Update: +920 tokens

Final Context Usage: [████████░░] 78% (15,240/19,500 tokens)
```
- Smart placeholder replacement dengan locale-aware formatting
- Final output assembly dengan export-ready data tables
- Context optimization suggestions untuk future queries

### Conditional Logic & Error Handling
- **If schema knowledge incomplete**: Fallback ke basic table inspection
- **If query execution fails**: Generate alternative simpler queries
- **If data validation fails**: Include prominent warnings dalam output
- **If no data found**: Generate appropriate "no data" response

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

## 7. User Experience Design dengan Real-Time Monitoring

### Real-Time Process Monitoring Interface

**1. Context Window & Token Meter**
```
State Context Usage: [████████░░] 78% (15,240 / 19,500 tokens)
⚠️ Warning: Approaching context limit

Token Breakdown:
- User Query: 45 tokens
- Schema Knowledge: 8,950 tokens  
- Query Results: 4,780 tokens
- Conversation History: 1,465 tokens
```

**2. Process Timing Dashboard**
```
🕐 Total Processing Time: 11.2 seconds

Breakdown:
├── 🧠 LLM API Calls: 4.1 sec (36.6%)
├── 🗄️ GraphDB Query: 1.6 sec (14.3%)  
├── 🔍 MySQL Query: 2.3 sec (20.5%)
├── ⚙️ Data Processing: 0.8 sec (7.1%)
├── 🔍 Reasoning & Planning: 1.9 sec (17.0%)
└── 📊 Output Formatting: 0.5 sec (4.5%)
```

**3. Real-Time Progress Bar dengan Checkpoints**
```
Agent Process Monitor:

✅ 1. Understanding User Query          [Completed - 0.8s]
✅ 2. Consulting Schema Knowledge       [Completed - 1.6s]  
✅ 3. Planning SQL Execution           [Completed - 2.1s]
🔄 4. Executing Database Queries       [In Progress...]
⏳ 5. Validating Results              [Pending]
⏳ 6. Generating Response              [Pending]

Current Status: Fetching customer payment data...
```

**4. Fallback & Retry Mechanism Display**
```
🔄 Retry Attempts Monitor:

Query Attempt #1: ❌ Failed - Table 'customer_payments' not found
├── Fallback Strategy: Searching alternative table names
├── GraphDB consulted for similar tables

Query Attempt #2: ❌ Failed - No data for specified date range  
├── Fallback Strategy: Expanding date range to find nearest data
├── Checking adjacent months: Dec 2022, Feb 2023

Query Attempt #3: ✅ Success - Found data in 'invoices' table
├── Alternative approach: Using invoice-payment LEFT JOIN
├── Results: 156 records found

Final Status: ✅ Query successful with fallback approach #3
```

### Enhanced Display Format untuk User

**1. Session Management Panel**
```
Current Session: session_2024_001    [New Chat] [Reset State]

Session Stats:
- Queries Processed: 7
- Context Usage: 78%  
- Average Response Time: 8.4s
- Success Rate: 85.7% (6/7 successful)
```

**2. Interactive Raw Data Table dengan Monitoring**
```
📊 Query Results (Retrieved in 2.3s)
Context Impact: +4,780 tokens

[Export CSV] [Export Excel] [Save to Session]

| Customer Name | Outstanding | Days Overdue | ••• |
|---------------|-------------|--------------|-----|
| PT ABC Corp   | Rp 15M     | 45 days      | ••• |
| CV XYZ        | Rp 8.5M    | 40 days      | ••• |

Showing 3 of 3 results • Loaded in 0.8s • Quality Score: 95%
```

**3. Enhanced Executive Summary dengan Performance Metrics**
```
📈 Executive Summary (Generated in 1.9s)

Key Findings:
• Total Outstanding: Rp 29.5M (3 customers)
• Average Overdue: 40 days
• Risk Level: Medium-High

Performance Metrics:
• Query Accuracy: 100%
• Data Freshness: Current (last updated 1 hour ago)  
• Processing Efficiency: 11.2s (Fast)
• Context Utilization: 78% (Good)
```

**4. Detailed Validation & Quality Panel**
```
🔍 Data Quality Assessment (Completed in 0.4s)

Quality Score: 95/100 ⭐⭐⭐⭐⭐

Checks Performed:
✅ Negative Values: None found
✅ Null Data: 0% missing values  
✅ Date Validity: All dates logical
✅ Business Rules: Passed
⚠️ Large Amounts: 1 invoice >Rp 10M (flagged for review)

Fallback History:
🔄 Initial query failed → Used alternative table structure
✅ Fallback successful → Results verified
```

### Advanced Error Handling & Fallback UI

**1. Intelligent Fallback Strategy Display**
```
🤖 Agent Reasoning Process:

Primary Approach Failed:
❌ "SELECT * FROM customer_payments WHERE..."
   Error: Table 'customer_payments' does not exist

Fallback Strategy #1:
🔄 Consulting GraphDB for alternative table names...
   Found: ['invoices', 'payments', 'billing_records']

Fallback Strategy #2:  
🔄 Reconstructing query using 'invoices' + 'payments' LEFT JOIN...
   Testing: "SELECT customers.name, invoices.amount..."

Success with Alternative Approach:
✅ Query executed successfully using invoice-payment relationship
✅ Data validation passed
✅ Results formatted for display

Agent Learning: Saved successful pattern for future similar queries
```

**2. Failure Analysis dengan User-Friendly Explanation**
```
❌ Query Failed After 3 Attempts

What the Agent Tried:
1. Direct customer payment table lookup → Table not found
2. Alternative payment tracking tables → No matching data  
3. Reconstructed approach using invoices → Data format mismatch

Why This Happened:
• Database schema doesn't match expected structure
• Requested date range might be outside available data
• Payment tracking might use different table organization

What You Can Try:
• Check if data exists for different time periods
• Try similar queries with broader criteria
• Use "show me available tables" to explore schema

Technical Details: [Show Details] [Contact Support]
```

### Context & Performance Optimization Features

**1. Smart Context Management**
```
🧠 Context Window Optimization

Current Usage: [████████░░] 15,240/19,500 tokens (78%)

Optimization Suggestions:
• Conversation history can be compressed (-2,400 tokens)
• Old query results can be archived (-1,800 tokens)  
• Redundant schema info can be cached (-950 tokens)

[Apply Optimizations] [Archive Old Data] [Start Fresh Session]

Predicted Impact: Will free up 5,150 tokens (26% reduction)
```

**2. Performance Analytics Dashboard**
```
⚡ Performance Analytics

Current Session Performance:
• Average Query Time: 8.4s (Target: <10s) ✅
• Success Rate: 85.7% (Target: >80%) ✅  
• Context Efficiency: 78% (Target: <85%) ✅
• User Satisfaction: N/A (Awaiting feedback)

Bottleneck Analysis:
🐌 Slowest Component: LLM API calls (4.1s avg)
⚡ Fastest Component: Data formatting (0.5s avg)
🎯 Optimization Opportunity: Cache schema knowledge (-1.2s potential)

[View Detailed Metrics] [Export Performance Report]
```

### Session Management & Reset Capabilities

**1. Smart Session Control**
```
📱 Session Management

Current Session: session_2024_001 (Started: 14:30 WIB)
├── Duration: 15 minutes
├── Queries: 7 successful, 1 failed
├── Context Used: 78% 
└── Last Activity: 2 minutes ago

Actions:
[🆕 New Chat] - Start fresh session (clears all context)
[🔄 Reset Context] - Keep conversation, clear technical state  
[💾 Save Session] - Bookmark current progress
[📤 Export History] - Download conversation + data

Warning: Starting new chat will lose current schema knowledge
Estimated reload time: ~3 seconds for schema re-learning
```

**2. Context Reset Options**
```
🔄 Context Reset Options

What to Keep:
☑️ Database schema knowledge (saves 3s reload time)  
☑️ User preferences & settings
☐ Previous query results (will free 4,780 tokens)
☐ Conversation history (will free 1,465 tokens)  

What to Reset:
☑️ Current processing state
☑️ Temporary calculations
☑️ Error histories
☑️ Performance metrics

Expected Impact:
• Context Usage: 78% → 35% 
• Available Tokens: +6,245
• Reload Time: <1 second (schema kept)

[Apply Reset] [Cancel]
```

### Contoh Output Lengkap

**User Query**: "Tunjukkan customer siapa saja yang belum lunas membayar beserta due date nya"

**Output yang Digenerate**:

**📊 Raw Data Table**
| Customer Name | Invoice Number | Invoice Amount | Outstanding | Due Date | Days Overdue |
|---------------|----------------|----------------|-------------|----------|--------------|
| PT ABC Corp | INV-001 | Rp 15.000.000 | Rp 15.000.000 | 2023-01-15 | 45 |
| CV XYZ | INV-002 | Rp 8.500.000 | Rp 8.500.000 | 2023-01-20 | 40 |
| PT DEF Ltd | INV-003 | Rp 12.000.000 | Rp 6.000.000 | 2023-01-25 | 35 |

**📈 Executive Summary**
- Total Outstanding: Rp 29.500.000
- Customer Count: 3 customers
- Average Days Overdue: 40 days
- Highest Risk: PT ABC Corp (Rp 15.000.000, 45 days overdue)

**📝 Analysis Narrative**
"Berdasarkan analisis piutang per tanggal 1 Maret 2023, terdapat 3 customer dengan total outstanding sebesar Rp 29.500.000. Customer dengan risiko tertinggi adalah PT ABC Corp dengan outstanding Rp 15.000.000 yang telah overdue selama 45 hari. 

Rekomendasi tindakan:
1. Follow up prioritas untuk PT ABC Corp (100% outstanding)
2. Monitoring ketat untuk CV XYZ (100% outstanding)  
3. PT DEF Ltd menunjukkan partial payment, perlu follow up untuk sisanya

Rata-rata days overdue 40 hari mengindikasikan perlu perbaikan dalam collection process."

**⚠️ Data Quality & Validations**
- ✅ All outstanding amounts are positive
- ✅ Due dates are valid and in the past
- ✅ Customer names are not null
- ⚠️ Note: Analysis based on data as of March 1, 2023
- ⚠️ Warning: 1 customer has partial payment (check payment allocation)

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