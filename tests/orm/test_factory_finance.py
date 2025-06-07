# tests/orm/test_factory_finance.py
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

def test_journal_creation_and_relations(session, factory):
    """Menguji pembuatan GeneralJournal dan relasi ke MasterAccount."""
    journal_h = factory.finance.create("GeneralJournalH", DocNo="GJ-REL-TEST")
    acc_debit = factory.master.create("MasterAccount", AccountNo="ACC-D")
    acc_credit = factory.master.create("MasterAccount", AccountNo="ACC-C")

    factory.finance.create("GeneralJournalD", generaljournalh=journal_h, masteraccount=acc_debit, Number=1, Debet=100)
    factory.finance.create("GeneralJournalD", generaljournalh=journal_h, masteraccount=acc_credit, Number=2, Credit=100, Debet=0)
    session.commit()

    retrieved_journal = session.query(db_models.GeneralJournalH).filter_by(DocNo="GJ-REL-TEST").one()
    assert len(retrieved_journal.details) == 2
    assert retrieved_journal.details[0].account_ref.AccountNo == "ACC-D"
    assert retrieved_journal.details[1].account_ref.AccountNo == "ACC-C"
    print(f"    -> Berhasil membuat Jurnal '{retrieved_journal.DocNo}' dan validasi relasi detail.")

def test_ap_book_and_relations(session, factory):
    """Menguji pembuatan Apbook dan relasinya."""
    supplier = factory.master.create("MasterSupplier", Code="SUP-APB-01")
    ap_entry = factory.finance.create("Apbook", mastersupplier=supplier, DocNo="AP-REL-TEST")
    session.commit()
    
    retrieved_ap = session.query(db_models.Apbook).filter_by(DocNo="AP-REL-TEST").one()
    assert retrieved_ap.supplier is not None
    assert retrieved_ap.supplier.Code == "SUP-APB-01"
    print(f"    -> Berhasil membuat Apbook untuk Supplier '{retrieved_ap.SupplierCode}' dan validasi relasi.")

def test_customer_balance_and_relations(session, factory):
    """Menguji pembuatan CustomerBalance dan relasinya."""
    customer = factory.master.create("MasterCustomer", Code="CUST-BAL01") # PERBAIKAN DI SINI
    balance_entry = factory.finance.create("CustomerBalance", mastercustomer=customer)
    session.commit()

    retrieved_balance = session.query(db_models.CustomerBalance).filter_by(CustomerCode="CUST-BAL01").one() # PERBAIKAN DI SINI
    assert retrieved_balance.customer is not None
    assert retrieved_balance.customer.Name == customer.Name
    print(f"    -> Berhasil membuat CustomerBalance untuk Customer '{retrieved_balance.CustomerCode}' dan validasi relasi.")
    
def run_all_finance_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Finance (dengan validasi relasi)...")
    
    tests_to_run = {
        "Journal Creation with Relations": test_journal_creation_and_relations,
        "AP Book Creation with Relations": test_ap_book_and_relations,
        "Customer Balance with Relations": test_customer_balance_and_relations,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL FINANCE] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL FINANCE] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False