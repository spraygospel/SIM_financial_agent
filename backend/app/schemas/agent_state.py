# backend/app/schemas/agent_state.py
from typing import TypedDict, List, Dict, Any, Optional, Union

# Definisi sub-TypedDict untuk struktur yang lebih kompleks dalam AgentState
class TimePeriod(TypedDict, total=False): # total=False membuat semua field opsional by default
    start_date: str
    end_date: str
    period_label: str

class MCPToolCallLog(TypedDict, total=False):
    server_name: str
    tool_name: str
    request_payload: Dict[str, Any]
    response_payload: Optional[Dict[str, Any]] 
    status: str # 'success' atau 'error'
    error_message: Optional[str] 
    timestamp: str

# === DEFINISI BARU UNTUK DATABASE OPERATION PLAN ===
class SelectColumn(TypedDict, total=False):
    field_name: str       
    alias: Optional[str]  
    aggregation: Optional[str] 
    is_expression: Optional[bool] 

class JoinCondition(TypedDict, total=False): 
    left_table_field: str  
    right_table_field: str 

class JoinClause(TypedDict, total=False):
    target_table: str
    type: str  
    on_conditions: List[JoinCondition] 

class FilterCondition(TypedDict, total=False):
    field_or_expression: str 
    operator: str  
    value: Any     

class LogicalFilterGroup(TypedDict, total=False): 
    logical_operator: str 
    conditions: List[Union['LogicalFilterGroup', FilterCondition]] 

class OrderByClause(TypedDict, total=False):
    field_or_expression: str 
    direction: str    

class DatabaseOperation(TypedDict, total=False):
    operation_id: str 
    operation_type: str 
    purpose: str
    
    main_table: str
    select_columns: List[SelectColumn]
    joins: Optional[List[JoinClause]]
    
    filters: Optional[Union[List[FilterCondition], LogicalFilterGroup]]
    
    group_by_columns: Optional[List[str]] 
    having_conditions: Optional[Union[List[FilterCondition], LogicalFilterGroup]] 
    order_by_clauses: Optional[List[OrderByClause]]
    limit: Optional[int]
    offset: Optional[int] 
    
    result_key: str 
    expected_result_format: Optional[str] 
# === AKHIR DEFINISI BARU ===

# Model Pydantic dari MCP server (bisa diimpor jika sudah ada dan sesuai)
# Atau kita definisikan ulang struktur yang diharapkan dari MCP Server response di sini
# Untuk kesederhanaan, kita gunakan Dict[str, Any] untuk relevant_tables dan table_relationships
# dari MCP Graphiti, dan Dict[str, Any] untuk hasil dari MCP MySQL.

class TableSchemaFromMCP(TypedDict, total=False): # Merepresentasikan satu tabel dari RelevantSchemaOutput
    table_name: str
    purpose: str # Tambahkan ini dari Graphiti semantic mapping
    business_category: Optional[str] # Tambahkan ini
    columns: List[Dict[str, Any]] # List dari ColumnMcp

class RelationshipFromMCP(TypedDict, total=False): # Merepresentasikan satu relasi dari RelevantSchemaOutput
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    relationship_type: str

class AgentState(TypedDict, total=False): # total=False membuat semua field opsional by default
    # Input Awal & Konteks Sesi
    user_query: str # Wajib ada di awal
    session_id: str # Wajib ada di awal
    conversation_history: List[Dict[str, str]]
    
    # Hasil dari `understand_query`
    intent: Optional[str] # Dibuat opsional karena bisa gagal
    entities_mentioned: Optional[List[str]]
    time_period: Optional[TimePeriod]
    requested_metrics: Optional[List[str]]
    query_complexity: Optional[str] # 'simple', 'medium', 'complex'

    # Hasil dari `consult_schema`
    relevant_tables: Optional[List[TableSchemaFromMCP]] # Diperbarui tipenya
    table_relationships: Optional[List[RelationshipFromMCP]] # Diperbarui tipenya
    financial_columns: Optional[Dict[str, List[str]]]
    temporal_columns: Optional[Dict[str, List[str]]]
    schema_consultation_warnings: Optional[List[str]]

    # --- PERUBAHAN DI SINI ---
    # HAPUS field-field ini:
    # sql_queries_plan: List[SqlQueryPlan] 
    # raw_data_query_plan: SqlQueryPlan

    # TAMBAHKAN field-field ini:
    database_operations_plan: Optional[List[DatabaseOperation]] # Untuk query agregasi/kalkulasi
    raw_data_operation_plan: Optional[DatabaseOperation] # Khusus untuk mengambil data mentah
    # --- AKHIR PERUBAHAN ---
    
    response_template: Optional[str] # Tetap ada, dihasilkan oleh plan_execution
    placeholder_mapping: Optional[Dict[str, Dict[str, Any]]] # Key: placeholder, Value: {type, precision, label}
    validation_rules_for_results: Optional[List[Dict[str, Any]]]
    data_source_info: Optional[Dict[str, Any]] # Dipindahkan ke sini, dihasilkan oleh plan_execution

    # Hasil dari `execute_query`
    financial_calculations: Optional[Dict[str, Any]] 
    raw_query_results: Optional[List[Dict[str, Any]]] 
    query_execution_status: Optional[str] # 'success', 'partial_failure', 'total_failure', 'no_operations_planned'
    query_execution_errors: Optional[List[Dict[str, str]]]

    # Hasil dari `validate_results`
    data_quality_checks: Optional[Dict[str, Any]]
    validation_warnings: Optional[List[str]]
    validation_status: Optional[str] # 'passed', 'passed_with_warnings', 'failed_critical', 'failed_no_data'
    quality_score: Optional[int] # 0-100

    # Hasil dari `replace_placeholders` (Output Final untuk API)
    final_narrative: Optional[str]
    data_table_for_display: Optional[List[Dict[str, Any]]]
    executive_summary: Optional[List[Dict[str, str]]] 
    warnings_for_display: Optional[List[str]]

    # Logging dan Status Internal
    current_node_name: Optional[str]
    error_message_for_user: Optional[str] 
    technical_error_details: Optional[str]
    mcp_tool_call_history: Optional[List[MCPToolCallLog]]
    workflow_status: Optional[str] # 'processing', 'completed', 'error'