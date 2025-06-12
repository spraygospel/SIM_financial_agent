# backend/mcp_servers/graphiti_server/config.py

import os
from dotenv import load_dotenv

# Muat file .env dari direktori yang sama
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

class ServerSettings:
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str | None = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD: str | None = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE: str = os.getenv("NEO4J_DATABASE", "neo4j")
    SCHEMA_GROUP_ID: str = os.getenv("SCHEMA_GROUP_ID", "sim_testgeluran_schema")

settings = ServerSettings()