# backend/app/db/session.py
import sys
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import settings

# --- Engine untuk Database Utama (Development/Produksi) ---
if not all([settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME]):
    print(
        "PERINGATAN: Variabel koneksi database utama (MYSQL_...) belum lengkap di .env. "
        "Operasi database utama akan gagal.",
        file=sys.stderr
    )
    engine = None
else:
    DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

# --- Engine untuk Database Tes ---
if not all([settings.TEST_DB_HOST, settings.TEST_DB_USER, settings.TEST_DB_PASSWORD, settings.TEST_DB_NAME]):
    print(
        "PERINGATAN: Variabel koneksi database tes (TEST_MYSQL_...) belum lengkap di .env. "
        "Pengujian ORM akan gagal.",
        file=sys.stderr
    )
    engine_test = None
else:
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine_test = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)

# --- Session Makers ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
SessionTestLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test) if engine_test else None

# --- Dependency Functions ---
def get_db_session() -> Iterator[Session]:
    """
    Generator untuk menyediakan sesi database utama ke endpoint FastAPI.
    """
    if not SessionLocal:
        raise RuntimeError("Sesi database utama tidak dapat dibuat. Periksa konfigurasi .env.")
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db_session() -> Iterator[Session]:
    """
    Generator untuk menyediakan sesi database tes untuk skrip pengujian.
    """
    if not SessionTestLocal:
        raise RuntimeError("Sesi database tes tidak dapat dibuat. Periksa konfigurasi TEST_MYSQL_... di .env.")
    db: Session = SessionTestLocal()
    try:
        yield db
    finally:
        db.close()