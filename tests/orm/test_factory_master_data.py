# tests/orm/test_factory_master_data.py
import sys
import os
import traceback
from sqlalchemy import create_engine
from decimal import Decimal

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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

def test_create_supplier(session, factory):
    """Menguji pembuatan MasterSupplier dengan dependensi otomatis."""
    supplier = factory.master.create("MasterSupplier")
    session.flush()
    
    assert supplier is not None
    assert supplier.country_ref is not None, "Relasi country_ref harus ada"
    assert supplier.city_ref is not None, "Relasi city_ref harus ada"
    assert supplier.currency_ref is not None, "Relasi currency_ref harus ada"
    print(f"    -> Berhasil membuat Supplier '{supplier.Name}' di Negara '{supplier.country_ref.Name}'")

def test_create_customer(session, factory):
    """Menguji pembuatan MasterCustomer dengan dependensi otomatis."""
    customer = factory.master.create("MasterCustomer")
    session.flush()

    assert customer is not None
    assert customer.country_ref is not None
    assert customer.customer_group_ref is not None
    assert customer.currency_ref is not None
    assert customer.price_list_type_ref is not None
    assert customer.sales_area1_ref is not None
    print(f"    -> Berhasil membuat Customer '{customer.Name}'")

def test_create_material(session, factory):
    """Menguji pembuatan MasterMaterial dengan dependensi otomatis."""
    material = factory.master.create("MasterMaterial")
    session.flush()

    assert material is not None
    assert material.smallest_unit_ref is not None
    assert material.sold_unit_ref is not None
    assert material.sku_unit_ref is not None
    assert material.group1_ref is not None
    assert material.type_ref is not None
    assert material.currency_ref is not None
    print(f"    -> Berhasil membuat Material '{material.Name}'")

def run_all_master_data_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Master Data...")
    
    tests_to_run = {
        "Supplier Creation": test_create_supplier,
        "Customer Creation": test_create_customer,
        "Material Creation": test_create_material,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL MASTER DATA] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL MASTER DATA] ❌ Gagal.")
        # Beri detail tes mana yang gagal
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False