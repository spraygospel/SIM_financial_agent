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

def test_create_journal_with_details(session, factory):
    """Menguji pembuatan GeneralJournalH dengan dua baris detail yang seimbang."""
    journal_header = factory.finance.create("GeneralJournalH")

    # Buat dua akun untuk jurnal debit dan kredit
    debit_account = factory.master.create("MasterAccount", Name="Kas")
    credit_account = factory.master.create("MasterAccount", Name="Pendapatan")
    session.flush()

    # Buat baris detail Debit
    factory.finance.create(
        "GeneralJournalD",
        generaljournalh=journal_header,
        masteraccount=debit_account,
        Number=1,
        Debet=Decimal("50000"),
        Credit=Decimal("0")
    )

    # Buat baris detail Kredit
    factory.finance.create(
        "GeneralJournalD",
        generaljournalh=journal_header,
        masteraccount=credit_account,
        Number=2,
        Debet=Decimal("0"),
        Credit=Decimal("50000")
    )

    session.flush()

    assert len(journal_header.details) == 2
    
    total_debet = sum(d.Debet for d in journal_header.details)
    total_credit = sum(d.Credit for d in journal_header.details)
    
    assert total_debet == total_credit
    print(f"    -> Berhasil membuat Jurnal '{journal_header.DocNo}' dengan 2 baris detail seimbang.")

def test_create_ap_book(session, factory):
    """Menguji pembuatan Apbook."""
    ap_book_entry = factory.finance.create("Apbook")
    session.flush()
    assert ap_book_entry is not None
    assert ap_book_entry.supplier is not None
    print(f"    -> Berhasil membuat Apbook untuk DocNo '{ap_book_entry.DocNo}'")

def test_create_customer_balance(session, factory):
    """Menguji pembuatan CustomerBalance."""
    customer_balance_entry = factory.finance.create("CustomerBalance")
    session.flush()
    assert customer_balance_entry is not None
    assert customer_balance_entry.customer is not None
    print(f"    -> Berhasil membuat CustomerBalance untuk Customer '{customer_balance_entry.CustomerCode}'")

def test_create_supplier_balance(session, factory):
    """Menguji pembuatan SupplierBalance."""
    supplier_balance_entry = factory.finance.create("SupplierBalance")
    session.flush()
    assert supplier_balance_entry is not None
    assert supplier_balance_entry.supplier is not None
    print(f"    -> Berhasil membuat SupplierBalance untuk Supplier '{supplier_balance_entry.SupplierCode}'")

def run_all_finance_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Finance...")
    
    tests_to_run = {
        "Balanced Journal Creation": test_create_journal_with_details,
        "AP Book Creation": test_create_ap_book,
        "Customer Balance Creation": test_create_customer_balance,
        "Supplier Balance Creation": test_create_supplier_balance,
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