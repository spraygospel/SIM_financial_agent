# backend/app/core/config.py
import os
from dotenv import load_dotenv
from pathlib import Path
import sys 
from typing import Optional 

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "AI Agent SQL Query"
    PROJECT_VERSION: str = "0.1.0"

    LLM_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    LLM_API_BASE_URL: Optional[str] = os.getenv("DEEPSEEK_API_BASE_URL") 
    LLM_MODEL_NAME: Optional[str] = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # --- TAMBAHKAN/PASTIKAN BAGIAN INI ADA DAN BENAR ---
    DB_HOST: Optional[str] = os.getenv("MYSQL_HOST")
    DB_USER: Optional[str] = os.getenv("MYSQL_USER")
    DB_PASSWORD: Optional[str] = os.getenv("MYSQL_PASSWORD")
    DB_NAME: Optional[str] = os.getenv("MYSQL_DATABASE") # Ini adalah database ERP Anda, misal 'sim_testgeluran'
    DB_PORT: int = int(os.getenv("MYSQL_PORT", 3306)) # Default port MySQL

    TEST_DB_HOST: Optional[str] = os.getenv("TEST_MYSQL_HOST", DB_HOST) # Default ke DB_HOST jika tidak diset
    TEST_DB_USER: Optional[str] = os.getenv("TEST_MYSQL_USER", DB_USER)
    TEST_DB_PASSWORD: Optional[str] = os.getenv("TEST_MYSQL_PASSWORD", DB_PASSWORD)
    TEST_DB_NAME: Optional[str] = os.getenv("TEST_MYSQL_DATABASE") # Ini harus diset spesifik
    TEST_DB_PORT: int = int(os.getenv("TEST_MYSQL_PORT", DB_PORT))

    NEO4J_URI: Optional[str] = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: Optional[str] = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: Optional[str] = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE: Optional[str] = os.getenv("NEO4J_DATABASE", "neo4j") 
    SCHEMA_GROUP_ID: Optional[str] = os.getenv("SCHEMA_GROUP_ID", "sim_testgeluran_schema")
    # --- AKHIR BAGIAN YANG DIPASTIKAN ---

    MYSQL_MCP_SERVER_URL: Optional[str] = os.getenv("MYSQL_MCP_SERVER_URL", "http://localhost:8001") 
    GRAPHITI_MCP_SERVER_URL: Optional[str] = os.getenv("GRAPHITI_MCP_SERVER_URL", "http://localhost:8002") 
    PLACEHOLDER_MCP_SERVER_URL: Optional[str] = os.getenv("PLACEHOLDER_MCP_SERVER_URL", "http://localhost:8003") 

settings = Settings()

# Pengecekan variabel penting
if not settings.LLM_API_KEY:
    print("PERINGATAN: DEEPSEEK_API_KEY tidak ditemukan di .env.", file=sys.stderr)
if not settings.LLM_API_BASE_URL: 
    print("PERINGATAN: DEEPSEEK_API_BASE_URL tidak ditemukan di .env.", file=sys.stderr)
if not settings.LLM_MODEL_NAME: 
    print("PERINGATAN: DEEPSEEK_MODEL tidak ditemukan di .env.", file=sys.stderr)

if not all([settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME]):
    print("PERINGATAN: Satu atau lebih variabel koneksi MySQL (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE) tidak diset di .env. Node execute_query mungkin gagal.", file=sys.stderr)

if not all([settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD, settings.SCHEMA_GROUP_ID]):
    print("PERINGATAN: Satu atau lebih variabel koneksi Neo4j/Graphiti tidak diset di .env. Node consult_schema mungkin gagal.", file=sys.stderr)
if not settings.TEST_DB_NAME:
    print("PERINGATAN: TEST_MYSQL_DATABASE tidak diset di .env. Tes database mungkin gagal atau menggunakan database yang salah.", file=sys.stderr)
elif settings.TEST_DB_NAME == settings.DB_NAME:
    print(f"PERINGATAN PENTING: TEST_MYSQL_DATABASE ('{settings.TEST_DB_NAME}') sama dengan MYSQL_DATABASE ('{settings.DB_NAME}'). Ini berisiko merusak data development/produksi saat testing. Pastikan Anda menggunakan database terpisah untuk tes!", file=sys.stderr)