# backend/mcp_servers/mysql_server/main.py

import os
import sys # Tambahkan ini untuk debug_print jika diperlukan
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import mysql.connector 

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context as MCPContext # Impor Context jika akan digunakan di tool

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
dotenv_path = os.path.join(project_root, 'backend', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

def debug_print(*args, **kwargs): # Fungsi helper untuk print ke stderr
    other_kwargs = {k: v for k, v in kwargs.items() if k != 'file'}
    print(*args, file=sys.stderr, **other_kwargs)

# Pydantic models (tetap sama)
class ExecuteSqlQueryInput(BaseModel):
    sql_queries: List[str] = Field(..., description="Satu atau lebih query SQL SELECT yang akan dieksekusi.")

class QueryExecutionResultItem(BaseModel):
    query: str = Field(description="Query SQL yang dieksekusi.")
    status: str = Field(description="Status eksekusi ('success' atau 'error').")
    row_count: Optional[int] = Field(default=None, description="Jumlah baris yang dihasilkan.")
    column_names: Optional[List[str]] = Field(default=None, description="Nama-nama kolom hasil.")
    results: Optional[List[Dict[str, Any]]] = Field(default=None, description="Hasil query sebagai list of dictionaries.")
    error_message: Optional[str] = Field(default=None, description="Pesan error jika eksekusi gagal.")

class BatchQueryExecutionOutput(BaseModel):
    batch_results: List[QueryExecutionResultItem]

# Inisialisasi MCP Server
mcp = FastMCP( 
    name="MySQLQueryServer",
    title="MySQL Query Execution Server",
    description="Server untuk mengeksekusi query SQL SELECT ke database MySQL."
)

# Konfigurasi koneksi database
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_PORT = int(os.getenv("MYSQL_PORT", 3306))


def get_db_connection():
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        error_msg = "Database connection details (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE) not fully configured in .env"
        debug_print(f"Connection Error: {error_msg}", file=sys.stderr)
        raise ConnectionError(error_msg)
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        debug_print(f"Successfully created MySQL connection to {DB_HOST}:{DB_PORT}/{DB_NAME}", file=sys.stderr)
        return conn
    except mysql.connector.Error as err:
        debug_print(f"Error connecting to MySQL: {err}", file=sys.stderr)
        raise ConnectionError(f"Failed to connect to MySQL: {err}") from err


@mcp.tool()
def execute_sql_query(ctx: MCPContext, payload: ExecuteSqlQueryInput) -> BatchQueryExecutionOutput:
    """
    Mengeksekusi satu atau serangkaian query SQL SELECT yang aman ke database MySQL.
    Mengembalikan hasil dalam format terstruktur. Hanya query SELECT yang diizinkan.

    Args:
        ctx: Konteks MCP. (Digunakan untuk logging internal tool jika diperlukan via ctx.info(), ctx.error())
        payload (ExecuteSqlQueryInput): Objek input yang berisi:
            sql_queries (List[str]): Daftar string query SQL SELECT yang akan dieksekusi.
                                     Contoh: ["SELECT * FROM sales_orders WHERE order_date = '2023-01-15'",
                                              "SELECT COUNT(*) FROM customers"]

    Returns:
        BatchQueryExecutionOutput: Objek output yang berisi daftar hasil eksekusi untuk setiap query.

    Contoh Penggunaan oleh Agent (dalam format pemanggilan tool):
    ```json
    {
        "tool_name": "execute_sql_query",
        "payload": {
            "sql_queries": [
                "SELECT customer_name, total_amount FROM sales_orders WHERE order_date >= '2023-01-01' AND order_date <= '2023-01-31' ORDER BY total_amount DESC LIMIT 5;",
                "SELECT SUM(total_amount) AS total_jan_sales FROM sales_orders WHERE order_date >= '2023-01-01' AND order_date <= '2023-01-31';"
            ]
        }
    }
    ```
    """
    batch_results: List[QueryExecutionResultItem] = []
    conn = None
    cursor = None # Definisikan cursor di sini agar bisa diakses di finally
    
    ctx.info(f"Executing execute_sql_query tool with {len(payload.sql_queries)} queries.")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) 

        for sql_query in payload.sql_queries:
            # Validasi dasar
            if not sql_query.strip().upper().startswith("SELECT"):
                error_msg = "Only SELECT queries are allowed."
                ctx.warning(f"Query rejected: '{sql_query}'. Reason: {error_msg}")
                batch_results.append(QueryExecutionResultItem(
                    query=sql_query,
                    status="error",
                    error_message=error_msg
                ))
                continue
            
            try:
                ctx.info(f"Executing SQL: {sql_query}")
                cursor.execute(sql_query)
                
                query_results = cursor.fetchall() 
                
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []
                row_count = len(query_results) if query_results is not None else 0
                ctx.info(f"Query '{sql_query}' executed successfully. Rows: {row_count}, Columns: {column_names}")

                batch_results.append(QueryExecutionResultItem(
                    query=sql_query,
                    status="success",
                    row_count=row_count,
                    column_names=column_names,
                    results=query_results
                ))
            except mysql.connector.Error as err:
                error_msg = str(err)
                ctx.error(f"Error executing query '{sql_query}': {error_msg}")
                batch_results.append(QueryExecutionResultItem(
                    query=sql_query,
                    status="error",
                    error_message=error_msg
                ))
            except Exception as e: 
                error_msg = f"An unexpected error occurred: {str(e)}"
                ctx.error(f"Unexpected error executing query '{sql_query}': {error_msg}")
                batch_results.append(QueryExecutionResultItem(
                    query=sql_query,
                    status="error",
                    error_message=error_msg
                ))
        
    except ConnectionError as conn_err: 
        error_msg = f"Database connection failed: {str(conn_err)}"
        ctx.error(error_msg)
        for sql_query in payload.sql_queries:
            if not any(res.query == sql_query for res in batch_results): # Hindari duplikasi error message per query
                batch_results.append(QueryExecutionResultItem(
                    query=sql_query,
                    status="error",
                    error_message=error_msg
                ))
    except Exception as e:
        error_msg = f"General error in execute_sql_query: {str(e)}"
        ctx.error(error_msg)
        if not batch_results: # Jika belum ada hasil sama sekali, isi semua dengan error ini
             for sql_query in payload.sql_queries:
                batch_results.append(QueryExecutionResultItem(
                    query=sql_query,
                    status="error",
                    error_message=error_msg
                ))
    finally:
        if cursor:
            cursor.close()
            debug_print("MySQL cursor closed.", file=sys.stderr)
        if conn and conn.is_connected():
            conn.close()
            debug_print("MySQL connection closed.", file=sys.stderr)
            
    return BatchQueryExecutionOutput(batch_results=batch_results)


if __name__ == "__main__":
    debug_print("Starting MySQL MCP Server for development...", file=sys.stderr)
    debug_print(f"Attempting to use DB: host={DB_HOST}, user={DB_USER}, db={DB_NAME}, port={DB_PORT}", file=sys.stderr)
    try:
        conn_test = get_db_connection()
        if conn_test.is_connected():
            debug_print("Successfully connected to MySQL for initial check.", file=sys.stderr)
            conn_test.close()
        else:
            debug_print("Failed to connect to MySQL for initial check.", file=sys.stderr)
    except ConnectionError as e:
        debug_print(f"Initial DB connection check failed: {e}", file=sys.stderr)
    
    mcp.run()