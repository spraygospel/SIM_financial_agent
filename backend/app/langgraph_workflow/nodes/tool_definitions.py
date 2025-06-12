# backend/app/langgraph_workflow/nodes/tool_definitions.py
from backend.app.tools import database_tools, graphiti_tools

# Ambil skema JSON dari model Pydantic
db_plan_schema = database_tools.ExecutePlanInput.model_json_schema()
graphiti_schema = graphiti_tools.GetRelevantSchemaInput.model_json_schema()

# Hapus properti 'title' yang tidak perlu dari skema yang dihasilkan Pydantic
if 'title' in db_plan_schema:
    del db_plan_schema['title']
if 'title' in graphiti_schema:
    del graphiti_schema['title']


tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "execute_database_plan",
            "description": "Menerima dan mengeksekusi satu atau lebih operasi database menggunakan ORM untuk mengambil data dari database.",
            # --- PERBAIKAN DI SINI ---
            # LLM harus mengirim argumen yang isinya adalah 'payload'
            "parameters": {
                "type": "object",
                "properties": {
                    "payload": db_plan_schema
                },
                "required": ["payload"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_relevant_schema",
            "description": "Mengambil 'peta data' (skema, kolom, relasi) yang relevan dari knowledge graph.",
            # --- PERBAIKAN DI SINI ---
            "parameters": {
                "type": "object",
                "properties": {
                    "payload": graphiti_schema
                },
                "required": ["payload"]
            }
        }
    }
]