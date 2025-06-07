# tests/orm/test_factory_purchase.py
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

def test_create_po_header(session, factory):
    """Menguji pembuatan PurchaseOrderH dengan dependensi otomatis."""
    po_header = factory.purchase.create("PurchaseOrderH")
    session.flush()
    
    assert po_header is not None
    assert po_header.supplier_ref is not None
    print(f"    -> Berhasil membuat PO Header '{po_header.DocNo}' untuk Supplier '{po_header.supplier_ref.Name}'")

def test_create_po_with_details(session, factory):
    """Menguji pembuatan PO lengkap dengan detail."""
    po_header = factory.purchase.create("PurchaseOrderH")
    
    # Buat 3 baris detail untuk PO ini
    factory.purchase.create("PurchaseOrderD", purchaseorderh=po_header, Number=1)
    factory.purchase.create("PurchaseOrderD", purchaseorderh=po_header, Number=2)
    factory.purchase.create("PurchaseOrderD", purchaseorderh=po_header, Number=3)
    
    session.flush()

    assert len(po_header.details) == 3
    print(f"    -> Berhasil membuat PO '{po_header.DocNo}' dengan {len(po_header.details)} baris detail.")

def test_create_purchase_return_with_details(session, factory):
    """Menguji pembuatan PurchaseReturnH dengan detailnya."""
    return_header = factory.purchase.create("PurchaseReturnH")
    session.flush()

    factory.purchase.create("PurchaseReturnD", purchasereturnh=return_header, Number=1)
    session.flush()

    assert len(return_header.details) == 1
    print(f"    -> Berhasil membuat Purchase Return '{return_header.DocNo}' dengan {len(return_header.details)} baris detail.")

def run_all_purchase_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Purchase...")
    
    tests_to_run = {
        "PO Header Creation": test_create_po_header,
        "PO with Details Creation": test_create_po_with_details,
        "Purchase Return Creation": test_create_purchase_return_with_details, 
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL PURCHASE] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL PURCHASE] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False