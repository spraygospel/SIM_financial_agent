# tests/orm/test_factory_sales.py
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

def test_create_so_header(session, factory):
    """Menguji pembuatan SalesOrderH dengan dependensi otomatis."""
    so_header = factory.sales.create("SalesOrderH")
    session.flush()
    
    assert so_header is not None
    assert so_header.customer is not None
    assert so_header.sales_person_ref is not None
    print(f"    -> Berhasil membuat SO Header '{so_header.DocNo}' untuk Customer '{so_header.customer.Name}'")

def test_create_so_with_details(session, factory):
    """Menguji pembuatan SO lengkap dengan detail."""
    so_header = factory.sales.create("SalesOrderH")
    
    factory.sales.create("SalesOrderD", salesorderh=so_header, Number=1)
    factory.sales.create("SalesOrderD", salesorderh=so_header, Number=2)
    
    session.flush()

    assert len(so_header.details) == 2
    print(f"    -> Berhasil membuat SO '{so_header.DocNo}' dengan {len(so_header.details)} baris detail.")
def test_create_arbook_from_invoice(session, factory):
    """Menguji pembuatan Arbook yang bergantung pada SalesInvoiceH."""
    # PERBAIKAN: Buat semua dependensi SalesInvoiceH terlebih dahulu
    so = factory.sales.create("SalesOrderH")
    gi = factory.sales.create("GoodsIssueH", salesorderh=so)
    session.flush() # Pastikan SO dan GI tersimpan dan relasi terbentuk

    # Sekarang buat SalesInvoiceH dengan dependensi yang sudah ada
    invoice_header = factory.sales.create("SalesInvoiceH", salesorderh=so, goodsissueh=gi)
    session.flush() # Pastikan invoice tersimpan

    assert invoice_header is not None
    assert invoice_header.customer is not None, "Relasi 'customer' di SalesInvoiceH seharusnya tidak None"
    
    # Sekarang buat Arbook dengan invoice yang sudah valid
    arbook_entry = factory.sales.create("Arbook", salesinvoiceh=invoice_header)
    session.flush()

    assert arbook_entry is not None
    assert arbook_entry.CustomerCode == invoice_header.CustomerCode
    print(f"    -> Berhasil membuat Arbook untuk Invoice '{arbook_entry.DocNo}'")

def test_create_sales_return_with_details(session, factory):
    """Menguji pembuatan SalesReturnH dengan detailnya."""
    return_header = factory.sales.create("SalesReturnH")
    session.flush()

    factory.sales.create("SalesReturnD", salesreturnh=return_header, Number=1)
    factory.sales.create("SalesReturnD", salesreturnh=return_header, Number=2)
    session.flush()

    assert len(return_header.details) == 2
    print(f"    -> Berhasil membuat Sales Return '{return_header.DocNo}' dengan {len(return_header.details)} baris detail.")

def run_all_sales_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Sales...")
    
    tests_to_run = {
        "SO Header Creation": test_create_so_header,
        "SO with Details Creation": test_create_so_with_details,
        "AR Book Creation": test_create_arbook_from_invoice,
        "Sales Return Creation": test_create_sales_return_with_details,
    }
    
    results = {}
    for name, func in tests_to_run.items():
        results[name] = _run_test(engine, func, name)
    
    if all(results.values()):
        print("\n[HASIL SALES] ✅ Semua tes berhasil.")
        return True
    else:
        print("\n[HASIL SALES] ❌ Gagal.")
        for name, status in results.items():
            if not status:
                print(f"  - Tes Gagal: {name}")
        return False