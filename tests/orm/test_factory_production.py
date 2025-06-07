# tests/orm/test_factory_production.py
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

def test_create_production_flow(session, factory):
    """Menguji alur produksi: JobOrder -> MaterialUsage -> JobResult."""
    # 1. Buat Job Order
    job_order = factory.production.create("JobOrder")
    session.flush() # PERBAIKAN: Flush untuk menyimpan Job Order
    assert job_order is not None
    print(f"    -> Berhasil membuat Job Order: {job_order.DocNo}")

    # 2. Buat Material Usage berdasarkan Job Order tersebut
    usage_header = factory.production.create("MaterialUsageH", joborder=job_order)
    factory.production.create("MaterialUsageD", materialusageh=usage_header)
    session.flush() # PERBAIKAN: Flush untuk menyimpan Material Usage
    assert len(usage_header.details) == 1
    print(f"    -> Berhasil membuat Material Usage: {usage_header.DocNo}")

    # 3. Buat Job Result berdasarkan Job Order yang sama
    result_header = factory.production.create("JobResultH", joborder=job_order)
    session.flush() # PERBAIKAN: Flush untuk menyimpan Job Result Header

    # 4. Buat Job Result Detail
    factory.production.create("JobResultD", jobresulth=result_header)
    session.flush() # PERBAIKAN: Flush untuk menyimpan Job Result Detail

    assert len(result_header.details) == 1
    # Verifikasi bahwa material di JobResultD sama dengan material di JobOrder
    assert result_header.details[0].MaterialCode == job_order.MaterialCode
    print(f"    -> Berhasil membuat Job Result: {result_header.DocNo}")

def run_all_production_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Production...")
    
    tests_to_run = {
        "Full Production Flow Creation": test_create_production_flow,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL PRODUCTION] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL PRODUCTION] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False