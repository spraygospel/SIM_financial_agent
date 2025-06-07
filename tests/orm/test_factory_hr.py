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

def test_hr_documents_and_relations(session, factory):
    """Menguji pembuatan dokumen-dokumen HR dan relasinya ke MasterEmployeeH."""
    employee = factory.master.create("MasterEmployeeH", EmployeeNo="EMP-HR-01")
    session.commit()
    
    # 1. Uji Change Shift
    change_shift_h = factory.hr.create("HrChangeShiftH", DocNo="CSH-REL-TEST")
    factory.hr.create("HrChangeShiftD", hrchangeshifth=change_shift_h, masteremployeeh=employee)
    session.commit()

    retrieved_cs = session.query(db_models.HrChangeShiftH).filter_by(DocNo="CSH-REL-TEST").one()
    assert len(retrieved_cs.details) == 1
    assert retrieved_cs.details[0].employee_ref.EmployeeNo == "EMP-HR-01"
    print(f"    -> Berhasil membuat Change Shift '{retrieved_cs.DocNo}' dan validasi relasi.")

    # 2. Uji Overtime
    overtime_h = factory.hr.create("HrOvertimeH", DocNo="OT-REL-TEST")
    factory.hr.create("HrOvertimeD", hrovertimeh=overtime_h, masteremployeeh=employee)
    session.commit()

    retrieved_ot = session.query(db_models.HrOvertimeH).filter_by(DocNo="OT-REL-TEST").one()
    assert len(retrieved_ot.details) == 1
    assert retrieved_ot.details[0].employee_ref.EmployeeNo == "EMP-HR-01"
    print(f"    -> Berhasil membuat Overtime '{retrieved_ot.DocNo}' dan validasi relasi.")

def run_all_hr_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk HR (dengan validasi relasi)...")
    
    tests_to_run = {
        "HR Document with Relations": test_hr_documents_and_relations,
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