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

def test_production_flow_and_relations(session, factory):
    """Menguji alur produksi dan validasi relasi dua arahnya."""
    # 1. Buat data prasyarat
    job_order = factory.production.create("JobOrder", DocNo="JO-REL-TEST")
    session.commit()

    # 2. Buat Material Usage dan validasi relasinya
    usage_header = factory.production.create("MaterialUsageH", joborder=job_order, DocNo="MU-REL-TEST")
    factory.production.create("MaterialUsageD", materialusageh=usage_header, Number=1)
    session.commit()

    retrieved_usage = session.query(db_models.MaterialUsageH).filter_by(DocNo="MU-REL-TEST").one()
    assert retrieved_usage.job_order_ref is not None, "Relasi MU -> JO tidak boleh None"
    assert retrieved_usage.job_order_ref.DocNo == "JO-REL-TEST"
    print(f"    -> Berhasil membuat Material Usage '{retrieved_usage.DocNo}' dan memvalidasi relasi ke Job Order.")

    # 3. Buat Job Result dan validasi relasinya
    result_header = factory.production.create("JobResultH", joborder=job_order, DocNo="JR-REL-TEST")
    factory.production.create("JobResultD", jobresulth=result_header, Number=1)
    session.commit()

    retrieved_result = session.query(db_models.JobResultH).filter_by(DocNo="JR-REL-TEST").one()
    retrieved_jo = session.query(db_models.JobOrder).filter_by(DocNo="JO-REL-TEST").one()

    assert retrieved_result.job_order_ref == retrieved_jo
    assert retrieved_result in retrieved_jo.job_results, "Relasi balik JO -> JR harus benar"
    assert len(retrieved_result.details) == 1
    assert retrieved_result.details[0].header == retrieved_result
    print(f"    -> Berhasil membuat Job Result '{retrieved_result.DocNo}' dan memvalidasi relasi dua arahnya.")


def run_all_production_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Production (dengan validasi relasi)...")
    
    tests_to_run = {
        "Production Flow with Relations": test_production_flow_and_relations,
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