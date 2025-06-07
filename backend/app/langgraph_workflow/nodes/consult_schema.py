# backend/app/langgraph_workflow/nodes/consult_schema.py
from typing import Dict, Any, List, Optional
import sys
import httpx 
from pydantic import BaseModel, Field
from neo4j import AsyncGraphDatabase, AsyncSession, AsyncManagedTransaction, AsyncDriver
from neo4j import exceptions as neo4j_exceptions
from datetime import datetime

from backend.app.schemas.agent_state import AgentState
from backend.app.core.config import settings

# --- Pydantic Models untuk payload dan respons MCP tool (Lokal) ---
class GetRelevantSchemaInfoInputForClient(BaseModel): 
    intent: str 
    entities: List[str]

class ColumnMcpForClient(BaseModel): 
    name: str 
    type: Optional[str] = None
    description: Optional[str] = None
    classification: Optional[str] = None
    is_aggregatable: Optional[bool] = None

class TableSchemaMcpForClient(BaseModel): 
    table_name: str 
    purpose: Optional[str] = None
    columns: List[ColumnMcpForClient] = Field(...)

class RelationshipMcpForClient(BaseModel): 
    from_table: str 
    from_column: str 
    to_table: str 
    to_column: str 
    relationship_type: str = Field(default="FOREIGN_KEY")

class RelevantSchemaOutputFromMCP(BaseModel): 
    relevant_tables: List[TableSchemaMcpForClient]
    table_relationships: List[RelationshipMcpForClient]
    success: bool = True
    error: Optional[str] = None
# --- Akhir Pydantic Models ---

# Pemetaan sederhana dari entitas generik NLU ke nama tabel aktual
# Ini bisa diperluas atau dibuat lebih dinamis nanti
ENTITY_TO_TABLE_MAP = {
    "sales_orders": ["salesorderh", "salesorderd"],
    "sales": ["salesorderh", "salesorderd", "salesinvoiceh", "salesinvoiced", "arbook"], # Ditambah arbook
    "customers": ["mastercustomer"],
    "pelanggan": ["mastercustomer"],
    "products": ["mastermaterial"],
    "produk": ["mastermaterial"],
    "inventory_adjustments": ["adjustinh", "adjustind", "adjustouth", "adjustoutd"],
    "adjustments": ["adjustinh", "adjustind", "adjustouth", "adjustoutd"],
    "penjualan": ["salesorderh", "salesorderd", "salesinvoiceh", "salesinvoiced", "arbook"], # Ditambah arbook
    "faktur_penjualan": ["salesinvoiceh", "salesinvoiced", "arbook"], # Ditambah arbook
    "sales_invoices": ["salesinvoiceh", "salesinvoiced", "arbook"], # Ditambah arbook
    
    # --- TAMBAHAN PENTING UNTUK PIUTANG ---
    "payments": ["customerpaymenth", "customerpaymentd", "arbook", "cashierreceipth", "cashierreceiptd"], # Tabel terkait pembayaran customer
    "pembayaran": ["customerpaymenth", "customerpaymentd", "arbook", "cashierreceipth", "cashierreceiptd"],
    "due_date": ["salesinvoiceh", "arbook"], # Tabel yang punya due date
    "jatuh_tempo": ["salesinvoiceh", "arbook"],
    "outstanding_payment": ["salesinvoiceh", "arbook", "customerpaymenth"], # Tabel untuk menghitung sisa bayar
    "belum_lunas": ["salesinvoiceh", "arbook", "customerpaymenth"],
    "payment_status": ["salesinvoiceh", "arbook", "customerpaymenth"], # Mirip dengan outstanding
    "piutang": ["arbook", "salesinvoiceh", "customerbalance"], # Tabel terkait data piutang umum
    "receivables": ["arbook", "salesinvoiceh", "customerbalance"],
    # --- AKHIR TAMBAHAN PENTING ---
}


async def consult_schema_node(state: AgentState) -> Dict[str, Any]:
    print(f"--- Executing Node: consult_schema_node ---", file=sys.stderr)
    
    intent = state.get("intent")
    entities_from_nlu = state.get("entities_mentioned", [])
    current_mcp_history = state.get("mcp_tool_call_history", [])

    schema_warnings: List[str] = []
    final_entities_for_filtering: List[str] = []

    # Langkah 1: Terjemahkan entitas NLU ke nama tabel yang mungkin
    if entities_from_nlu:
        for nlu_entity in entities_from_nlu:
            nlu_entity_lower = nlu_entity.lower()
            if nlu_entity_lower in ENTITY_TO_TABLE_MAP:
                final_entities_for_filtering.extend(ENTITY_TO_TABLE_MAP[nlu_entity_lower])
            else:
                # Jika tidak ada di map, asumsikan NLU mungkin sudah benar atau coba sebagai nama tabel langsung
                final_entities_for_filtering.append(nlu_entity_lower)
        # Hilangkan duplikasi
        final_entities_for_filtering = sorted(list(set(final_entities_for_filtering)))
        print(f"consult_schema_node: NLU entities '{entities_from_nlu}' mapped to potential table names: '{final_entities_for_filtering}'", file=sys.stderr)
    else:
        print("consult_schema_node: No entities from NLU, will fetch all schema for group.", file=sys.stderr)
        # Jika tidak ada entitas dari NLU, final_entities_for_filtering akan kosong,
        # yang berarti kita akan mengambil semua skema (sesuai logika di bawah).


    if not intent and not final_entities_for_filtering: # Perlu intent atau entitas untuk melanjutkan
        warning_msg = "Intent dan entitas tidak ditemukan untuk konsultasi skema."
        print(f"WARNING in consult_schema_node: {warning_msg}", file=sys.stderr)
        schema_warnings.append(warning_msg)
        return {
            "schema_consultation_warnings": schema_warnings,
            "relevant_tables": [],
            "table_relationships": [],
            "current_node_name": "consult_schema"
        }

    mcp_tool_call_log_entry = {
        "server_name": "graphiti_direct_neo4j_call",
        "tool_name": "get_relevant_schema_info_inline",
        "request_payload": {"intent": intent, "entities_for_filtering": final_entities_for_filtering}, # Log entitas yang sudah dimap
        "response_payload": None, "status": "error", "error_message": None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    driver: Optional[AsyncDriver] = None
    all_tables_from_db: List[TableSchemaMcpForClient] = []
    all_relationships_from_db: List[RelationshipMcpForClient] = []

    try:
        if not all([settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD]):
            # ... (error handling koneksi sama seperti sebelumnya) ...
            error_msg = "Neo4j connection details not fully configured." # Pesan lebih singkat
            print(f"ERROR in consult_schema_node: {error_msg}", file=sys.stderr)
            mcp_tool_call_log_entry["error_message"] = error_msg
            current_mcp_history.append(mcp_tool_call_log_entry)
            return {
                "schema_consultation_warnings": [error_msg],
                "relevant_tables": [], "table_relationships": [],
                "current_node_name": "consult_schema",
                "mcp_tool_call_history": current_mcp_history,
                "error_message_for_user": "Tidak dapat terhubung ke knowledge base skema."
            }

        print(f"consult_schema_node: Creating Neo4j driver for {settings.NEO4J_URI}", file=sys.stderr)
        driver = AsyncGraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
        
        async def fetch_all_schema_tx(tx: AsyncManagedTransaction): # Ganti nama fungsi agar lebih jelas
            nonlocal all_tables_from_db, all_relationships_from_db
            print("consult_schema_node: Fetching ALL schema from Neo4j for group_id...", file=sys.stderr)
            
            query_tables_cols = """
                MATCH (t:DatabaseTable {group_id: $group_id})-[:HAS_COLUMN]->(c:DatabaseColumn)
                WHERE t.group_id = $group_id AND c.group_id = $group_id
                RETURN t.table_name AS tableName, t.purpose AS tablePurpose, 
                       COLLECT({
                           name: c.column_name, type: c.type_from_db, 
                           description: c.description, classification: c.classification, 
                           is_aggregatable: c.is_aggregatable
                       }) AS columns
                ORDER BY tableName
            """
            result_tables = await tx.run(query_tables_cols, group_id=settings.SCHEMA_GROUP_ID)
            async for record in result_tables:
                cols_data = record["columns"] if record["columns"] is not None else []
                # Pastikan setiap col_data adalah dict sebelum di-unpack
                valid_cols_data = [col for col in cols_data if isinstance(col, dict)]
                cols = [ColumnMcpForClient(**col_data) for col_data in valid_cols_data]
                all_tables_from_db.append(TableSchemaMcpForClient(
                    table_name=record["tableName"], purpose=record["tablePurpose"], columns=cols
                ))
            
            query_relationships = """
                MATCH (c1:DatabaseColumn {group_id: $group_id})-[r:REFERENCES {group_id: $group_id}]->(c2:DatabaseColumn {group_id: $group_id})
                WHERE c1.group_id = $group_id AND c2.group_id = $group_id AND r.group_id = $group_id
                RETURN r.from_table AS fromTable, r.from_column AS fromColumn, 
                       r.to_table AS toTable, r.to_column AS toColumn,
                       r.relationship_type AS relationshipType 
                ORDER BY fromTable, fromColumn
            """
            result_rels = await tx.run(query_relationships, group_id=settings.SCHEMA_GROUP_ID)
            async for record in result_rels:
                rel_type_from_db = record.get("relationshipType")
                final_rel_type = rel_type_from_db if rel_type_from_db is not None else "FOREIGN_KEY"
                all_relationships_from_db.append(RelationshipMcpForClient(
                    from_table=record["fromTable"], from_column=record["fromColumn"], 
                    to_table=record["toTable"], to_column=record["toColumn"],
                    relationship_type=final_rel_type 
                ))

        async with driver.session(database=settings.NEO4J_DATABASE) as session:
            await session.execute_read(fetch_all_schema_tx) # Selalu fetch semua dulu
        
        print(f"consult_schema_node: Fetched {len(all_tables_from_db)} total tables and {len(all_relationships_from_db)} total relationships from Neo4j.", file=sys.stderr)

        # Langkah 2: Lakukan filtering berdasarkan final_entities_for_filtering
        final_tables_to_return_models: List[TableSchemaMcpForClient] = []
        final_relationships_to_return_models: List[RelationshipMcpForClient] = []

        if final_entities_for_filtering:
            entity_tables_lower_set = {e.lower() for e in final_entities_for_filtering}
            print(f"consult_schema_node: Applying filter with entities: {entity_tables_lower_set}", file=sys.stderr)
            
            final_tables_to_return_models = [
                tbl for tbl in all_tables_from_db
                if tbl.table_name.lower() in entity_tables_lower_set
            ]
            
            if final_tables_to_return_models:
                table_names_in_filtered_result_set = {t.table_name.lower() for t in final_tables_to_return_models}
                final_relationships_to_return_models = [
                    rel for rel in all_relationships_from_db
                    if rel.from_table.lower() in table_names_in_filtered_result_set and \
                       rel.to_table.lower() in table_names_in_filtered_result_set
                ]
                print(f"consult_schema_node: Filtered to {len(final_tables_to_return_models)} tables and {len(final_relationships_to_return_models)} relationships.", file=sys.stderr)
            else:
                warning_msg = f"Tidak ada tabel skema yang cocok setelah pemetaan dan filter dengan entitas: {final_entities_for_filtering} (NLU awal: {entities_from_nlu})."
                print(f"consult_schema_node: {warning_msg}", file=sys.stderr)
                schema_warnings.append(warning_msg)
                # Biarkan final_tables_to_return_models dan final_relationships_to_return_models kosong
        else: # Jika final_entities_for_filtering kosong (karena NLU awal kosong)
            print(f"consult_schema_node: No specific entities to filter by. Returning all {len(all_tables_from_db)} tables.", file=sys.stderr)
            final_tables_to_return_models = all_tables_from_db
            final_relationships_to_return_models = all_relationships_from_db
        
        # Convert Pydantic models to dicts for AgentState
        output_relevant_tables = [tbl.model_dump() for tbl in final_tables_to_return_models]
        output_table_relationships = [rel.model_dump() for rel in final_relationships_to_return_models]

        # Ekstrak financial_columns dan temporal_columns dari output_relevant_tables
        financial_cols_map: Dict[str, List[str]] = {}
        temporal_cols_map: Dict[str, List[str]] = {}
        for tbl_dict in output_relevant_tables:
            tbl_name = tbl_dict.get("table_name")
            if tbl_name:
                fc_list = []
                tc_list = []
                for col_dict in tbl_dict.get("columns", []):
                    classification = col_dict.get("classification", "")
                    col_name = col_dict.get("name")
                    if col_name:
                        if "financial" in classification:
                            fc_list.append(col_name)
                        elif "temporal" in classification:
                            tc_list.append(col_name)
                if fc_list:
                    financial_cols_map[tbl_name] = fc_list
                if tc_list:
                    temporal_cols_map[tbl_name] = tc_list


        mcp_tool_call_log_entry["status"] = "success"
        mcp_tool_call_log_entry["response_payload"] = {
            "relevant_tables": output_relevant_tables,
            "table_relationships": output_table_relationships
        }
        current_mcp_history.append(mcp_tool_call_log_entry)

        return {
            "relevant_tables": output_relevant_tables,
            "table_relationships": output_table_relationships,
            "financial_columns": financial_cols_map, # Diisi di sini
            "temporal_columns": temporal_cols_map,  # Diisi di sini
            "schema_consultation_warnings": schema_warnings,
            "current_node_name": "consult_schema",
            "mcp_tool_call_history": current_mcp_history
        }

    except (neo4j_exceptions.ServiceUnavailable, neo4j_exceptions.AuthError) as e_neo:
        # ... (error handling sama seperti sebelumnya) ...
        error_msg = f"Neo4j connection/auth error: {e_neo}"
        print(f"ERROR in consult_schema_node: {error_msg}", file=sys.stderr)
        mcp_tool_call_log_entry["error_message"] = error_msg
        current_mcp_history.append(mcp_tool_call_log_entry)
        return {
            "schema_consultation_warnings": [error_msg], "relevant_tables": [], "table_relationships": [],
            "error_message_for_user": "Tidak dapat terhubung ke knowledge base skema.",
            "current_node_name": "consult_schema", "mcp_tool_call_history": current_mcp_history
        }
    except Exception as e_gen:
        # ... (error handling sama seperti sebelumnya) ...
        error_msg = f"General error in consult_schema_node: {e_gen}"
        print(f"ERROR in consult_schema_node: {error_msg}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        mcp_tool_call_log_entry["error_message"] = error_msg
        current_mcp_history.append(mcp_tool_call_log_entry)
        return {
            "schema_consultation_warnings": [error_msg], "relevant_tables": [], "table_relationships": [],
            "error_message_for_user": "Terjadi kesalahan internal saat memproses skema.",
            "current_node_name": "consult_schema", "mcp_tool_call_history": current_mcp_history
        }
    finally:
        if driver:
            await driver.close()
            print("consult_schema_node: Neo4j driver closed.", file=sys.stderr)