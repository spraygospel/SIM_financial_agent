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

def test_po_creation_and_relations(session, factory):
    """Menguji pembuatan PurchaseOrderH/D dan validasi relasi dua arah."""
    # 1. Buat data master spesifik
    supplier = factory.master.create("MasterSupplier", Code="SUP-PO-01") # PERBAIKAN DI SINI
    material = factory.master.create("MasterMaterial", Code="MAT-PO-TEST")
    
    # 2. Buat objek utama dan detailnya
    po_header = factory.purchase.create("PurchaseOrderH", mastersupplier=supplier, DocNo="PO-REL-TEST")
    factory.purchase.create("PurchaseOrderD", purchaseorderh=po_header, mastermaterial=material, Number=1)
    
    session.commit()

    # 3. Ambil kembali dari DB dan validasi
    retrieved_po = session.query(db_models.PurchaseOrderH).filter_by(DocNo="PO-REL-TEST").one()
    retrieved_supplier = session.query(db_models.MasterSupplier).filter_by(Code="SUP-PO-01").one() # PERBAIKAN DI SINI

    assert len(retrieved_po.details) == 1
    assert retrieved_po.supplier_ref == retrieved_supplier
    assert retrieved_po in retrieved_supplier.purchase_orders
    assert retrieved_po.details[0].material_ref.Code == "MAT-PO-TEST"
    print(f"    -> Berhasil membuat PO '{retrieved_po.DocNo}' dan memvalidasi relasinya.")

def test_purchase_return_with_relations(session, factory):
    """Menguji pembuatan PurchaseReturnH/D dan validasi relasi dua arah."""
    supplier = factory.master.create("MasterSupplier", Code="SUP-PR-01") # PERBAIKAN DI SINI
    return_header = factory.purchase.create("PurchaseReturnH", mastersupplier=supplier, DocNo="PR-REL-TEST")
    factory.purchase.create("PurchaseReturnD", purchasereturnh=return_header, Number=1)
    session.commit()

    retrieved_pr = session.query(db_models.PurchaseReturnH).filter_by(DocNo="PR-REL-TEST").one()
    assert len(retrieved_pr.details) == 1
    assert retrieved_pr.supplier_ref.Code == "SUP-PR-01" # PERBAIKAN DI SINI
    print(f"    -> Berhasil membuat Purchase Return '{retrieved_pr.DocNo}' dan memvalidasi relasinya.")

def run_all_purchase_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Purchase (dengan validasi relasi)...")
    
    tests_to_run = {
        "PO Creation with Relations": test_po_creation_and_relations,
        "Purchase Return with Relations": test_purchase_return_with_relations,
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