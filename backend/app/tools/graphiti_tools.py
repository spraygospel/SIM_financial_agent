# backend/app/tools/graphiti_tools.py

import json
import uuid
from typing import List, Dict, Any, Optional, AsyncIterator
from contextlib import asynccontextmanager

# Impor Pydantic dan config utama
from pydantic import BaseModel, Field
from backend.app.core.config import settings

# Impor Neo4j
from neo4j import AsyncGraphDatabase, AsyncDriver

# --- Pydantic Models (Input & Output Tools) ---
class GetRelevantSchemaInput(BaseModel): 
    entities: List[str]

class ColumnSchema(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    classification: Optional[str] = None
    is_aggregatable: Optional[bool] = None

class TableSchema(BaseModel):
    table_name: str
    purpose: Optional[str] = None
    columns: List[ColumnSchema]

class RelationshipSchema(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    relationship_type: str = "FOREIGN_KEY"

class RelevantSchemaOutput(BaseModel):
    relevant_tables: List[TableSchema]
    table_relationships: List[RelationshipSchema]
    success: bool = True
    error: Optional[str] = None

class StoreSessionDataInput(BaseModel):
    session_id: str
    data_to_store: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class DataHandle(BaseModel):
    data_handle_id: str
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

# --- Pengelola Koneksi Neo4j (Pola yang Baik) ---
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

# --- Definisi Tool sebagai Fungsi Python Biasa ---

async def get_relevant_schema(payload: Dict[str, Any]) -> RelevantSchemaOutput:
    """
    Mengambil "peta data" (skema, kolom, relasi) yang relevan dari knowledge graph.
    Tool ini WAJIB dipanggil dengan daftar entitas (nama tabel) yang spesifik.
    """
    try:
        validated_input = GetRelevantSchemaInput(**payload)
    except Exception as e:
        error_msg = f"Gagal memvalidasi input untuk get_relevant_schema. Error: {e}"
        print(f"\n🔥 [ERROR] {error_msg}")
        return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=error_msg)

    # --- PERBAIKAN PENTING DI SINI ---
    # Tambahkan jaring pengaman untuk mencegah panggilan dengan entities kosong
    if not validated_input.entities:
        error_msg = "Error: `get_relevant_schema` tidak boleh dipanggil dengan daftar entitas kosong. Identifikasi dulu tabel yang relevan."
        print(f"\n🔥 [ERROR] {error_msg}")
        # Kembalikan daftar nama tabel yang tersedia sebagai petunjuk untuk LLM
        try:
            async with get_neo4j_driver() as driver:
                async with driver.session(database=settings.NEO4J_DATABASE) as session:
                    result = await session.run("MATCH (t:DatabaseTable {group_id: $gid}) RETURN t.table_name as name", gid=settings.SCHEMA_GROUP_ID)
                    available_tables = [record["name"] for record in await result.data()]
            hint = f"Tabel yang tersedia: {', '.join(available_tables[:20])}..." # Beri petunjuk sebagian tabel
            return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=f"{error_msg}. {hint}")
        except Exception as e_hint:
            return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=f"{error_msg}. Gagal mengambil daftar tabel: {e_hint}")
    # -------------------------------------
    
    try:
        async with get_neo4j_driver() as driver:
            async with driver.session(database=settings.NEO4J_DATABASE) as session:
                tables_result = await session.run(
                    """
                    MATCH (t:DatabaseTable {group_id: $gid})-[:HAS_COLUMN]->(c:DatabaseColumn)
                    WHERE t.table_name IN $entities
                    RETURN t.table_name AS table_name, t.purpose AS tablePurpose, 
                           collect({
                               name: c.column_name, type: c.type_from_db, description: c.description, 
                               classification: c.classification, is_aggregatable: c.is_aggregatable
                           }) AS columns
                    ORDER BY table_name
                    """, gid=settings.SCHEMA_GROUP_ID, entities=validated_input.entities
                )
                
                records_raw = await tables_result.data()
                records_processed = []
                for r in records_raw:
                    records_processed.append({
                        "table_name": r["table_name"],
                        "purpose": r.get("tablePurpose"),
                        "columns": r["columns"]
                    })
                tables_data = [TableSchema(**r) for r in records_processed]

                rels_result = await session.run(
                    """
                    MATCH (c1:DatabaseColumn)-[r:REFERENCES]->(c2:DatabaseColumn)
                    WHERE r.group_id = $gid AND r.from_table IN $entities AND r.to_table IN $entities
                    RETURN r.from_table AS from_table, r.from_column AS from_column, r.to_table AS to_table, r.to_column AS to_column
                    """, gid=settings.SCHEMA_GROUP_ID, entities=validated_input.entities
                )
                rels_records = await rels_result.data()
                rels_data = [RelationshipSchema(**r) for r in rels_records]

        return RelevantSchemaOutput(relevant_tables=tables_data, table_relationships=rels_data)
    except Exception as e:
        return RelevantSchemaOutput(relevant_tables=[], table_relationships=[], success=False, error=str(e))

async def store_session_data(payload: StoreSessionDataInput) -> StoreSessionDataOutput:
    """
    Menyimpan data hasil query ke dalam memori sesi sementara (node di Graphiti)
    dan mengembalikan sebuah 'DataHandle' sebagai referensi.
    """
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
        return StoreSessionDataOutput(success=False, error=str(e))

async def retrieve_session_data(payload: RetrieveSessionDataInput) -> List[Dict[str, Any]] | None:
    """
    Mengambil kembali data yang sebelumnya disimpan di memori sesi menggunakan DataHandle.
    Mengembalikan data jika sukses, atau None jika gagal.
    """
    try:
        async with get_neo4j_driver() as driver:
            async with driver.session(database=settings.NEO4J_DATABASE) as session:
                result = await session.run(
                    "MATCH (d:SessionData {uuid: $uuid, group_id: $sid}) RETURN d.data_json AS data",
                    uuid=payload.data_handle_id, sid=payload.session_id
                )
                record = await result.single()

        if record and record["data"]:
            return json.loads(record["data"])
        else:
            return None
    except Exception:
        return None