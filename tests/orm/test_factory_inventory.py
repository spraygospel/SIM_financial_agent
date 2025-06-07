# tests/orm/test_factory_inventory.py
import sys
import os
import traceback
from decimal import Decimal

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

def test_stock_adjustment_and_relations(session, factory):
    """Menguji pembuatan alur Adjustment In/Out dan relasinya."""
    location = factory.master.create("MasterLocation", Code="WHADJ") # PERBAIKAN DI SINI
    material = factory.master.create("MasterMaterial", Code="MAT-ADJ")
    
    # 1. Uji Adjustment In
    adj_in_header = factory.inventory.create("AdjustInH", masterlocation=location, DocNo="AI-REL-TEST")
    factory.inventory.create("AdjustInD", adjustinh=adj_in_header, mastermaterial=material)
    session.commit()

    retrieved_adj_in = session.query(db_models.AdjustInH).filter_by(DocNo="AI-REL-TEST").one()
    assert len(retrieved_adj_in.details) == 1
    assert retrieved_adj_in.location_ref.Code == "WHADJ" # PERBAIKAN DI SINI
    assert retrieved_adj_in.details[0].material_ref.Code == "MAT-ADJ"
    print(f"    -> Berhasil membuat Adjustment In '{retrieved_adj_in.DocNo}' dan validasi relasi.")

    # 2. Uji Adjustment Out
    adj_out_header = factory.inventory.create("AdjustOutH", masterlocation=location, DocNo="AO-REL-TEST")
    factory.inventory.create("AdjustOutD", adjustouth=adj_out_header, mastermaterial=material)
    session.commit()
    
    retrieved_adj_out = session.query(db_models.AdjustOutH).filter_by(DocNo="AO-REL-TEST").one()
    assert len(retrieved_adj_out.details) == 1
    assert retrieved_adj_out.location_ref.Code == "WHADJ" # PERBAIKAN DI SINI
    assert retrieved_adj_out.details[0].material_ref.Code == "MAT-ADJ"
    print(f"    -> Berhasil membuat Adjustment Out '{retrieved_adj_out.DocNo}' dan validasi relasi.")

def test_batch_creation_and_relation(session, factory):
    """Menguji pembuatan Batch dan relasinya ke MasterMaterial."""
    material = factory.master.create("MasterMaterial", Code="MAT-BATCH")
    batch = factory.inventory.create("Batch", mastermaterial=material)
    session.commit()

    retrieved_batch = session.query(db_models.Batch).filter_by(MaterialCode="MAT-BATCH").one()
    assert retrieved_batch.material_ref is not None
    assert retrieved_batch.material_ref == material
    print(f"    -> Berhasil membuat Batch untuk Material '{retrieved_batch.MaterialCode}' dan validasi relasi.")


def run_all_inventory_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Inventory (dengan validasi relasi)...")
    
    tests_to_run = {
        "Stock Adjustment with Relations": test_stock_adjustment_and_relations,
        "Batch Creation with Relations": test_batch_creation_and_relation,
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