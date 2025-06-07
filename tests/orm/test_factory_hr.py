# tests/orm/test_factory_hr.py
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

def test_create_hr_documents(session, factory):
    """Menguji pembuatan dokumen-dokumen HR."""
    # 1. Uji Change Shift
    change_shift_h = factory.hr.create("HrChangeShiftH")
    factory.hr.create("HrChangeShiftD", hrchangeshifth=change_shift_h)
    session.flush()
    assert len(change_shift_h.details) == 1
    print(f"    -> Berhasil membuat Change Shift '{change_shift_h.DocNo}'")

    # 2. Uji Overtime
    overtime_h = factory.hr.create("HrOvertimeH")
    factory.hr.create("HrOvertimeD", hrovertimeh=overtime_h)
    session.flush()
    assert len(overtime_h.details) == 1
    print(f"    -> Berhasil membuat Overtime '{overtime_h.DocNo}'")

def run_all_hr_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk HR...")
    
    tests_to_run = {
        "HR Document Creation": test_create_hr_documents,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL HR] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL HR] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False