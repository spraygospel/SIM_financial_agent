# backend/app/langgraph_workflow/nodes/execute_query.py
from typing import Dict, Any, List, Optional, Union, Tuple # Tambah Union dan Tuple
import sys
import mysql.connector 
from datetime import datetime

from backend.app.schemas.agent_state import AgentState, DatabaseOperation, MCPToolCallLog, SelectColumn, JoinClause, JoinCondition, FilterCondition, LogicalFilterGroup, OrderByClause # Impor semua yang baru
from backend.app.core.config import settings


def get_db_connection_for_node():
    if not all([settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME]):
        error_msg = "MySQL DB connection details (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) not fully configured in settings."
        print(f"ERROR in get_db_connection_for_node: {error_msg}", file=sys.stderr)
        raise ConnectionError(error_msg)
    try:
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT
        )
        print(f"execute_query_node: Successfully created MySQL connection to {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}", file=sys.stderr)
        return conn
    except mysql.connector.Error as err:
        print(f"execute_query_node: Error connecting to MySQL: {err}", file=sys.stderr)
        raise ConnectionError(f"Failed to connect to MySQL: {err}") from err

# --- FUNGSI BARU UNTUK MEMBANGUN SQL ---
def _build_sql_from_operation(plan: DatabaseOperation, db_type: str = "mysql") -> Tuple[str, Tuple[Any, ...]]:
    if not plan.get("main_table") or not plan.get("select_columns"):
        raise ValueError("Rencana operasi tidak valid: 'main_table' dan 'select_columns' wajib ada.")

    sql_parts: List[str] = ["SELECT"]
    sql_params: List[Any] = []

    # SELECT columns
    select_column_fragments: List[str] = []
    for col_spec_dict in plan["select_columns"]:
        col_spec = SelectColumn(**col_spec_dict) if isinstance(col_spec_dict, dict) else col_spec_dict
        
        field_name_or_expr = col_spec.get('field_name', '*')
        # Di sini kita asumsikan field_name_or_expr sudah aman atau merupakan nama kolom valid
        # Tidak ada sanitasi identifier dilakukan di sini untuk MVP, bergantung pada LLM yang terkontrol
        
        fragment = field_name_or_expr
        if col_spec.get('aggregation'):
            agg_func = col_spec['aggregation'].upper()
            allowed_aggregations = ["SUM", "COUNT", "AVG", "MIN", "MAX", "COUNT_DISTINCT"]
            if agg_func not in allowed_aggregations:
                raise ValueError(f"Agregasi tidak diizinkan: {agg_func}")
            
            if agg_func == "COUNT_DISTINCT":
                fragment = f"COUNT(DISTINCT {field_name_or_expr})"
            else:
                fragment = f"{agg_func}({field_name_or_expr})"
        
        if col_spec.get('alias'):
            # Asumsi alias aman
            fragment += f" AS `{col_spec['alias']}`" # Gunakan backtick untuk alias jika mengandung spasi/keyword
        select_column_fragments.append(fragment)
    
    sql_parts.append(", ".join(select_column_fragments) if select_column_fragments else "*")

    # FROM clause
    # Asumsi main_table aman
    sql_parts.append(f"FROM `{plan['main_table']}`")

    # JOIN clauses
    if plan.get("joins"):
        for join_spec_dict in plan["joins"]:
            join_spec = JoinClause(**join_spec_dict) if isinstance(join_spec_dict, dict) else join_spec_dict
            join_type = join_spec.get("type", "INNER").upper()
            if join_type not in ["INNER", "LEFT", "RIGHT", "FULL OUTER"]:
                raise ValueError(f"Tipe JOIN tidak valid: {join_type}")
            
            # Asumsi target_table aman
            join_fragment = f" {join_type} JOIN `{join_spec['target_table']}` ON "
            
            on_conditions_str_list: List[str] = []
            if not join_spec.get("on_conditions"):
                 raise ValueError(f"Join ke tabel {join_spec['target_table']} tidak memiliki ON condition.")

            for cond_dict in join_spec["on_conditions"]:
                # Asumsi field aman
                on_conditions_str_list.append(f"`{cond_dict['left_table_field'].replace('.', '`.`')}` = `{cond_dict['right_table_field'].replace('.', '`.`')}`")
            
            join_fragment += " AND ".join(on_conditions_str_list)
            sql_parts.append(join_fragment)

    # WHERE clause (dan HAVING, karena logikanya sama)
    def build_filter_logic(filter_input: Union[List[FilterCondition], LogicalFilterGroup, None], params_list: list) -> str:
        if not filter_input:
            return ""

        conditions_str_list: List[str] = []
        
        current_logical_operator = "AND" # Default untuk list FilterCondition

        if isinstance(filter_input, dict) and filter_input.get("logical_operator") and filter_input.get("conditions"):
            lg_filter_group = LogicalFilterGroup(**filter_input) if isinstance(filter_input, dict) else filter_input
            current_logical_operator = lg_filter_group.get("logical_operator", "AND").upper()
            if current_logical_operator not in ["AND", "OR"]:
                raise ValueError(f"Operator logika filter tidak valid: {current_logical_operator}")
            
            conditions_to_process = lg_filter_group.get("conditions", [])
        elif isinstance(filter_input, list):
            conditions_to_process = filter_input # Ini adalah list FilterCondition
        else:
            raise ValueError(f"Struktur filter input tidak valid: {type(filter_input)}")

        for cond_item_dict in conditions_to_process:
            if isinstance(cond_item_dict, dict) and cond_item_dict.get("logical_operator"): # Nested LogicalFilterGroup
                nested_clause = build_filter_logic(cond_item_dict, params_list)
                if nested_clause:
                    conditions_str_list.append(f"({nested_clause})")
            elif isinstance(cond_item_dict, dict): # Ini adalah FilterCondition
                fc = FilterCondition(**cond_item_dict) if isinstance(cond_item_dict, dict) else cond_item_dict
                
                field_or_expr = fc.get("field_or_expression")
                operator = fc.get("operator", "").upper()
                value = fc.get("value") # Bisa None jika operator IS NULL / IS NOT NULL

                if not field_or_expr or not operator:
                    raise ValueError(f"FilterCondition tidak lengkap: {fc}")

                # Asumsi field_or_expr aman
                field_ref = f"`{field_or_expr.replace('.', '`.`')}`" if '.' in field_or_expr and not fc.get('is_expression') else field_or_expr

                allowed_ops_value_as_param = ["=", "!=", ">", "<", ">=", "<=", "LIKE", "NOT LIKE"]
                allowed_ops_value_in_query = ["IS NULL", "IS NOT NULL"]
                allowed_ops_value_list = ["IN", "NOT IN"]
                allowed_ops_value_tuple_for_between = ["BETWEEN"]

                if operator in allowed_ops_value_as_param:
                    conditions_str_list.append(f"{field_ref} {operator} %s")
                    params_list.append(value)
                elif operator in allowed_ops_value_in_query:
                    conditions_str_list.append(f"{field_ref} {operator}")
                elif operator in allowed_ops_value_list:
                    if not isinstance(value, list) or not value:
                        raise ValueError(f"Operator {operator} memerlukan value berupa list yang tidak kosong.")
                    placeholders = ", ".join(["%s"] * len(value))
                    conditions_str_list.append(f"{field_ref} {operator} ({placeholders})")
                    params_list.extend(value)
                elif operator in allowed_ops_value_tuple_for_between:
                    if not isinstance(value, (list, tuple)) or len(value) != 2:
                        raise ValueError(f"Operator {operator} memerlukan value berupa list/tuple dengan 2 elemen.")
                    conditions_str_list.append(f"{field_ref} {operator} %s AND %s")
                    params_list.extend(value)
                else:
                    raise ValueError(f"Operator filter tidak diizinkan atau tidak dikenal: {operator}")
            else:
                raise ValueError(f"Struktur kondisi filter tidak valid: {cond_item_dict}")
        
        return f" {current_logical_operator} ".join(conditions_str_list) if conditions_str_list else ""

    where_clause_str = build_filter_logic(plan.get("filters"), sql_params)
    if where_clause_str:
        sql_parts.append(f"WHERE {where_clause_str}")

    # GROUP BY clause
    if plan.get("group_by_columns"):
        # Asumsi kolom aman
        group_by_cols_sanitized = [f"`{col.replace('.', '`.`')}`" if '.' in col else col for col in plan["group_by_columns"]]
        sql_parts.append(f"GROUP BY {', '.join(group_by_cols_sanitized)}")

    # HAVING clause
    having_clause_str = build_filter_logic(plan.get("having_conditions"), sql_params)
    if having_clause_str:
        sql_parts.append(f"HAVING {having_clause_str}")

    # ORDER BY clause
    if plan.get("order_by_clauses"):
        order_fragments: List[str] = []
        for ob_spec_dict in plan["order_by_clauses"]:
            ob_spec = OrderByClause(**ob_spec_dict) if isinstance(ob_spec_dict, dict) else ob_spec_dict
            # Asumsi field aman
            field_ref_ob = f"`{ob_spec['field_or_expression'].replace('.', '`.`')}`" if '.' in ob_spec['field_or_expression'] and not ob_spec.get('is_expression') else ob_spec['field_or_expression']
            direction = ob_spec.get("direction", "ASC").upper()
            if direction not in ["ASC", "DESC"]:
                raise ValueError(f"Arah ORDER BY tidak valid: {direction}")
            order_fragments.append(f"{field_ref_ob} {direction}")
        if order_fragments:
            sql_parts.append(f"ORDER BY {', '.join(order_fragments)}")

    # LIMIT clause
    limit_val = plan.get("limit")
    if limit_val is not None: 
        if not isinstance(limit_val, int) or limit_val < 0:
            raise ValueError("LIMIT harus integer non-negatif.")
        sql_parts.append("LIMIT %s")
        sql_params.append(limit_val)
    
    offset_val = plan.get("offset")
    if offset_val is not None:
        if not isinstance(offset_val, int) or offset_val < 0:
            raise ValueError("OFFSET harus integer non-negatif.")
        if limit_val is None: 
            raise ValueError("OFFSET memerlukan LIMIT.")
        sql_parts.append("OFFSET %s")
        sql_params.append(offset_val)

    final_sql = " ".join(sql_parts) + ";"
    return final_sql, tuple(sql_params)
# --- AKHIR FUNGSI BARU ---

async def execute_query_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: execute_query_node (Refactored for DatabaseOperationPlan) ---", file=sys.stderr)
    
    db_ops_plan_list: List[DatabaseOperation] = state.get("database_operations_plan", [])
    raw_data_op_plan: Optional[DatabaseOperation] = state.get("raw_data_operation_plan")
    current_mcp_history: List[MCPToolCallLog] = state.get("mcp_tool_call_history", [])

    financial_calculations: Dict[str, Any] = {}
    raw_query_results_list: Optional[List[Dict[str, Any]]] = None 
    query_execution_status = "success"
    query_execution_errors: List[Dict[str, str]] = []

    all_operations_to_execute: List[DatabaseOperation] = []
    if db_ops_plan_list: # Pastikan ini list sebelum extend
        all_operations_to_execute.extend(db_ops_plan_list)
    if raw_data_op_plan and isinstance(raw_data_op_plan, dict):
        all_operations_to_execute.append(raw_data_op_plan)

    if not all_operations_to_execute:
        print("execute_query_node: No DatabaseOperations to execute.", file=sys.stderr)
        return {
            "financial_calculations": financial_calculations,
            "raw_query_results": raw_query_results_list,
            "query_execution_status": "no_operations_planned",
            "query_execution_errors": [{"operation_id": "N/A", "error": "No DatabaseOperations planned"}],
            "current_node_name": "execute_query",
            "mcp_tool_call_history": current_mcp_history
        }

    conn = None
    cursor = None
    
    batch_mcp_log_entry: MCPToolCallLog = { # type: ignore
        "server_name": "mysql_direct_db_call_parameterized",
        "tool_name": "execute_database_operations_batch_inline",
        "request_payload": {"operations_summary": [op.get("purpose", "N/A") for op in all_operations_to_execute]}, # Lebih ringkas
        "response_payload": {"batch_results": []},
        "status": "processing",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        conn = get_db_connection_for_node()
        
        total_ops = len(all_operations_to_execute)
        successful_ops = 0

        for op_plan_dict in all_operations_to_execute:
            op_plan = DatabaseOperation(**op_plan_dict) if isinstance(op_plan_dict, dict) else op_plan_dict

            operation_id = op_plan.get("operation_id", f"unknown_op_{datetime.now().timestamp()}")
            purpose = op_plan.get("purpose", "N/A")
            result_key = op_plan.get("result_key")
            expected_format = op_plan.get("expected_result_format")

            if not result_key:
                err_msg_plan = "Rencana operasi tidak valid (tidak ada result_key)."
                print(f"execute_query_node: {err_msg_plan} Detail: {op_plan}", file=sys.stderr)
                query_execution_errors.append({"operation_id": operation_id, "error": err_msg_plan})
                if batch_mcp_log_entry["response_payload"] is not None: # type: ignore
                    batch_mcp_log_entry["response_payload"]["batch_results"].append({ # type: ignore
                        "operation_id": operation_id, "status": "error", "error_message": err_msg_plan
                    })
                continue
            
            generated_sql = ""
            generated_params: Tuple[Any, ...] = tuple()
            try:
                generated_sql, generated_params = _build_sql_from_operation(op_plan)
                print(f"execute_query_node: Built SQL for OpID '{operation_id}' (Purpose: {purpose}): {generated_sql} WITH PARAMS: {generated_params}", file=sys.stderr)
                
                cursor = conn.cursor(dictionary=True)
                cursor.execute(generated_sql, generated_params)
                results = cursor.fetchall()
                cursor.close() 
                cursor = None

                if result_key == "RAW_DATA_TABLE":
                    raw_query_results_list = results
                    print(f"execute_query_node: Stored {len(results) if results else 0} rows for RAW_DATA_TABLE.", file=sys.stderr)
                # JIKA BUKAN RAW_DATA_TABLE, MAKA ITU UNTUK financial_calculations
                elif result_key: # Pastikan result_key ada sebelum digunakan untuk financial_calculations
                    if expected_format == "single_value":
                        if results and len(results) == 1 and results[0] and len(results[0]) == 1:
                            single_value = list(results[0].values())[0]
                            financial_calculations[result_key] = single_value
                            print(f"execute_query_node: Stored single value for {result_key}: {single_value}", file=sys.stderr)
                        elif not results: 
                            financial_calculations[result_key] = None 
                            print(f"execute_query_node: No results for {result_key} (expected single_value), stored None.", file=sys.stderr)
                        else: 
                            # Jika expected single_value tapi hasil tidak sesuai, bisa jadi error atau simpan apa adanya dengan warning
                            financial_calculations[result_key] = results # Simpan list of dicts
                            print(f"WARNING: OpID '{operation_id}' expected 'single_value' tapi dapat {len(results)} baris / {len(results[0]) if results else 0} kolom. Stored as list of dicts for {result_key}.", file=sys.stderr)
                    elif expected_format == "list_of_dicts":
                        financial_calculations[result_key] = results if results else []
                        print(f"execute_query_node: Stored list of dicts for {result_key} ({len(results) if results else 0} items).", file=sys.stderr)
                    else: # Format tidak diketahui atau tidak 'single_value'/'list_of_dicts'
                        financial_calculations[result_key] = results if results else None # Default ke None jika tidak ada hasil
                        print(f"execute_query_node: Stored results for {result_key} (format: {expected_format if expected_format else 'N/A'}, {len(results) if results else 0} items).", file=sys.stderr)
                else:
                    print(f"WARNING: OpID '{operation_id}' tidak memiliki result_key yang valid. Hasil tidak disimpan.", file=sys.stderr)


                if batch_mcp_log_entry["response_payload"] is not None: # type: ignore
                    batch_mcp_log_entry["response_payload"]["batch_results"].append({ # type: ignore
                         "operation_id": operation_id, "generated_sql": generated_sql, "status": "success", "row_count": len(results) if results else 0
                    })
                successful_ops += 1

            except (mysql.connector.Error, ValueError) as err_exec_build: # Tangkap ValueError dari _build_sql_from_operation
                error_type = "DB_ERROR" if isinstance(err_exec_build, mysql.connector.Error) else "SQL_BUILD_ERROR"
                error_msg_detail = f"{error_type} for OpID '{operation_id}' (SQL Attempted: {generated_sql if generated_sql else 'Build Failed'}): {err_exec_build}"
                print(error_msg_detail, file=sys.stderr)
                query_execution_errors.append({"operation_id": operation_id, "sql_attempted": generated_sql, "error": str(err_exec_build)})
                financial_calculations[result_key] = f"ERROR_{error_type}: {str(err_exec_build)}"
                if batch_mcp_log_entry["response_payload"] is not None: # type: ignore
                    batch_mcp_log_entry["response_payload"]["batch_results"].append({ # type: ignore
                        "operation_id": operation_id, "generated_sql": generated_sql, "status": "error", "error_message": str(err_exec_build)
                    })

        if total_ops > 0:
            if successful_ops == total_ops:
                query_execution_status = "success"
                batch_mcp_log_entry["status"] = "success"
            elif successful_ops > 0:
                query_execution_status = "partial_failure"
                batch_mcp_log_entry["status"] = "partial_failure"
                batch_mcp_log_entry["error_message"] = "Some operations failed."
            else:
                query_execution_status = "total_failure"
                batch_mcp_log_entry["status"] = "error"
                batch_mcp_log_entry["error_message"] = "All operations failed."
        else: # Tidak ada operasi untuk dijalankan, sudah ditangani di awal
            query_execution_status = "no_operations_planned"
            batch_mcp_log_entry["status"] = "no_operations_planned"

    except ConnectionError as conn_err:
        error_msg_conn = f"MySQL DB connection failed in execute_query_node: {str(conn_err)}"
        print(error_msg_conn, file=sys.stderr)
        query_execution_status = "total_failure"
        query_execution_errors.append({"operation_id": "DB_Connection", "error": str(conn_err)})
        batch_mcp_log_entry["status"] = "error"
        batch_mcp_log_entry["error_message"] = str(conn_err)
        for op_plan_dict_err in all_operations_to_execute: # Tandai semua hasil error
            op_plan_err = DatabaseOperation(**op_plan_dict_err) if isinstance(op_plan_dict_err, dict) else op_plan_dict_err
            if op_plan_err.get("result_key"):
                financial_calculations[op_plan_err["result_key"]] = f"ERROR_CONN: {str(conn_err)}"
    except Exception as e:
        error_msg_gen = f"General error in execute_query_node (Parameterized logic): {str(e)}"
        print(error_msg_gen, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        query_execution_status = "total_failure"
        query_execution_errors.append({"operation_id": "General_Node_Error", "error": str(e)})
        batch_mcp_log_entry["status"] = "error"
        batch_mcp_log_entry["error_message"] = str(e)
        for op_plan_dict_err_gen in all_operations_to_execute: # Tandai semua hasil error
            op_plan_err_gen = DatabaseOperation(**op_plan_dict_err_gen) if isinstance(op_plan_dict_err_gen, dict) else op_plan_dict_err_gen
            if op_plan_err_gen.get("result_key"):
                financial_calculations[op_plan_err_gen["result_key"]] = f"ERROR_NODE: {str(e)}"
    finally:
        if cursor:
            cursor.close()
            print("execute_query_node: Final MySQL cursor closed in finally block.", file=sys.stderr)
        if conn and conn.is_connected():
            conn.close()
            print("execute_query_node: MySQL connection closed in finally block.", file=sys.stderr)

    current_mcp_history.append(batch_mcp_log_entry)

    return {
        "financial_calculations": financial_calculations,
        "raw_query_results": raw_query_results_list,
        "query_execution_status": query_execution_status,
        "query_execution_errors": query_execution_errors,
        "current_node_name": "execute_query",
        "mcp_tool_call_history": current_mcp_history
    }