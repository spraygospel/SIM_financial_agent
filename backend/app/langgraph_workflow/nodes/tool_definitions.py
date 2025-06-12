# backend/app/langgraph_workflow/nodes/tool_definitions.py
from backend.app.tools import database_tools, graphiti_tools

search_read_schema = database_tools.SearchReadInput.model_json_schema()
if 'title' in search_read_schema: del search_read_schema['title']

# --- TAMBAHKAN INI ---
get_schema_schema = graphiti_tools.GetRelevantSchemaInput.model_json_schema()
if 'title' in get_schema_schema: del get_schema_schema['title']
# --------------------

tools_definition = [
    # --- TAMBAHKAN TOOL INI DI POSISI PERTAMA ---
    {
        "type": "function",
        "function": {
            "name": "get_relevant_schema",
            "description": "WAJIB DIGUNAKAN PERTAMA KALI. Mengambil 'peta data' (skema, kolom, relasi) yang relevan sebelum membuat query.",
            "parameters": {
                "type": "object",
                "properties": {"payload": get_schema_schema},
                "required": ["payload"]
            }
        }
    },
    # --------------------------------------------
    {
        "type": "function",
        "function": {
            "name": "search_read",
            "description": "Mencari dan membaca data dari database. Gunakan ini SETELAH mendapatkan skema.",
            "parameters": {
                "type": "object",
                "properties": {"payload": search_read_schema},
                "required": ["payload"]
            }
        }
    }
]