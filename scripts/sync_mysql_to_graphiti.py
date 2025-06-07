# File: scripts/sync_mysql_to_graphiti.py

import os
import json
import asyncio
import uuid # Kita akan tetap gunakan uuid.uuid5 untuk deterministik
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from neo4j import AsyncGraphDatabase, AsyncSession, AsyncManagedTransaction # Tambahkan import yang relevan
from neo4j import exceptions as neo4j_exceptions

# Import Graphiti client hanya untuk inisialisasi driver jika diperlukan, atau bisa langsung pakai AsyncGraphDatabase
# Untuk operasi tulis, kita akan pakai driver Neo4j langsung seperti saran pakar untuk kontrol penuh.
# from graphiti_core import Graphiti 

import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from backend.app.schemas.graphiti_schema_nodes import (
    DatabaseTableNode, 
    DatabaseColumnNode,
    HasColumnEdge,
    ReferencesEdge,
    NAMESPACE_AI_AGENT_SCHEMA # Impor namespace UUID kita
)

# --- Konfigurasi ---
GROUP_ID = "sim_testgeluran_schema"
SEMANTIC_MAPPING_FILE_PATH = os.path.join(project_root, "data_samples", "graphiti_semantic_mapping.json")
# -------------------

class DatabaseSchemaImporter:
    def __init__(self, uri: str, user: str, password: str):
        # Menggunakan AsyncGraphDatabase.driver langsung seperti contoh pakar
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
    
    async def close(self):
        if self.driver:
            await self.driver.close()
            print("Neo4j driver connection closed by importer.")

    async def _ensure_indexes(self, session: AsyncSession):
        """Membuat indeks yang diperlukan jika belum ada menggunakan managed transaction."""
        async def create_indexes_tx(tx: AsyncManagedTransaction):
            print("Ensuring indexes exist...")
            await tx.run("CREATE INDEX dbTableUuid IF NOT EXISTS FOR (n:DatabaseTable) ON (n.uuid)")
            await tx.run("CREATE INDEX dbTableGroupId IF NOT EXISTS FOR (n:DatabaseTable) ON (n.group_id)")
            await tx.run("CREATE INDEX dbColumnUuid IF NOT EXISTS FOR (n:DatabaseColumn) ON (n.uuid)")
            await tx.run("CREATE INDEX dbColumnGroupId IF NOT EXISTS FOR (n:DatabaseColumn) ON (n.group_id)")
            print("Indexes checked/created.")
        
        await session.execute_write(create_indexes_tx)

    async def _create_table_nodes(self, session: AsyncSession, schema_data: Dict[str, Any]) -> Dict[str, DatabaseTableNode]:
        table_nodes_dict: Dict[str, DatabaseTableNode] = {}

        async def create_tables_tx(tx: AsyncManagedTransaction):
            nonlocal table_nodes_dict
            print(f"Phase 1b: Creating/Merging {len(schema_data)} TableNodes...")
            for table_name_json, table_details in schema_data.items():
                table_name = table_name_json
                
                # Menggunakan UUID deterministik kita
                table_uuid = str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{GROUP_ID}.{table_name}"))
                
                props_for_node = {
                    "table_name": table_name, # Menggunakan 'table_name' sesuai model Pydantic kita
                    "purpose": table_details.get("purpose"),
                    "business_category": table_details.get("business_category")
                }

                query = """
                MERGE (t:DatabaseTable {uuid: $uuid, group_id: $group_id})
                ON CREATE SET 
                    t += $props, 
                    t.label_metadata_type = 'DatabaseTable', 
                    t.created_at = datetime()
                ON MATCH SET 
                    t += $props, 
                    t.label_metadata_type = 'DatabaseTable', 
                    t.updated_at = datetime()
                RETURN t.uuid as uuid, t.table_name as name
                """
                result = await tx.run(query, {
                    'uuid': table_uuid,
                    'group_id': GROUP_ID,
                    'props': props_for_node
                })
                record = await result.single()
                if record:
                    # print(f"  Created/Merged table node: {record['name']} -> {record['uuid']}")
                    # Simpan instance Pydantic untuk referensi nanti (misalnya untuk ambil UUID)
                    table_nodes_dict[table_name] = DatabaseTableNode(
                        uuid=table_uuid, group_id=GROUP_ID, table_name=table_name,
                        purpose=props_for_node["purpose"], business_category=props_for_node["business_category"]
                    )
            print("TableNodes created/merged.")
        
        await session.execute_write(create_tables_tx)
        return table_nodes_dict

    async def _create_column_nodes(self, session: AsyncSession, schema_data: Dict[str, Any]) -> Dict[str, DatabaseColumnNode]:
        column_nodes_dict: Dict[str, DatabaseColumnNode] = {}

        async def create_columns_tx(tx: AsyncManagedTransaction):
            nonlocal column_nodes_dict
            column_count = sum(len(details.get("columns", {})) for details in schema_data.values())
            print(f"Phase 1c: Creating/Merging {column_count} ColumnNodes...")
            for table_name_json, table_details in schema_data.items():
                table_name = table_name_json
                if "columns" in table_details:
                    for col_name_json, col_details in table_details["columns"].items():
                        col_name = col_name_json
                        column_key = f"{table_name}.{col_name}" # Untuk dictionary Python
                        
                        # Menggunakan UUID deterministik kita
                        col_uuid = str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{GROUP_ID}.{table_name}.{col_name}"))

                        props_for_node = {
                            "column_name": col_name, # Sesuai model Pydantic kita
                            "table_name_prop": table_name, # Menyimpan nama tabel induk sebagai properti
                            "description": col_details.get("description"),
                            "classification": col_details.get("classification"),
                            "is_aggregatable": col_details.get("is_aggregatable"),
                            "type_from_db": col_details.get("type_from_db")
                        }
                        
                        query = """
                        MERGE (c:DatabaseColumn {uuid: $uuid, group_id: $group_id})
                        ON CREATE SET 
                            c += $props, 
                            c.label_metadata_type = 'DatabaseColumn', 
                            c.created_at = datetime()
                        ON MATCH SET 
                            c += $props, 
                            c.label_metadata_type = 'DatabaseColumn', 
                            c.updated_at = datetime()
                        RETURN c.uuid as uuid, c.column_name as name, c.table_name_prop as t_name
                        """
                        result = await tx.run(query, {
                            'uuid': col_uuid,
                            'group_id': GROUP_ID,
                            'props': props_for_node
                        })
                        record = await result.single()
                        if record:
                            # print(f"  Created/Merged column node: {record['t_name']}.{record['name']} -> {record['uuid']}")
                            column_nodes_dict[column_key] = DatabaseColumnNode(
                                uuid=col_uuid, group_id=GROUP_ID, column_name=col_name,
                                description=props_for_node["description"], classification=props_for_node["classification"],
                                is_aggregatable=props_for_node["is_aggregatable"], type_from_db=props_for_node["type_from_db"]
                            )
            print("ColumnNodes created/merged.")

        await session.execute_write(create_columns_tx)
        return column_nodes_dict

    async def _create_has_column_relationships(self, session: AsyncSession, schema_data: Dict[str, Any], 
                                               table_nodes: Dict[str, DatabaseTableNode], 
                                               column_nodes: Dict[str, DatabaseColumnNode]):
        has_column_edges_created = 0
        
        async def create_has_column_tx(tx: AsyncManagedTransaction):
            nonlocal has_column_edges_created
            print("Phase 2: Creating/Merging HAS_COLUMN relationships...")
            for table_name_json, table_details in schema_data.items():
                table_name = table_name_json
                current_table_node = table_nodes.get(table_name)
                if not current_table_node:
                    print(f"    WARNING: TableNode for '{table_name}' not found, skipping HAS_COLUMN rels.")
                    continue

                if "columns" in table_details:
                    for col_name_json in table_details["columns"].keys():
                        col_name = col_name_json
                        column_key = f"{table_name}.{col_name}"
                        current_column_node = column_nodes.get(column_key)

                        if not current_column_node:
                            print(f"    WARNING: ColumnNode for '{column_key}' not found, skipping HAS_COLUMN rel.")
                            continue
                        
                        # Menggunakan UUID deterministik kita untuk edge
                        edge_uuid = str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{GROUP_ID}.{current_table_node.uuid}.{current_column_node.uuid}.HAS_COLUMN"))

                        query = """
                        MATCH (source_node:DatabaseTable {uuid: $s_uuid, group_id: $gid})
                        MATCH (target_node:DatabaseColumn {uuid: $t_uuid, group_id: $gid})
                        MERGE (source_node)-[r:HAS_COLUMN {uuid: $e_uuid}]->(target_node)
                        ON CREATE SET 
                            r.group_id = $gid,
                            r.created_at = datetime()
                        ON MATCH SET
                            r.group_id = $gid,
                            r.updated_at = datetime()
                        RETURN r
                        """
                        result = await tx.run(query, {
                            's_uuid': current_table_node.uuid,
                            't_uuid': current_column_node.uuid,
                            'e_uuid': edge_uuid,
                            'gid': GROUP_ID
                        })
                        record = await result.single()
                        if record and record["r"]:
                            has_column_edges_created += 1
                        else:
                            print(f"    WARNING/NO_OP: MERGE for HAS_COLUMN for {table_name}.{col_name} did not return/create rel. Source: {current_table_node.uuid}, Target: {current_column_node.uuid}")
            print(f"{has_column_edges_created} HAS_COLUMN relationships created/merged.")

        await session.execute_write(create_has_column_tx)
        
    async def _create_references_relationships(self, session: AsyncSession, schema_data: Dict[str, Any], 
                                               table_nodes: Dict[str, DatabaseTableNode], 
                                               column_nodes: Dict[str, DatabaseColumnNode]):
        references_edges_created = 0

        async def create_references_tx(tx: AsyncManagedTransaction):
            nonlocal references_edges_created
            print("Phase 3: Creating/Merging REFERENCES relationships...")
            for table_name_json, table_details in schema_data.items():
                table_name = table_name_json # from_table
                if "relationships" in table_details and table_details["relationships"]:
                    for rel_info in table_details["relationships"]:
                        from_col_name = rel_info.get("from_column")
                        to_table_name = rel_info.get("to_table")
                        to_col_name = rel_info.get("to_column")

                        from_column_key = f"{table_name}.{from_col_name}"
                        to_column_key = f"{to_table_name}.{to_col_name}"

                        from_col_node = column_nodes.get(from_column_key)
                        to_col_node = column_nodes.get(to_column_key)

                        if from_col_node and to_col_node:
                            # Menggunakan UUID deterministik kita untuk edge
                            edge_uuid = str(uuid.uuid5(NAMESPACE_AI_AGENT_SCHEMA, f"{GROUP_ID}.{from_col_node.uuid}.{to_col_node.uuid}.REFERENCES"))
                            
                            query = """
                            MATCH (source_node:DatabaseColumn {uuid: $s_uuid, group_id: $gid})
                            MATCH (target_node:DatabaseColumn {uuid: $t_uuid, group_id: $gid})
                            MERGE (source_node)-[r:REFERENCES {uuid: $e_uuid}]->(target_node)
                            ON CREATE SET 
                                r.group_id = $gid,
                                r.from_table = $f_table,
                                r.from_column = $f_column,
                                r.to_table = $t_table,
                                r.to_column = $t_column,
                                r.created_at = datetime()
                            ON MATCH SET
                                r.group_id = $gid,
                                r.from_table = $f_table,
                                r.from_column = $f_column,
                                r.to_table = $t_table,
                                r.to_column = $t_column,
                                r.updated_at = datetime()
                            RETURN r
                            """
                            result = await tx.run(query, {
                                's_uuid': from_col_node.uuid,
                                't_uuid': to_col_node.uuid,
                                'e_uuid': edge_uuid,
                                'gid': GROUP_ID,
                                'f_table': table_name, # from_table name
                                'f_column': from_col_name,
                                't_table': to_table_name,
                                't_column': to_col_name
                            })
                            record = await result.single()
                            if record and record["r"]:
                                references_edges_created += 1
                            else:
                                print(f"    WARNING/NO_OP: MERGE for REFERENCES for {from_column_key} -> {to_column_key} did not return/create rel.")
                        else:
                            if not from_col_node:
                                print(f"    SKIPPED REFERENCES: Source ColumnNode not found for {from_column_key}")
                            if not to_col_node:
                                print(f"    SKIPPED REFERENCES: Target ColumnNode not found for {to_column_key}")
            print(f"{references_edges_created} REFERENCES relationships created/merged.")
        
        await session.execute_write(create_references_tx)

    async def import_schema(self, schema_data: Dict[str, Any]):
        """Import database schema using proper transaction management"""
        async with self.driver.session(database="neo4j") as session: # Pastikan nama database Neo4j benar
            await self._ensure_indexes(session)
            
            # Fase 1: Buat semua nodes
            table_nodes_map = await self._create_table_nodes(session, schema_data)
            column_nodes_map = await self._create_column_nodes(session, schema_data)
            
            # Fase 2: Buat relationships
            await self._create_has_column_relationships(session, schema_data, table_nodes_map, column_nodes_map)
            await self._create_references_relationships(session, schema_data, table_nodes_map, column_nodes_map)
            
        print(f"Schema import process completed for group_id: {GROUP_ID}")


async def main():
    dotenv_path = os.path.join(project_root, 'backend', '.env')
    loaded = load_dotenv(dotenv_path=dotenv_path)
    if not loaded:
        print(f"Warning: Could not load .env file from {dotenv_path}")

    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    if not all([neo4j_uri, neo4j_user, neo4j_password]):
        print("Error: Missing Neo4j connection details in .env or environment.")
        return

    try:
        with open(SEMANTIC_MAPPING_FILE_PATH, 'r') as f:
            schema_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Semantic mapping file not found at {SEMANTIC_MAPPING_FILE_PATH}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {SEMANTIC_MAPPING_FILE_PATH}")
        return

    importer = DatabaseSchemaImporter(neo4j_uri, neo4j_user, neo4j_password)
    
    try:
        # Tidak perlu memanggil build_indices_and_constraints() dari Graphiti lagi
        # karena kita menggunakan driver Neo4j langsung dan _ensure_indexes menangani indeks.
        await importer.import_schema(schema_data)

    except neo4j_exceptions.ServiceUnavailable:
        print(f"Neo4j service unavailable at {neo4j_uri}. Ensure Neo4j is running.")
    except neo4j_exceptions.AuthError:
        print(f"Neo4j authentication failed for user '{neo4j_user}'. Check credentials.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await importer.close()

if __name__ == "__main__":
    asyncio.run(main())