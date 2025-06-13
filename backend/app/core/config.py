# backend/app/core/config.py
import sys
from pathlib import Path

def load_config_from_txt() -> dict:
    """
    Mencari dan mem-parsing config.txt, lalu mengembalikannya sebagai dictionary.
    """
    # Mencari file config.txt di root folder 'backend'
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.txt'
    
    if not config_path.is_file():
        print("KRITIS: File 'backend/config.txt' tidak ditemukan!", file=sys.stderr)
        return {}

    print(f"--- [CONFIG] Membaca konfigurasi dari: {config_path} ---")
    config = {}
    with open(config_path, 'r') as f:
        for line in f:
            # Abaikan baris kosong atau baris komentar
            if line.strip() and not line.strip().startswith('#'):
                try:
                    key, value = line.strip().split('=', 1)
                    # Hapus tanda kutip jika ada
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    config[key.strip()] = value.strip()
                except ValueError:
                    # Abaikan baris yang tidak memiliki format KEY=VALUE
                    pass
    return config

# --- Muat konfigurasi sekali saja saat modul ini diimpor ---
_config_data = load_config_from_txt()

class Settings:
    PROJECT_NAME: str = "AI Agent SQL Query"
    PROJECT_VERSION: str = "0.1.0"

    # Ambil nilai dari dictionary yang sudah dimuat
    LLM_API_KEY: str | None = _config_data.get("DEEPSEEK_API_KEY")
    LLM_API_BASE_URL: str | None = _config_data.get("DEEPSEEK_API_BASE_URL")
    LLM_MODEL_NAME: str | None = _config_data.get("DEEPSEEK_MODEL", "deepseek-chat")

    DB_HOST: str | None = _config_data.get("MYSQL_HOST")
    DB_USER: str | None = _config_data.get("MYSQL_USER")
    DB_PASSWORD: str | None = _config_data.get("MYSQL_PASSWORD")
    DB_NAME: str | None = _config_data.get("MYSQL_DATABASE")
    DB_PORT: int = int(_config_data.get("MYSQL_PORT", 3306))

    @property
    def DATABASE_URL(self) -> str:
        if all([self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return ""

    # --- PENAMBAHAN KEMBALI VARIABEL YANG HILANG ---
    NEO4J_URI: str | None = _config_data.get("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str | None = _config_data.get("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str | None = _config_data.get("NEO4J_PASSWORD")
    NEO4J_DATABASE: str | None = _config_data.get("NEO4J_DATABASE", "neo4j")
    SCHEMA_GROUP_ID: str | None = _config_data.get("SCHEMA_GROUP_ID", "sim_testgeluran_schema")
    # -----------------------------------------------

# Buat satu instance untuk diimpor di seluruh aplikasi
settings = Settings()

# Verifikasi saat startup
if not settings.LLM_API_KEY:
    print("PERINGATAN: DEEPSEEK_API_KEY tidak ditemukan di config.txt", file=sys.stderr)
if not settings.DATABASE_URL:
     print("PERINGATAN: Konfigurasi MYSQL_* tidak lengkap di config.txt", file=sys.stderr)
if not settings.NEO4J_PASSWORD:
     print("PERINGATAN: NEO4J_PASSWORD tidak ditemukan di config.txt", file=sys.stderr)