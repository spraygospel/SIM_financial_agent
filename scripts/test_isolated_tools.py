# scripts/test_isolated_tools.py
import asyncio
import json
from pprint import pprint

# Penting: Tambahkan path root proyek agar bisa impor modul backend
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Impor tools dan model Pydantic yang relevan
from backend.app.tools import graphiti_tools, database_tools
from backend.app.tools.database_tools import ExecutePlanInput, DatabaseOperation

async def run_isolated_tests():
    """Menjalankan tes terisolasi untuk setiap tool."""
    print("--- Memulai Tes Terisolasi untuk Tools ---")

    # --- Tes 1: get_relevant_schema (Graphiti/Neo4j) ---
    print("\n🔄 [Tes 1] Menguji tool 'get_relevant_schema'...")
    try:
        # Kita pura-pura LLM meminta skema untuk 'mastercustomer'
        schema_input = graphiti_tools.GetRelevantSchemaInput(entities=["mastercustomer"])
        schema_result = await graphiti_tools.get_relevant_schema(schema_input)
        
        if schema_result.success:
            print("✅ 'get_relevant_schema' BERHASIL.")
            print("Skema yang ditemukan untuk 'mastercustomer':")
            # Menggunakan .model_dump_json() untuk pretty print
            print(schema_result.model_dump_json(indent=2))
        else:
            print(f"🔥 'get_relevant_schema' GAGAL. Error: {schema_result.error}")
    except Exception as e:
        print(f"🔥 Terjadi exception saat menguji 'get_relevant_schema': {e}")


    # --- Tes 2: execute_database_plan (MySQL) ---
    print("\n🔄 [Tes 2] Menguji tool 'execute_database_plan'...")
    try:
        # Kita buat rencana manual untuk mengambil 2 customer, meniru permintaan E2E
        manual_plan = ExecutePlanInput(
            operations=[
                DatabaseOperation(
                    operation_id="get_two_customers",
                    main_table="mastercustomer",
                    select_columns=[
                        {"field_name": "mastercustomer.Code", "alias": "CustomerCode"},
                        {"field_name": "mastercustomer.Name", "alias": "CustomerName"}
                    ],
                    limit=2
                )
            ]
        )

        db_result = database_tools.execute_database_plan(manual_plan)
        
        if db_result.get("success"):
            print("✅ 'execute_database_plan' BERHASIL.")
            print("Hasil dari database:")
            pprint(db_result)
        else:
            print(f"🔥 'execute_database_plan' GAGAL. Error: {db_result.get('error')}")

    except Exception as e:
        print(f"🔥 Terjadi exception saat menguji 'execute_database_plan': {e}")
    
    print("\n--- Tes Terisolasi Selesai ---")

if __name__ == "__main__":
    asyncio.run(run_isolated_tests())