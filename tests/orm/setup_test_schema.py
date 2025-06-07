# tests/orm/setup_test_schema.py
import sys
import os
import traceback

# Menambahkan path ke root proyek agar bisa impor 'backend'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from backend.app.core.config import settings
from backend.app.db_models import Base # Impor Base dari __init__.py di db_models

def create_test_schema():
    if not settings.TEST_DB_NAME:
        print("[ERROR] TEST_MYSQL_DATABASE tidak dikonfigurasi di .env. Tidak dapat membuat skema tes.", file=sys.stderr)
        return
    
    if settings.TEST_DB_NAME == settings.DB_NAME:
        confirm = input(
            f"PERINGATAN PENTING: Anda akan membuat skema di database '{settings.TEST_DB_NAME}', "
            f"yang SAMA dengan database utama Anda ('{settings.DB_NAME}').\n"
            "Ini akan MENGHAPUS SEMUA TABEL YANG ADA jika ada konflik nama.\n"
            "Apakah Anda benar-benar yakin ingin melanjutkan? (ketik 'YA' untuk melanjutkan): "
        )
        if confirm.upper() != 'YA':
            print("Operasi dibatalkan oleh pengguna.")
            return

    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )

    print(f"\n[INFO] Membuat koneksi ke database tes: {settings.TEST_DB_NAME} di {settings.TEST_DB_HOST}...")
    try:
        engine_test = create_engine(TEST_DATABASE_URL)
        
        # PERBAIKAN: AKTIFKAN BLOK INI UNTUK MEMASTIKAN SKEMA SEGAR
        print("[INFO] Menghapus semua tabel lama untuk memastikan skema sinkron...")
        Base.metadata.drop_all(bind=engine_test)
        print("[SUCCESS] Tabel lama berhasil dihapus.")
        
        print("[INFO] Membuat semua tabel berdasarkan model ORM...")
        Base.metadata.create_all(bind=engine_test)
        print(f"[SUCCESS] Semua tabel berhasil dibuat di database tes '{settings.TEST_DB_NAME}'.")
        
    except Exception as e:
        print(f"[ERROR] Gagal membuat skema di database tes: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    create_test_schema()