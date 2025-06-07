# tests/orm/test_factory_system.py
import sys
import os
import traceback

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from backend.app.core.config import settings
from backend.factories.base import test_session_scope
from backend.app import db_models

def _run_test(engine, test_func, test_name):
    print(f"\n[TEST] Menjalankan: {test_name}...")
    try:
        with test_session_scope(engine) as (session, factory):
            test_func(session, factory)
        print(f"  [SUCCESS] Tes '{test_name}' berhasil.")
        return True
    except Exception as e:
        print(f"  [FAIL] Error pada '{test_name}': {e}")
        traceback.print_exc(file=sys.stdout)
        return False

def test_system_user_and_permissions(session, factory):
    """Menguji pembuatan User, Role, dan Menu."""
    # 1. Buat User dan Role
    user = factory.system.create("User", User="testuser")
    factory.system.create("Role", user=user, Role="ADMIN")
    session.commit()

    retrieved_user = session.query(db_models.User).filter_by(User="testuser").one()
    # Di sini kita bisa menambahkan assert jika ada relasi dari User ke Role
    # assert len(retrieved_user.roles) > 0

    print(f"    -> Berhasil membuat User '{retrieved_user.User}' dengan Role.")

    # 2. Buat Menu dan MenuList
    menu = factory.system.create("Menu", Role="ADMIN", Menu="TestMenu", SubMenu="TestSub")
    factory.system.create("MenuList", menu=menu)
    session.commit()

    retrieved_menu = session.query(db_models.Menu).filter_by(Menu="TestMenu").one()
    assert retrieved_menu is not None
    assert retrieved_menu.Role == "ADMIN"
    print(f"    -> Berhasil membuat Menu '{retrieved_menu.Menu}' untuk Role '{retrieved_menu.Role}'.")

def run_all_system_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk System (dengan validasi relasi)...")
    
    tests_to_run = {
        "System User and Permissions Creation": test_system_user_and_permissions,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL SYSTEM] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL SYSTEM] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False