# File: scripts/initialize_db_mysql.py

import os
import sys
from sqlalchemy import create_engine, text

# --- Setup Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ------------------

try:
    from backend.app.core.config import settings
    from backend.mcp_servers.mysql_server.db_models import Base
    print("Successfully imported settings and ORM Base.")
except ImportError as e:
    print(f"Error during import: {e}")
    sys.exit(1)

def initialize_database():
    """
    Membuat semua tabel berdasarkan ORM dan mengisi data dari data.sql
    ke database development (bukan tes).
    """
    db_url = settings.DATABASE_URL
    if not db_url:
        print("Error: DATABASE_URL not configured in .env file.")
        return
        
    print(f"Connecting to DEVELOPMENT database: {settings.DB_HOST}/{settings.DB_NAME}")
    
    try:
        engine = create_engine(db_url)
    except Exception as e:
        print(f"Failed to create engine: {e}")
        return

    # 1. Buat semua tabel berdasarkan model ORM
    print("Creating tables based on ORM models...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (or already exist).")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")
        return

    # 2. Baca dan jalankan file data.sql
    data_sql_path = os.path.join(project_root, 'data_samples', 'data.sql')
    if not os.path.exists(data_sql_path):
        print(f"Error: data.sql not found at {data_sql_path}")
        return
        
    print(f"Populating data from {data_sql_path}...")
    try:
        with open(data_sql_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        with engine.connect() as connection:
            # Pisahkan perintah berdasarkan ';' dan filter yang kosong
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            for statement in statements:
                connection.execute(text(statement))
            # Untuk SQLAlchemy 2.0, commit terjadi secara otomatis saat blok 'with' selesai
            # Jika menggunakan versi lama atau ingin eksplisit: connection.commit()
        print("Data populated successfully.")
    except Exception as e:
        print(f"An error occurred during data population: {e}")

    print("\nDevelopment database initialization complete.")

if __name__ == "__main__":
    initialize_database()