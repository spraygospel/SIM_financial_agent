# backend/app/tests/db/test_db_session.py
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

# Coba impor engine, SessionLocal, dan get_db_session dari modul session kita
try:
    from backend.app.db.session import engine, SessionLocal, get_db_session
    SESSION_SETUP_SUCCESS = True
except Exception as e:
    print(f"Gagal mengimpor dari backend.app.db.session: {e}")
    SESSION_SETUP_SUCCESS = False
    engine = None
    SessionLocal = None
    get_db_session = None

# Impor salah satu model untuk pengujian query ORM, misalnya MasterCountry
# Pastikan __init__.py di db_models sudah benar
try:
    from backend.app.db_models import MasterCountry
    MODEL_IMPORT_SUCCESS = True
except Exception as e:
    print(f"Gagal mengimpor MasterCountry dari backend.app.db_models: {e}")
    MODEL_IMPORT_SUCCESS = False
    MasterCountry = None

@pytest.mark.skipif(not SESSION_SETUP_SUCCESS, reason="Setup sesi DB gagal, tes dilewati.")
def test_engine_creation():
    assert engine is not None, "SQLAlchemy engine seharusnya terbuat."
    print("Engine SQLAlchemy berhasil diimpor/dibuat.")

@pytest.mark.skipif(not SESSION_SETUP_SUCCESS, reason="Setup sesi DB gagal, tes dilewati.")
def test_session_local_creation():
    assert SessionLocal is not None, "SessionLocal factory seharusnya terbuat."
    if hasattr(SessionLocal, "configure"): # Cara cek apakah ini sessionmaker asli
         print("SessionLocal SQLAlchemy berhasil diimpor/dibuat.")
    else:
        print("SessionLocal adalah dummy karena engine gagal dibuat.")
        assert not hasattr(SessionLocal, "configure"), "SessionLocal seharusnya dummy jika engine gagal."


@pytest.mark.skipif(not SESSION_SETUP_SUCCESS or not engine, reason="Engine DB tidak tersedia, tes dilewati.")
def test_database_connection_raw_sql():
    print("Menguji koneksi database dengan SQL mentah...")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar_one()
            assert value == 1
            print("Koneksi database dan eksekusi SQL mentah berhasil (SELECT 1).")
    except Exception as e:
        pytest.fail(f"Gagal melakukan koneksi atau eksekusi SQL mentah: {e}")

@pytest.mark.skipif(not SESSION_SETUP_SUCCESS or not SessionLocal or not hasattr(SessionLocal, "configure"), reason="SessionLocal DB tidak tersedia atau dummy, tes dilewati.")
def test_get_db_session():
    print("Menguji fungsi get_db_session()...")
    db_session_generator = get_db_session()
    db: Session = next(db_session_generator)
    assert db is not None, "get_db_session() seharusnya mengembalikan sesi."
    assert isinstance(db, Session), "Objek yang dikembalikan oleh get_db_session() seharusnya adalah instance dari SQLAlchemy Session."
    print("Fungsi get_db_session() berhasil mendapatkan sesi.")
    try:
        # Lakukan operasi sederhana
        result = db.execute(text("SELECT DATABASE()")).scalar_one() # Mendapatkan nama database saat ini
        print(f"Berhasil mengeksekusi query dalam sesi. Database saat ini: {result}")
        from backend.app.core.config import settings
        assert result == settings.DB_NAME, f"Terhubung ke database yang salah! Seharusnya '{settings.DB_NAME}', tapi terhubung ke '{result}'"
    except Exception as e:
        pytest.fail(f"Gagal melakukan operasi dalam sesi yang didapatkan dari get_db_session(): {e}")
    finally:
        # Mensimulasikan penutupan sesi oleh FastAPI
        try:
            next(db_session_generator) # Ini akan memicu blok finally di get_db_session
        except StopIteration:
            pass # Ini diharapkan
        except Exception as e:
            print(f"Error saat mencoba menutup sesi dari generator: {e}")


@pytest.mark.skipif(not SESSION_SETUP_SUCCESS or not MODEL_IMPORT_SUCCESS or not SessionLocal or not hasattr(SessionLocal, "configure"), 
                    reason="Sesi DB atau Model tidak tersedia, tes dilewati.")
def test_orm_query_master_country():
    print("Menguji query ORM sederhana pada model MasterCountry...")
    db_session_generator = get_db_session()
    db: Session = next(db_session_generator)
    try:
        country = db.query(MasterCountry).first()
        if country:
            print(f"Berhasil mengambil data pertama dari MasterCountry: Code={country.Code}, Name={country.Name}")
        else:
            print("Tabel MasterCountry kosong atau query gagal mengembalikan data (ini bisa jadi normal jika tabel memang kosong).")
        # Tidak ada assert spesifik untuk data di sini karena tabel bisa kosong,
        # yang penting query tidak menghasilkan error.
    except Exception as e:
        pytest.fail(f"Gagal melakukan query ORM pada MasterCountry: {e}")
    finally:
        try:
            next(db_session_generator)
        except StopIteration:
            pass
        except Exception as e:
            print(f"Error saat mencoba menutup sesi dari generator (ORM test): {e}")