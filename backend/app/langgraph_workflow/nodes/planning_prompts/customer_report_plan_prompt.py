# backend/app/langgraph_workflow/nodes/planning_prompts/customer_report_plan_prompt.py
from typing import Optional, List, Dict, Any

def get_customer_report_prompt_parts(
    intent: str,
    time_period_display_str: str, 
) -> Dict[str, str]:
    
    # Ini bisa kita sesuaikan dengan result_key yang dihasilkan oleh contoh di markdown
    # Dari markdown, contohnya menggunakan:
    # UNPAID_CUSTOMERS_DETAIL, COUNT_UNPAID_CUSTOMERS, SUM_TOTAL_OUTSTANDING_ALL
    
    # Untuk narasi, kita butuh COUNT dan SUM keseluruhan.
    count_unpaid_cust_key = f"COUNT_UNPAID_CUSTOMERS" 
    sum_total_outstanding_key = f"SUM_TOTAL_OUTSTANDING_ALL"
    
    # Jika ada periode waktu, kita bisa tambahkan ke key untuk membuatnya lebih unik jika perlu
    # Namun, contoh di markdown sudah memberikan nama result_key yang bagus.
    # Kita akan gunakan itu langsung di contoh JSON.

    intent_specific_json_example = f"""
    {{
      "operations": [  // Mengacu pada "Contoh Complete DatabaseOperationPlan"
        // ... SALIN OPERASI 1 (get_unpaid_customers_detail) DARI MARKDOWN KE SINI ...
        // Pastikan format JSON-nya benar
        {{
          "operation_id": "get_unpaid_customers_detail",
          "operation_type": "select",
          "purpose": "Mendapatkan daftar customer yang memiliki tagihan belum lunas beserta total outstanding per customer {time_period_display_str}",
          "main_table": "arbook",
          "select_columns": [
            {{"table": "arbook", "column": "CustomerCode", "alias": "customer_code"}},
            {{"table": "mastercustomer", "column": "Name", "alias": "customer_name"}},
            {{"table": "arbook", "column": "DocValueLocal", "alias": "total_tagihan", "aggregation": "SUM"}},
            {{"table": "customerpaymentd", "column": "PaymentLocal", "alias": "total_pembayaran", "aggregation": "SUM"}},
            {{"table": null, "column": "SUM(arbook.DocValueLocal) - SUM(IFNULL(customerpaymentd.PaymentLocal, 0))", "alias": "total_outstanding"}}
          ],
          "joins": [
            {{"type": "INNER", "table": "mastercustomer", "on_conditions": [
              {{"left_table": "arbook", "left_column": "CustomerCode", "operator": "=", "right_table": "mastercustomer", "right_column": "Code"}}
            ]}},
            {{"type": "LEFT", "table": "customerpaymentd", "on_conditions": [
              {{"left_table": "arbook", "left_column": "DocNo", "operator": "=", "right_table": "customerpaymentd", "right_column": "ARDocNo"}}
            ]}}
          ],
          "filters": null, // Sesuaikan jika perlu filter waktu berdasarkan time_period_display_str
          "group_by_columns": ["arbook.CustomerCode", "mastercustomer.Name"],
          "having_conditions": {{
            "logic": "AND",
            "conditions": [
              {{"table": null, "column": "SUM(arbook.DocValueLocal) - SUM(IFNULL(customerpaymentd.PaymentLocal, 0))", "operator": ">", "value": "0", "value_type": "literal"}}
            ],
            "groups": []
          }},
          "order_by_clauses": [{{"table": null, "column": "total_outstanding", "direction": "DESC"}}],
          "limit": 50, // Ubah ini untuk raw_data_operation_plan, untuk agregasi ini mungkin tidak perlu limit
          "result_key": "UNPAID_CUSTOMERS_DETAIL_LIST", // Ganti result key ini agar tidak bentrok dengan raw data table
          "expected_result_format": "record" // atau list_of_dicts
        }},
        // ... SALIN OPERASI 2 (count_unpaid_customers) DARI MARKDOWN KE SINI ...
        {{
          "operation_id": "count_unpaid_customers",
          "operation_type": "select",
          "purpose": "Menghitung jumlah customer unik yang belum lunas untuk summary {time_period_display_str}",
          "main_table": "arbook", // Ini perlu subquery sebenarnya untuk hasil akurat
          "select_columns": [
            {{"table": "arbook", "column": "CustomerCode", "alias": "{count_unpaid_cust_key}", "aggregation": "COUNT", "distinct": true}}
            // Seharusnya: SELECT COUNT(*) FROM (SELECT DISTINCT ar.CustomerCode FROM arbook ar LEFT JOIN customerpaymentd cpd ON ar.DocNo = cpd.ARDocNo GROUP BY ar.CustomerCode HAVING SUM(ar.DocValueLocal - IFNULL(cpd.PaymentLocal,0)) > 0 ) as Sub
          ],
          "joins": [ // Join dan having ini mungkin tidak tepat jika tujuannya hanya COUNT dari hasil yang sudah difilter outstanding
            {{"type": "LEFT", "table": "customerpaymentd", "on_conditions": [
              {{"left_table": "arbook", "left_column": "DocNo", "operator": "=", "right_table": "customerpaymentd", "right_column": "ARDocNo"}}
            ]}}
          ],
          "filters": null, // Tambahkan filter waktu jika ada
          // "group_by_columns": ["arbook.CustomerCode"], // Untuk COUNT DISTINCT keseluruhan, group by ini salah
          "having_conditions": {{ // Ini juga perlu subquery
            "logic": "AND",
            "conditions": [
              {{"table": null, "column": "SUM(arbook.DocValueLocal) - SUM(IFNULL(customerpaymentd.PaymentLocal, 0))", "operator": ">", "value": "0", "value_type": "literal"}}
            ],
            "groups": []
          }},
          "result_key": "{count_unpaid_cust_key}",
          "expected_result_format": "single_value"
        }},
        // ... SALIN OPERASI 3 (sum_total_outstanding) DARI MARKDOWN KE SINI ...
        {{
          "operation_id": "sum_total_outstanding_all",
          "operation_type": "select",
          "purpose": "Menghitung total keseluruhan outstanding untuk summary {time_period_display_str}",
          "main_table": "arbook", // Ini juga perlu subquery
          "select_columns": [
            {{"table": null, "column": "SUM(arbook.DocValueLocal - IFNULL(customerpaymentd.PaymentLocal, 0))", "alias": "{sum_total_outstanding_key}"}}
            // Seharusnya: SELECT SUM(OutstandingAmount) FROM ( SELECT (SUM(ar.DocValueLocal) - SUM(IFNULL(cpd.PaymentLocal,0))) as OutstandingAmount FROM arbook ar ... GROUP BY ar.DocNo HAVING ... )
          ],
          "joins": [
             {{"type": "LEFT", "table": "customerpaymentd", "on_conditions": [
              {{"left_table": "arbook", "left_column": "DocNo", "operator": "=", "right_table": "customerpaymentd", "right_column": "ARDocNo"}}
            ]}}
          ],
          "filters": null, // Tambahkan filter waktu jika ada
          // "group_by_columns": null, // Untuk SUM keseluruhan, ini benar
          "having_conditions": {{ // Untuk filter per dokumen sebelum di SUM total
             "logic":"AND",
             "conditions": [
                 {{"table": null, "column": "(arbook.DocValueLocal - SUM(IFNULL(customerpaymentd.PaymentLocal, 0)))", "operator": ">", "value": "0", "value_type": "literal", "is_expression_in_having": true}}
             ],
             "groups": [] // Group by arbook.DocNo diperlukan agar having ini benar
          }},
          "result_key": "{sum_total_outstanding_key}",
          "expected_result_format": "single_value"
        }}
      ],
      "raw_data_operation_plan": {{ // Ini dari Pattern 1 di markdown, tapi kita sesuaikan select_columns dan result_key
        "operation_id": "fetch_raw_unpaid_customers_detail_for_table",
        "operation_type": "select", // Sesuai struktur baru di prompt
        "purpose": "Mendapatkan daftar detail customer yang memiliki tagihan belum lunas {time_period_display_str}",
        "main_table": "arbook",
        "select_columns": [
            {{ "table": "arbook", "column": "CustomerCode", "alias": "CustomerCode"}},
            {{ "table": "mastercustomer", "column": "Name", "alias": "customer_name"}},
            {{ "table": "arbook", "column": "DocNo", "alias": "DocNo"}},
            {{ "table": "arbook", "column": "DueDate", "alias": "DueDate"}},
            {{ "table": "arbook", "column": "DocValueLocal", "alias": "DocValueLocal"}},
            {{ "table": null, "column": "SUM(IFNULL(customerpaymentd.PaymentLocal, 0))", "alias": "total_paid"}},
            {{ "table": null, "column": "(SUM(arbook.DocValueLocal) - SUM(IFNULL(customerpaymentd.PaymentLocal, 0)))", "alias": "outstanding_amount"}}
        ],
        "joins": [
            {{ "type": "INNER", "table": "mastercustomer", "on_conditions": [
                {{ "left_table": "arbook", "left_column": "CustomerCode", "operator": "=", "right_table": "mastercustomer", "right_column": "Code"}}
            ]}},
            {{ "type": "LEFT", "table": "customerpaymentd", "on_conditions": [
                {{ "left_table": "arbook", "left_column": "DocNo", "operator": "=", "right_table": "customerpaymentd", "right_column": "ARDocNo"}}
            ]}}
        ],
        "filters": null, // Filter waktu jika ada
        "group_by_columns": ["arbook.CustomerCode", "mastercustomer.Name", "arbook.DocNo", "arbook.DueDate", "arbook.DocValueLocal"],
        "having_conditions": {{
            "logic": "AND",
            "conditions": [
                {{ "table": null, "column": "(SUM(arbook.DocValueLocal) - SUM(IFNULL(customerpaymentd.PaymentLocal, 0)))", "operator": ">", "value": "0", "value_type": "literal"}}
            ],
            "groups": []
        }},
        "order_by_clauses": [
            {{ "table": null, "column": "outstanding_amount", "direction": "DESC"}},
            {{ "table": "mastercustomer", "column": "Name", "direction": "ASC"}}
        ],
        "limit": 50,
        "result_key": "RAW_DATA_TABLE", // Ini sudah standar
        "expected_result_format": "record" // Sesuai
      }},
      "response_template": "Ditemukan {{{{ {count_unpaid_cust_key} }}}} customer yang memiliki tagihan belum lunas, dengan total keseluruhan nilai piutang sebesar {{{{ {sum_total_outstanding_key} }}}}.",
      "placeholder_mapping": {{
        "{count_unpaid_cust_key}": {{ "type": "number_with_separator", "label": "Jumlah Customer Belum Lunas ({time_period_display_str})" }},
        "{sum_total_outstanding_key}": {{ "type": "currency_IDR", "precision": 0, "label": "Total Keseluruhan Piutang ({time_period_display_str})" }}
      }},
      "data_source_info": {{
        "description": "Data piutang customer diambil dari tabel arbook, mastercustomer, dan customerpaymentd.",
        "tables_used": ["arbook", "mastercustomer", "customerpaymentd"],
        "join_details": [
            "arbook JOIN mastercustomer ON arbook.CustomerCode = mastercustomer.Code",
            "arbook LEFT JOIN customerpaymentd ON arbook.DocNo = customerpaymentd.ARDocNo"
        ],
        "filters_applied": ["Outstanding amount > 0"]
      }}
    }}
    """

    intent_specific_rules = """
Aturan Khusus untuk Laporan Customer (Piutang):
1.  Setiap objek dalam list `database_operations_plan` dan `raw_data_operation_plan` HARUS memiliki field "operation_id", "operation_type", "purpose", "main_table", dan "select_columns". "result_key" juga wajib.
2.  `main_table` HARUS diisi.
3.  `on_conditions` dalam `joins` HARUS berupa list of dictionaries dengan "left_table", "left_column", "operator", "right_table", "right_column".
4.  Untuk menghitung piutang:
    - Gunakan `arbook.DocValueLocal` sebagai nilai tagihan.
    - Gunakan `SUM(IFNULL(customerpaymentd.PaymentLocal, 0))` sebagai total pembayaran per `arbook.DocNo`. Lakukan `LEFT JOIN` dari `arbook` ke `customerpaymentd` ON `arbook.DocNo = customerpaymentd.ARDocNo`.
    - Piutang per dokumen adalah `(arbook.DocValueLocal - SUM(IFNULL(customerpaymentd.PaymentLocal, 0)))`.
    - Filter dengan `HAVING (arbook.DocValueLocal - SUM(IFNULL(customerpaymentd.PaymentLocal, 0))) > 0`. Ini memerlukan `GROUP BY` yang mencakup `arbook.DocNo` dan `arbook.DocValueLocal`.
5.  Untuk `database_operations_plan`:
    a. **Operasi 1 (Menghitung Jumlah Customer Unik Belum Lunas)**:
       - `operation_id`: "count_unpaid_customers"
       - `purpose`: "Menghitung jumlah customer unik yang memiliki tagihan belum lunas {time_period_display_str}"
       - `main_table`: "arbook"
       - `select_columns`: `[ {{"table": "arbook", "column": "CustomerCode", "alias": "count_customers", "aggregation": "COUNT", "distinct": true}} ]`
       - `joins` ke `customerpaymentd`.
       - `group_by_columns`: `["arbook.CustomerCode"]` (untuk distinct customer)
       - `having_conditions`: Harus memfilter customer yang total piutangnya > 0. Ini mungkin memerlukan subquery atau pendekatan CTE yang lebih kompleks yang mungkin sulit bagi Anda untuk buat sebagai JSON. Alternatif: Jika Anda bisa membuat query yang menghitung outstanding per customer, lalu hitung COUNT dari hasilnya. Atau, buat operasi yang mengambil daftar CustomerCode unik yang belum lunas, lalu Python yang melakukan len().
       - **PENDEKATAN YANG LEBIH DIANJURKAN untuk LLM**: Buat operasi yang mengambil CustomerCode unik yang memiliki setidaknya satu invoice belum lunas. `select_columns: [{{"table": "arbook", "column": "CustomerCode", "distinct": true}}]`, lalu lakukan `LEFT JOIN customerpaymentd`, `GROUP BY arbook.CustomerCode, arbook.DocNo, arbook.DocValueLocal`, dan `HAVING (SUM(arbook.DocValueLocal) - SUM(IFNULL(customerpaymentd.PaymentLocal, 0))) > 0`. Hasilnya akan berupa list CustomerCode, Python akan menghitung `len()`. Maka `expected_result_format` menjadi `list`. Atau, jika Anda BISA membuat query SQL yang langsung menghasilkan SATU ANGKA untuk COUNT DISTINCT customer yang outstanding, itu lebih baik. Coba ini: `select_columns: [{"table": null, "column": "COUNT(DISTINCT sub.CustomerCode)", "alias": "count_customers"}]` dengan subquery yang tepat di `main_table` atau via common table expression (CTE) yang Anda definisikan.
       - **TARGET SEDERHANA UNTUK LLM (COUNT)**: `main_table` subquery: `(SELECT ar.CustomerCode FROM arbook ar LEFT JOIN customerpaymentd cpd ON ar.DocNo = cpd.ARDocNo GROUP BY ar.CustomerCode, ar.DocNo, ar.DocValueLocal HAVING (ar.DocValueLocal - SUM(IFNULL(cpd.PaymentLocal, 0))) > 0) AS UnpaidInvoicesPerCustomer`, lalu `select_columns: [{{"table": "UnpaidInvoicesPerCustomer", "column": "CustomerCode", "aggregation": "COUNT_DISTINCT", "alias": "..."}}]`. Jika ini terlalu kompleks, minta LLM untuk hanya mengambil daftar CustomerCode unik, dan Python yang menghitungnya. Untuk sekarang, coba hasilkan query `COUNT(DISTINCT arbook.CustomerCode)` dengan join dan having yang benar untuk filter outstanding per invoice.
       - `result_key`: `{count_unpaid_cust_key}`
       - `expected_result_format`: "single_value"
    b. **Operasi 2 (Menghitung Total Keseluruhan Outstanding)**:
       - `operation_id`: "sum_total_outstanding"
       - `purpose`: "Menghitung total keseluruhan nilai piutang dari semua customer yang belum lunas {time_period_display_str}"
       - `main_table`: "arbook"
       - `select_columns`: `[ {{"table": null, "column": "SUM(arbook.DocValueLocal - IFNULL(TotalPaidPerDoc, 0))", "alias": "total_outstanding_value"}} ]` Ini juga memerlukan subquery untuk `TotalPaidPerDoc = SUM(customerpaymentd.PaymentLocal)`.
       - **TARGET SEDERHANA UNTUK LLM (SUM)**: `main_table` berupa subquery: `(SELECT (ar.DocValueLocal - SUM(IFNULL(cpd.PaymentLocal,0))) AS OutstandingAmountForDoc FROM arbook ar LEFT JOIN customerpaymentd cpd ON ar.DocNo = cpd.ARDocNo GROUP BY ar.DocNo, ar.DocValueLocal HAVING (ar.DocValueLocal - SUM(IFNULL(cpd.PaymentLocal,0))) > 0) AS OutstandingDocs`, lalu `select_columns: [{{"table":"OutstandingDocs", "column":"OutstandingAmountForDoc", "aggregation":"SUM", "alias":"..."}}]`.
       - `joins` ke `customerpaymentd`.
       - `group_by_columns` (mungkin tidak perlu jika sudah di subquery).
       - `having_conditions` (mungkin tidak perlu jika sudah di subquery).
       - `result_key`: `{sum_total_outstanding_key}`
       - `expected_result_format`: "single_value"
6.  `raw_data_operation_plan` harus mengambil DAFTAR DETAIL CUSTOMER dan OUTSTANDING PER CUSTOMER (bukan per invoice). Jadi perlu agregasi SUM(outstanding_per_invoice) di sini juga, di-group by CustomerCode dan Name.
7.  `response_template` harus menggunakan `result_key` dari poin 5a dan 5b.
"""
    return {
        "intent_specific_json_example": intent_specific_json_example,
        "intent_specific_rules": intent_specific_rules
    }