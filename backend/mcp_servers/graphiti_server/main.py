# backend/mcp_servers/graphiti_server/main.py
import os
import sys
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context as MCPContext # Impor Context
from neo4j import AsyncGraphDatabase, AsyncSession, AsyncManagedTransaction, AsyncDriver
from neo4j import exceptions as neo4j_exceptions

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
dotenv_path = os.path.join(project_root, 'backend', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

def debug_print(*args, **kwargs):
    other_kwargs = {k: v for k, v in kwargs.items() if k != 'file'}
    print(*args, file=sys.stderr, **other_kwargs)

debug_print("--- GRAPHITI SERVER STARTING ---", file=sys.stderr)

# --- Pydantic Models ---
class GetRelevantSchemaInfoInput(BaseModel): 
    intent: str = Field(..., description="Intent utama yang terdeteksi dari query pengguna, misal 'sales_analysis'.")
    entities: List[str] = Field(..., description="Daftar entitas yang terdeteksi dari query, misal ['sales_orders', 'order_date']. Entitas ini bisa berupa nama tabel atau nama kolom yang relevan.")

class ColumnMcp(BaseModel): 
    name: str = Field(...)
    type: Optional[str] = None
    description: Optional[str] = None
    classification: Optional[str] = None
    is_aggregatable: Optional[bool] = None

class TableSchemaMcp(BaseModel): 
    table_name: str = Field(...)
    purpose: Optional[str] = None
    columns: List[ColumnMcp] = Field(...)

class RelationshipMcp(BaseModel): 
    from_table: str = Field(...)
    from_column: str = Field(...)
    to_table: str = Field(...)
    to_column: str = Field(...)
    relationship_type: str = Field(default="FOREIGN_KEY")

class RelevantSchemaOutput(BaseModel): 
    relevant_tables: List[TableSchemaMcp] = Field(...)
    table_relationships: List[RelationshipMcp] = Field(...)
    success: bool = True
    error: Optional[str] = None

# --- Neo4j Config ---
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
SCHEMA_GROUP_ID = os.getenv("SCHEMA_GROUP_ID", "sim_testgeluran_schema") # Ambil dari env, default ke yang sudah ada

# --- MCP Server Initialization ---
mcp = FastMCP( 
    name="GraphitiSchemaServer", 
    title="Graphiti Schema Server",
    description="Server untuk mengambil metadata skema dari Neo4j (Graphiti)."
)

# --- Tool Implementation ---
@mcp.tool()
async def get_relevant_schema_info(
    ctx: MCPContext, 
    payload: GetRelevantSchemaInfoInput 
) -> RelevantSchemaOutput:
    """
    Mengambil informasi skema (tabel, kolom, relasi) yang paling relevan dari Graphiti (Neo4j)
    berdasarkan intent dan entitas yang terdeteksi dari query pengguna. Tool ini dapat memfilter
    hasil berdasarkan entitas yang diberikan untuk mengurangi ukuran output.

    Args:
        ctx: Konteks MCP. (Digunakan untuk logging internal tool via ctx.info(), ctx.error())
        payload (GetRelevantSchemaInfoInput): Objek input yang berisi:
            intent (str): Intent utama dari query pengguna (misal 'inventory_analysis', 'financial_summary').
                          Saat ini, intent belum digunakan secara aktif untuk filtering di Cypher,
                          namun dikirim untuk penggunaan di masa depan atau logging.
            entities (List[str]): Daftar NAMA TABEL yang relevan. Jika daftar ini tidak kosong,
                                  tool akan memfilter output agar hanya menyertakan tabel-tabel
                                  ini dan relasi di antaranya. Jika kosong, semua tabel dari
                                  SCHEMA_GROUP_ID akan dikembalikan.
                                  Contoh: ["adjustind", "adjustinh", "masterlocation"]

    Returns:
        RelevantSchemaOutput: Objek output yang berisi daftar tabel relevan, relasi,
                              status sukses, dan pesan error jika ada.

    Contoh Penggunaan oleh Agent (dalam format pemanggilan tool):
    ```json
    {
        "tool_name": "get_relevant_schema_info",
        "payload": {
            "intent": "inventory_adjustment_analysis",
            "entities": ["adjustind", "adjustinh", "masterlocation"]
        }
    }
    ```
    ```json
    {
        "tool_name": "get_relevant_schema_info",
        "payload": {
            "intent": "view_action_log_schema",
            "entities": ["actionlog"]
        }
    }
    ```
    ```json
    {
        "tool_name": "get_relevant_schema_info",
        "payload": {
            "intent": "get_all_schema_details",
            "entities": [] // Akan mengembalikan semua tabel dalam SCHEMA_GROUP_ID
        }
    }
    ```
    """
    
    ctx.info(f"Tool 'get_relevant_schema_info' called. Intent: '{payload.intent}', Entities: {payload.entities}")
    
    driver: Optional[AsyncDriver] = None
    relevant_tables_data: List[TableSchemaMcp] = []
    table_relationships_data: List[RelationshipMcp] = []

    try:
        if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
            error_msg = "Neo4j connection details (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD) not fully configured in .env."
            ctx.error(error_msg)
            return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=error_msg)

        ctx.info(f"Creating new Neo4j driver instance for {NEO4J_URI}")
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        async def fetch_schema_tx(tx: AsyncManagedTransaction):
            nonlocal relevant_tables_data, table_relationships_data
            ctx.info("Fetching schema from Neo4j...")
            
            # Query untuk mengambil tabel dan kolom-kolomnya
            query_tables_cols = """
                MATCH (t:DatabaseTable {group_id: $group_id})-[:HAS_COLUMN]->(c:DatabaseColumn)
                WHERE t.group_id = $group_id AND c.group_id = $group_id
                RETURN t.table_name AS tableName, 
                       t.purpose AS tablePurpose, 
                       COLLECT({
                           name: c.column_name, 
                           type: c.type_from_db, 
                           description: c.description, 
                           classification: c.classification, 
                           is_aggregatable: c.is_aggregatable
                       }) AS columns
                ORDER BY tableName
            """
            result_tables = await tx.run(query_tables_cols, group_id=SCHEMA_GROUP_ID)
            async for record in result_tables:
                cols_data = record["columns"] if record["columns"] is not None else []
                cols = [ColumnMcp(**col_data) for col_data in cols_data]
                relevant_tables_data.append(TableSchemaMcp(
                    table_name=record["tableName"], 
                    purpose=record["tablePurpose"], 
                    columns=cols
                ))
            ctx.info(f"Fetched {len(relevant_tables_data)} tables with columns from group_id '{SCHEMA_GROUP_ID}'.")

            query_relationships = """
                MATCH (c1:DatabaseColumn {group_id: $group_id})-[r:REFERENCES {group_id: $group_id}]->(c2:DatabaseColumn {group_id: $group_id})
                WHERE c1.group_id = $group_id AND c2.group_id = $group_id AND r.group_id = $group_id
                RETURN r.from_table AS fromTable, 
                       r.from_column AS fromColumn, 
                       r.to_table AS toTable, 
                       r.to_column AS toColumn,
                       r.relationship_type AS relationshipType 
                ORDER BY fromTable, fromColumn
            """
            result_rels = await tx.run(query_relationships, group_id=SCHEMA_GROUP_ID)
            async for record in result_rels:
                rel_type_from_db = record.get("relationshipType")
                
                # Tentukan nilai yang akan diteruskan ke Pydantic model
                # Pastikan selalu string, gunakan default jika None
                final_rel_type = rel_type_from_db if rel_type_from_db is not None else "FOREIGN_KEY"

                table_relationships_data.append(RelationshipMcp(
                    from_table=record["fromTable"], 
                    from_column=record["fromColumn"], 
                    to_table=record["toTable"], 
                    to_column=record["toColumn"],
                    relationship_type=final_rel_type 
                ))
            ctx.info(f"Fetched {len(table_relationships_data)} relationships from group_id '{SCHEMA_GROUP_ID}'.")
        async with driver.session(database="neo4j") as session: 
            await session.execute_read(fetch_schema_tx)
            
        final_tables_to_return = relevant_tables_data
        final_relationships_to_return = table_relationships_data
        
        # Logika filtering berdasarkan payload.entities
        if payload.entities:
            entity_tables_lower = [e.lower() for e in payload.entities]
            ctx.info(f"Filtering schema based on entities: {entity_tables_lower}")
            
            filtered_tables = [
                tbl for tbl in relevant_tables_data 
                if tbl.table_name.lower() in entity_tables_lower
            ]
            
            if filtered_tables:
                final_tables_to_return = filtered_tables
                table_names_in_filtered_result = {t.table_name.lower() for t in final_tables_to_return}
                
                final_relationships_to_return = [
                    rel for rel in table_relationships_data 
                    if rel.from_table.lower() in table_names_in_filtered_result and \
                       rel.to_table.lower() in table_names_in_filtered_result
                ]
                ctx.info(f"Filtered to {len(final_tables_to_return)} tables and {len(final_relationships_to_return)} relationships.")
            else:
                ctx.warning(f"No tables matched the provided entities: {payload.entities}. Returning all tables found in group '{SCHEMA_GROUP_ID}'.")
                # Jika filter menghasilkan 0 tabel, kita kembalikan semua tabel yang ada di group_id tersebut,
                # atau bisa juga error. Untuk saat ini, kembalikan semua.
                # Atau jika ingin strict, bisa jadi error atau empty list:
                # final_tables_to_return = []
                # final_relationships_to_return = []

        else:
            ctx.info("No entity filter provided, returning all tables and relationships for the group_id.")

        return RelevantSchemaOutput(
            relevant_tables=final_tables_to_return,
            table_relationships=final_relationships_to_return,
            success=True
        )
    
    except neo4j_exceptions.ServiceUnavailable as e_service:
        error_msg = f"Neo4j service is unavailable: {e_service}"
        ctx.error(error_msg)
        return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=error_msg)
    except neo4j_exceptions.AuthError as e_auth:
        error_msg = f"Neo4j authentication failed: {e_auth}"
        ctx.error(error_msg)
        return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=error_msg)
    except Exception as e_tool:
        error_msg = f"General error in get_relevant_schema_info: {str(e_tool)}"
        ctx.error(f"TOOL ERROR: {error_msg}")
        import traceback
        tb_str = traceback.format_exc()
        ctx.error(f"Traceback: {tb_str}")
        return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=error_msg)
    finally:
        if driver:
            await driver.close()
            ctx.info("Neo4j driver closed for this call.")


if __name__ == "__main__":
    debug_print("Running Graphiti Schema Server directly (stdio)...", file=sys.stderr)
    debug_print(f"Attempting to use Neo4j: uri={NEO4J_URI}, user={NEO4J_USER}, schema_group_id={SCHEMA_GROUP_ID}", file=sys.stderr)
    mcp.run()

debug_print("--- GRAPHITI SERVER MODULE LOADED ---", file=sys.stderr)