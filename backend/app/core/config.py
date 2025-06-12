# File: backend/app/core/config.py

import os
from dotenv import load_dotenv
from pathlib import Path
import sys 
from typing import Optional 

# Menggunakan Path untuk membuat path ke .env menjadi lebih robust
# Ini akan mencari file .env di root proyek (satu level di atas folder 'backend')
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "AI Agent SQL Query"
    PROJECT_VERSION: str = "0.1.0"

    # --- Konfigurasi LLM ---
    LLM_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    LLM_API_BASE_URL: Optional[str] = os.getenv("DEEPSEEK_API_BASE_URL") 
    LLM_MODEL_NAME: Optional[str] = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # --- Konfigurasi Database Utama (Development/Production) ---
    DB_HOST: Optional[str] = os.getenv("MYSQL_HOST")
    DB_USER: Optional[str] = os.getenv("MYSQL_USER")
    DB_PASSWORD: Optional[str] = os.getenv("MYSQL_PASSWORD")
    DB_NAME: Optional[str] = os.getenv("MYSQL_DATABASE")
    DB_PORT: int = int(os.getenv("MYSQL_PORT", 3306))

    @property
    def DATABASE_URL(self) -> str:
        """Mendapatkan URL koneksi database utama secara dinamis."""
        # Pastikan kita punya semua bagian sebelum mencoba membuat URL
        if all([self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return "" # Kembalikan string kosong jika ada yang kurang

    # --- Konfigurasi Database Testing ---
    TEST_DB_HOST: Optional[str] = os.getenv("TEST_MYSQL_HOST", DB_HOST)
    TEST_DB_USER: Optional[str] = os.getenv("TEST_MYSQL_USER", DB_USER)
    TEST_DB_PASSWORD: Optional[str] = os.getenv("TEST_MYSQL_PASSWORD", DB_PASSWORD)
    TEST_DB_NAME: Optional[str] = os.getenv("TEST_MYSQL_DATABASE")
    TEST_DB_PORT: int = int(os.getenv("TEST_MYSQL_PORT", DB_PORT))

    @property
    def TEST_DATABASE_URL(self) -> str:
        """Mendapatkan URL koneksi database tes secara dinamis."""
        # Pastikan kita punya semua bagian sebelum mencoba membuat URL
        if all([self.TEST_DB_HOST, self.TEST_DB_USER, self.TEST_DB_PASSWORD, self.TEST_DB_NAME]):
            return f"mysql+pymysql://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return "" # Kembalikan string kosong jika ada yang kurang

    # --- Konfigurasi Neo4j / Graphiti ---
    NEO4J_URI: Optional[str] = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: Optional[str] = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: Optional[str] = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE: Optional[str] = os.getenv("NEO4J_DATABASE", "neo4j") 
    SCHEMA_GROUP_ID: Optional[str] = os.getenv("SCHEMA_GROUP_ID", "sim_testgeluran_schema")

    # --- Konfigurasi URL Server MCP ---
    MYSQL_MCP_SERVER_URL: Optional[str] = os.getenv("MYSQL_MCP_SERVER_URL", "http://localhost:8001") 
    GRAPHITI_MCP_SERVER_URL: Optional[str] = os.getenv("GRAPHITI_MCP_SERVER_URL", "http://localhost:8002") 
    # Placeholder server ditiadakan karena fungsionalitasnya akan diintegrasikan
    # ke dalam node LangGraph `replace_placeholders`
    # PLACEHOLDER_MCP_SERVER_URL: Optional[str] = os.getenv("PLACEHOLDER_MCP_SERVER_URL", "http://localhost:8003") 

# Buat satu instance dari Settings untuk diimpor di seluruh aplikasi
settings = Settings()

# --- Pengecekan Variabel Penting Saat Startup ---
# Ini akan memberi peringatan saat aplikasi dimulai jika ada konfigurasi yang hilang.

def check_env_vars():
    print("--- Memeriksa Variabel Lingkungan ---")
    warnings = []
    
    # Cek LLM
    if not settings.LLM_API_KEY or not settings.LLM_API_BASE_URL:
        warnings.append("Koneksi LLM (DEEPSEEK_*) tidak lengkap. Agent mungkin tidak bisa berpikir.")
    
    # Cek DB Utama
    if not settings.DATABASE_URL:
        warnings.append("Koneksi Database Utama (MYSQL_*) tidak lengkap. Aplikasi utama mungkin gagal.")
    
    # Cek DB Tes
    if not settings.TEST_DATABASE_URL:
        warnings.append("Koneksi Database Tes (TEST_MYSQL_*) tidak lengkap. Skrip validasi akan gagal.")
    elif settings.TEST_DB_NAME == settings.DB_NAME:
        warnings.append(f"PENTING: TEST_MYSQL_DATABASE ('{settings.TEST_DB_NAME}') sama dengan MYSQL_DATABASE ('{settings.DB_NAME}'). Berisiko merusak data!")

    # Cek Neo4j
    if not all([settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD]):
        warnings.append("Koneksi Neo4j/Graphiti (NEO4J_*) tidak lengkap. Agent mungkin tidak bisa mengakses skema.")
    
    if warnings:
        print("PERINGATAN KONFIGURASI:", file=sys.stderr)
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}", file=sys.stderr)
    else:
        print("Semua variabel lingkungan penting terdeteksi.")
    print("------------------------------------")

# Anda bisa memanggil check_env_vars() di main.py nanti jika perlu,
# atau cukup jalankan file ini langsung untuk mengecek (`python backend/app/core/config.py`)