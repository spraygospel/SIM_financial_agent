# tests/orm/test_factory_inventory.py
import sys
import os
import traceback

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from backend.app.core.config import settings
from backend.factories.base import test_session_scope

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

def test_create_stock(session, factory):
    """Menguji pembuatan record Stock."""
    stock_record = factory.inventory.create("Stock")
    session.flush()
    
    assert stock_record is not None
    assert stock_record.material_ref is not None
    assert stock_record.location_ref is not None
    print(f"    -> Berhasil membuat record Stock untuk Material '{stock_record.MaterialCode}'")

def test_create_stock_balance(session, factory):
    """Menguji pembuatan record StockBalance."""
    stock_balance_record = factory.inventory.create("StockBalance")
    session.flush()

    assert stock_balance_record is not None
    assert stock_balance_record.material_ref is not None
    assert stock_balance_record.location_ref is not None
    print(f"    -> Berhasil membuat record StockBalance untuk Material '{stock_balance_record.MaterialCode}'")

def run_all_inventory_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Inventory...")
    
    tests_to_run = {
        "Stock Creation": test_create_stock,
        "StockBalance Creation": test_create_stock_balance,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL INVENTORY] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL INVENTORY] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False