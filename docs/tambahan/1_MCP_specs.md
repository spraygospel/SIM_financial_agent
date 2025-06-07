
**Dokumen Perencanaan Tambahan 1: Spesifikasi Detail MCP Server**

**Versi Dokumen**: 1.0
**Tanggal**: 23 Oktober 2024

**Daftar Isi**:
1.  Pendahuluan
2.  MCP Server untuk Graphiti (`graphiti_mcp_server`)
    2.1. Deskripsi Umum
    2.2. Tools yang Diekspos
        2.2.1. `get_relevant_schema_info`
    2.3. Struktur Data (Pydantic Models)
    2.4. Contoh Request dan Response
3.  MCP Server untuk MySQL (`mysql_mcp_server`)
    3.1. Deskripsi Umum
    3.2. Tools yang Diekspos
        3.2.1. `execute_sql_query`
    3.3. Struktur Data (Pydantic Models)
    3.4. Contoh Request dan Response
4.  MCP Server untuk Placeholder System (`placeholder_mcp_server`)
    4.1. Deskripsi Umum
    4.2. Tools yang Diekspos
        4.2.1. `fill_placeholders`
    4.3. Struktur Data (Pydantic Models)
    4.4. Contoh Request dan Response

---

**1. Pendahuluan**

Dokumen ini merinci spesifikasi teknis untuk setiap Model Context Protocol (MCP) Server yang akan digunakan oleh AI Agent. MCP Server bertindak sebagai jembatan antara logika inti agent (yang diorkestrasi oleh LangGraph) dan berbagai layanan eksternal seperti Graphiti (untuk metadata skema), MySQL (untuk eksekusi data), dan Placeholder System (untuk pemformatan output).

Setiap MCP Server akan mengekspos satu atau lebih "tools" yang dapat dipanggil oleh agent melalui protokol MCP. Desain tools ini difokuskan pada efisiensi dan relevansi data yang dikembalikan untuk mengoptimalkan penggunaan context window LLM.

---

**2. MCP Server untuk Graphiti (`graphiti_mcp_server`)**

**2.1. Deskripsi Umum**
`graphiti_mcp_server` bertanggung jawab untuk menyediakan informasi metadata skema database yang relevan dari knowledge graph Graphiti. Informasi ini akan digunakan oleh agent untuk memahami struktur data dan merencanakan query SQL yang tepat.

**2.2. Tools yang Diekspos**

   **2.2.1. Tool: `get_relevant_schema_info`**
    *   **Deskripsi**: Mengambil informasi skema (tabel, kolom, relasi) yang paling relevan dari Graphiti berdasarkan intent dan entitas yang terdeteksi dari query pengguna. Tool ini dirancang untuk memberikan *hanya* potongan skema yang dibutuhkan, bukan keseluruhan skema database, demi efisiensi *context window*.
    *   **Input Parameters**:
        ```python
        from pydantic import BaseModel, Field
        from typing import List, Dict

        class GetRelevantSchemaInfoInput(BaseModel):
            intent: str = Field(..., description="Intent utama yang terdeteksi dari query pengguna, misal 'sales_analysis'.")
            entities: List[str] = Field(..., description="Daftar entitas yang terdeteksi, misal ['sales', 'monthly_data', 'revenue'].")
            # Optional: Tambahkan parameter untuk mengontrol kedalaman atau detail informasi skema jika diperlukan
            # max_related_tables: int = Field(default=3, description="Jumlah maksimum tabel terkait yang akan diambil.")
        ```
    *   **Output Structure**:
        ```python
        # (Struktur data ini akan didefinisikan di bagian 2.3)
        class RelevantSchemaOutput(BaseModel):
            relevant_tables: List[TableSchemaMcp] = Field(description="Daftar tabel yang dianggap relevan.")
            table_relationships: List[RelationshipMcp] = Field(description="Daftar relasi antar tabel yang relevan.")
            financial_columns: Dict[str, List[str]] = Field(description="Kolom finansial per tabel relevan.")
            temporal_columns: Dict[str, List[str]] = Field(description="Kolom temporal per tabel relevan.")
            # Tambahkan key lain jika ada info skema penting lain yang ringkas
            # primary_keys: Dict[str, str] = Field(description="Primary key per tabel relevan.")
            # common_join_columns: List[str] = Field(description="Kolom yang sering digunakan untuk join.")
        ```

**2.3. Struktur Data (Pydantic Models) untuk `graphiti_mcp_server`**
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ColumnMcp(BaseModel):
    name: str = Field(description="Nama kolom.")
    type: str = Field(description="Tipe data kolom (misal, VARCHAR, INTEGER, DATE).")
    description: Optional[str] = Field(default=None, description="Deskripsi fungsional kolom dari Graphiti.")
    classification: Optional[str] = Field(default=None, description="Klasifikasi kolom (misal, 'temporal', 'financial_amount', 'identifier', 'descriptive').")
    is_aggregatable: Optional[bool] = Field(default=False, description="Apakah kolom ini bisa diagregasi (SUM, AVG, COUNT).")
    # Contoh detail tambahan yang mungkin berguna:
    # sample_values: Optional[List[str]] = Field(default_factory=list, description="Contoh nilai dari kolom ini.")
    # is_primary_key: bool = Field(default=False)
    # is_foreign_key: bool = Field(default=False)
    # foreign_key_to_table: Optional[str] = Field(default=None)

class TableSchemaMcp(BaseModel):
    table_name: str = Field(description="Nama tabel.")
    purpose: Optional[str] = Field(default=None, description="Deskripsi tujuan tabel dari Graphiti.")
    columns: List[ColumnMcp] = Field(description="Daftar kolom dalam tabel ini.")
    # Contoh detail tambahan:
    # relevance_score: Optional[float] = Field(default=0.0, description="Skor relevansi tabel terhadap query.")

class RelationshipMcp(BaseModel):
    from_table: str = Field(description="Tabel asal relasi.")
    from_column: str = Field(description="Kolom asal pada tabel asal.")
    to_table: str = Field(description="Tabel tujuan relasi.")
    to_column: str = Field(description="Kolom tujuan pada tabel tujuan.")
    relationship_type: str = Field(default="FOREIGN_KEY", description="Tipe relasi (misal, 'FOREIGN_KEY', 'JOIN_TABLE').")
```

**2.4. Contoh Request dan Response untuk `get_relevant_schema_info`**
*   **Request**:
    ```json
    {
      "intent": "sales_analysis",
      "entities": ["sales", "Januari 2023", "total_amount"]
    }
    ```
*   **Response**:
    ```json
    {
      "relevant_tables": [
        {
          "table_name": "sales_orders",
          "purpose": "Mencatat semua transaksi penjualan.",
          "columns": [
            {"name": "order_id", "type": "VARCHAR", "description": "ID unik order", "classification": "identifier", "is_aggregatable": false},
            {"name": "order_date", "type": "DATE", "description": "Tanggal order dibuat", "classification": "temporal", "is_aggregatable": false},
            {"name": "customer_id", "type": "VARCHAR", "description": "ID pelanggan", "classification": "identifier", "is_aggregatable": false},
            {"name": "total_amount", "type": "DECIMAL", "description": "Total nilai order", "classification": "financial_amount", "is_aggregatable": true}
          ]
        },
        {
          "table_name": "order_lines",
          "purpose": "Detail item per transaksi penjualan.",
          "columns": [
            {"name": "line_id", "type": "VARCHAR", "classification": "identifier"},
            {"name": "order_id", "type": "VARCHAR", "classification": "identifier"},
            {"name": "product_id", "type": "VARCHAR", "classification": "identifier"},
            {"name": "quantity", "type": "INTEGER", "classification": "quantitative", "is_aggregatable": true},
            {"name": "unit_price", "type": "DECIMAL", "classification": "financial_amount", "is_aggregatable": true}
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
      ],
      "financial_columns": {
        "sales_orders": ["total_amount"],
        "order_lines": ["quantity", "unit_price"]
      },
      "temporal_columns": {
        "sales_orders": ["order_date"]
      }
    }
    ```

---

**3. MCP Server untuk MySQL (`mysql_mcp_server`)**

**3.1. Deskripsi Umum**
`mysql_mcp_server` menyediakan antarmuka untuk mengeksekusi query SQL ke database MySQL ERP dan mengembalikan hasilnya. Keamanan dan efisiensi adalah prioritas utama.

**3.2. Tools yang Diekspos**

   **3.2.1. Tool: `execute_sql_query`**
    *   **Deskripsi**: Menjalankan satu atau serangkaian query SQL (dipisahkan `';'`) yang telah divalidasi dan aman ke database. Mengembalikan hasil dalam format terstruktur. Hanya query jenis `SELECT` yang diizinkan untuk MVP.
    *   **Input Parameters**:
        ```python
        class ExecuteSqlQueryInput(BaseModel):
            sql_queries: List[str] = Field(..., description="Satu atau lebih query SQL SELECT yang akan dieksekusi. Jika lebih dari satu, hasil akan dikembalikan sebagai list.")
            # max_rows: int = Field(default=1000, description="Jumlah maksimum baris yang akan dikembalikan per query untuk mencegah data besar.")
            # timeout_seconds: int = Field(default=30, description="Batas waktu eksekusi query.")
        ```
    *   **Output Structure**:
        ```python
        # (Struktur data ini akan didefinisikan di bagian 3.3)
        class QueryExecutionResult(BaseModel):
            query: str = Field(description="Query SQL yang dieksekusi.")
            status: str = Field(description="Status eksekusi ('success' atau 'error').")
            row_count: Optional[int] = Field(default=None, description="Jumlah baris yang dihasilkan.")
            column_names: Optional[List[str]] = Field(default=None, description="Nama-nama kolom hasil.")
            results: Optional[List[Dict[str, any]]] = Field(default=None, description="Hasil query sebagai list of dictionaries.")
            error_message: Optional[str] = Field(default=None, description="Pesan error jika eksekusi gagal.")
        
        class BatchQueryExecutionOutput(BaseModel):
            batch_results: List[QueryExecutionResult]
        ```

**3.3. Struktur Data (Pydantic Models) untuk `mysql_mcp_server`**
*(Struktur `QueryExecutionResult` dan `BatchQueryExecutionOutput` sudah didefinisikan di atas)*

**3.4. Contoh Request dan Response untuk `execute_sql_query`**
*   **Request**:
    ```json
    {
      "sql_queries": [
        "SELECT SUM(total_amount) AS total_sales FROM sales_orders WHERE order_date >= '2023-01-01' AND order_date <= '2023-01-31';",
        "SELECT COUNT(*) AS transaction_count FROM sales_orders WHERE order_date >= '2023-01-01' AND order_date <= '2023-01-31';"
      ]
    }
    ```
*   **Response**:
    ```json
    {
      "batch_results": [
        {
          "query": "SELECT SUM(total_amount) AS total_sales FROM sales_orders WHERE order_date >= '2023-01-01' AND order_date <= '2023-01-31';",
          "status": "success",
          "row_count": 1,
          "column_names": ["total_sales"],
          "results": [{"total_sales": 125000000.50}],
          "error_message": null
        },
        {
          "query": "SELECT COUNT(*) AS transaction_count FROM sales_orders WHERE order_date >= '2023-01-01' AND order_date <= '2023-01-31';",
          "status": "success",
          "row_count": 1,
          "column_names": ["transaction_count"],
          "results": [{"transaction_count": 456}],
          "error_message": null
        }
      ]
    }
    ```

---

**4. MCP Server untuk Placeholder System (`placeholder_mcp_server`)**

**4.1. Deskripsi Umum**
`placeholder_mcp_server` bertanggung jawab untuk mengisi *template* narasi dengan data aktual dan menerapkan aturan pemformatan yang sesuai. Ini memastikan LLM tidak memproses angka secara langsung.

**4.2. Tools yang Diekspos**

   **4.2.1. Tool: `fill_placeholders`**
    *   **Deskripsi**: Mengganti semua placeholder dalam string template dengan nilai-nilai aktual dari dictionary data, dan menerapkan aturan pemformatan yang ditentukan.
    *   **Input Parameters**:
        ```python
        class FormattingRule(BaseModel):
            type: str = Field(description="Tipe pemformatan, misal 'currency_IDR', 'number_with_separator', 'date_DD_MMM_YYYY'.")
            # precision: Optional[int] = Field(default=None, description="Untuk angka, jumlah digit desimal.")

        class FillPlaceholdersInput(BaseModel):
            response_template: str = Field(..., description="String template dengan placeholder, misal 'Total penjualan: {TOTAL_SALES}'.")
            data_values: Dict[str, any] = Field(..., description="Dictionary berisi nilai aktual untuk setiap placeholder.")
            formatting_rules: Dict[str, FormattingRule] = Field(default_factory=dict, description="Dictionary aturan pemformatan per placeholder. Key adalah nama placeholder.")
        ```
    *   **Output Structure**:
        ```python
        class FillPlaceholdersOutput(BaseModel):
            final_narrative: str = Field(description="Narasi final setelah placeholder diisi dan diformat.")
        ```

**4.3. Struktur Data (Pydantic Models) untuk `placeholder_mcp_server`**
*(Struktur `FormattingRule`, `FillPlaceholdersInput`, dan `FillPlaceholdersOutput` sudah didefinisikan di atas)*

**4.4. Contoh Request dan Response untuk `fill_placeholders`**
*   **Request**:
    ```json
    {
      "response_template": "Laporan Penjualan {PERIOD_LABEL}:\n- Total Penjualan: {TOTAL_SALES_VALUE}\n- Jumlah Transaksi: {TRANSACTION_COUNT_VALUE} transaksi",
      "data_values": {
        "PERIOD_LABEL": "Januari 2023",
        "TOTAL_SALES_VALUE": 125000000.50,
        "TRANSACTION_COUNT_VALUE": 456
      },
      "formatting_rules": {
        "TOTAL_SALES_VALUE": {"type": "currency_IDR", "precision": 2},
        "TRANSACTION_COUNT_VALUE": {"type": "number_with_separator"}
      }
    }
    ```
*   **Response**:
    ```json
    {
      "final_narrative": "Laporan Penjualan Januari 2023:\n- Total Penjualan: Rp 125.000.000,50\n- Jumlah Transaksi: 456 transaksi"
    }
    ```

---