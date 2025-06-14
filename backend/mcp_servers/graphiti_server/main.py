# backend/mcp_servers/graphiti_server/main.py (Revisi Final dengan Pola yang Benar)

import sys
import os
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, AsyncIterator
from contextlib import asynccontextmanager

# --- Setup Path Mandiri (Wajib di Atas) ---
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# --- Impor Lokal & Library ---
from pydantic import BaseModel, Field
from neo4j import AsyncGraphDatabase, AsyncDriver

from mcp.server.fastmcp import FastMCP, Context
# Impor dari config lokal, bukan global
from backend.mcp_servers.graphiti_server.config import settings

# --- Pydantic Models ---
class GetRelevantSchemaInfoInput(BaseModel):
    intent: str
    entities: List[str]

class ColumnMcp(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    classification: Optional[str] = None
    is_aggregatable: Optional[bool] = None

class TableSchemaMcp(BaseModel):
    table_name: str
    purpose: Optional[str] = None
    columns: List[ColumnMcp]

class RelationshipMcp(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    relationship_type: str = "FOREIGN_KEY"

class RelevantSchemaOutput(BaseModel):
    relevant_tables: List[TableSchemaMcp]
    table_relationships: List[RelationshipMcp]
    success: bool = True
    error: Optional[str] = None

class StoreSessionDataInput(BaseModel):
    session_id: str
    data_to_store: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class DataHandle(BaseModel):
    data_handle_id: str
    storage_location: str = "Graphiti"
    group_id: str
    data_description: str
    row_count: int

class StoreSessionDataOutput(BaseModel):
    data_handle: Optional[DataHandle] = None
    success: bool = True
    error: Optional[str] = None

class RetrieveSessionDataInput(BaseModel):
    session_id: str
    data_handle_id: str

class RetrieveSessionDataOutput(BaseModel):
    retrieved_data: Optional[List[Dict[str, Any]]] = None
    success: bool = True
    error: Optional[str] = None

# --- Pengelola Koneksi Neo4j ---
@asynccontextmanager
async def get_neo4j_driver() -> AsyncIterator[AsyncDriver]:
    if not all([settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD]):
        raise ConnectionError("Detail koneksi Neo4j tidak dikonfigurasi sepenuhnya.")
    
    driver = AsyncGraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
    try:
        await driver.verify_connectivity()
        yield driver
    finally:
        await driver.close()

# --- Inisialisasi & Definisi Tool MCP ---
mcp = FastMCP(
    name="GraphitiDataServer",
    title="Graphiti Data & Schema Server",
    description="Server untuk mengambil metadata skema dan mengelola data sesi sementara di Neo4j."
)

# ... (Definisi tool get_relevant_schema, store_session_data, retrieve_session_data tetap sama persis)
@mcp.tool()
async def get_relevant_schema(ctx: Context, payload: GetRelevantSchemaInfoInput) -> RelevantSchemaOutput:
    ctx.info(f"Tool 'get_relevant_schema' dipanggil untuk entitas: {payload.entities}")
    try:
        async with get_neo4j_driver() as driver:
            async with driver.session(database=settings.NEO4J_DATABASE) as session:
                tables_result = await session.run(
                    """
                    MATCH (t:DatabaseTable {group_id: $gid})-[:HAS_COLUMN]->(c:DatabaseColumn)
                    WHERE size($entities) = 0 OR t.table_name IN $entities
                    RETURN t.table_name AS tableName, t.purpose AS tablePurpose, 
                           collect({
                               name: c.column_name, type: c.type_from_db, description: c.description, 
                               classification: c.classification, is_aggregatable: c.is_aggregatable
                           }) AS columns
                    ORDER BY tableName
                    """, gid=settings.SCHEMA_GROUP_ID, entities=payload.entities
                )
                records = await tables_result.data()
                tables_data = [
                    TableSchemaMcp(
                        table_name=r["tableName"],
                        purpose=r["tablePurpose"],
                        columns=[ColumnMcp(**c) for c in r["columns"]]
                    )
                    for r in records
                ]

                rels_result = await session.run(
                    """
                    MATCH (c1:DatabaseColumn)-[r:REFERENCES]->(c2:DatabaseColumn)
                    WHERE r.group_id = $gid AND (size($entities) = 0 OR (r.from_table IN $entities AND r.to_table IN $entities))
                    RETURN r.from_table AS from_table, r.from_column AS from_column, r.to_table AS to_table, r.to_column AS to_column
                    """, gid=settings.SCHEMA_GROUP_ID, entities=payload.entities
                )
                rels_records = await rels_result.data()
                rels_data = [RelationshipMcp(**r) for r in rels_records]

        return RelevantSchemaOutput(success=True, relevant_tables=tables_data, table_relationships=rels_data)
    except Exception as e:
        ctx.error(f"Error di get_relevant_schema: {e}", exc_info=True)
        return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=str(e))

@mcp.tool()
async def store_session_data(ctx: Context, payload: StoreSessionDataInput) -> StoreSessionDataOutput:
    ctx.info(f"Tool 'store_session_data' dipanggil untuk sesi: {payload.session_id}")
    handle_id = str(uuid.uuid4())
    try:
        async with get_neo4j_driver() as driver:
            async with driver.session(database=settings.NEO4J_DATABASE) as session:
                await session.run(
                    """
                    CREATE (d:SessionData {
                        uuid: $uuid, group_id: $sid, data_json: $data,
                        description: $desc, row_count: $count, created_at: datetime()
                    })
                    """, uuid=handle_id, sid=payload.session_id, data=json.dumps(payload.data_to_store),
                         desc=payload.metadata.get("data_description", "N/A"), count=len(payload.data_to_store)
                )
        handle = DataHandle(
            data_handle_id=handle_id, group_id=payload.session_id,
            data_description=payload.metadata.get("data_description", "N/A"), row_count=len(payload.data_to_store)
        )
        return StoreSessionDataOutput(data_handle=handle)
    except Exception as e:
        ctx.error(f"Error di store_session_data: {e}", exc_info=True)
        return StoreSessionDataOutput(success=False, error=str(e))

@mcp.tool()
async def retrieve_session_data(ctx: Context, payload: RetrieveSessionDataInput) -> RetrieveSessionDataOutput:
    ctx.info(f"Tool 'retrieve_session_data' dipanggil untuk handle: {payload.data_handle_id}")
    try:
        async with get_neo4j_driver() as driver:
            async with driver.session(database=settings.NEO4J_DATABASE) as session:
                result = await session.run(
                    "MATCH (d:SessionData {uuid: $uuid, group_id: $sid}) RETURN d.data_json AS data",
                    uuid=payload.data_handle_id, sid=payload.session_id
                )
                record = await result.single()

        if record and record["data"]:
            return RetrieveSessionDataOutput(retrieved_data=json.loads(record["data"]))
        else:
            return RetrieveSessionDataOutput(success=False, error="Data tidak ditemukan atau sesi tidak cocok.")
    except Exception as e:
        ctx.error(f"Error di retrieve_session_data: {e}", exc_info=True)
        return RetrieveSessionDataOutput(success=False, error=str(e))

# --- Main Execution & ASGI App Exposure ---
if __name__ == "__main__":
    print("Menjalankan Graphiti Server secara langsung tidak direkomendasikan. Gunakan uvicorn.", file=sys.stderr)
    mcp.run()
