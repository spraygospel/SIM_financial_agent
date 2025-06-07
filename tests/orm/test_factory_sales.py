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

def test_sales_order_flow_and_relations(session, factory):
    """Menguji alur Sales Order -> Goods Issue -> Sales Invoice -> AR Book dan relasinya."""
    # 1. Buat data master spesifik
    customer = factory.master.create("MasterCustomer", Code="CUST-FLOW")
    material = factory.master.create("MasterMaterial", Code="MAT-FLOW")
    session.commit()

    # 2. Buat Sales Order
    so_header = factory.sales.create("SalesOrderH", mastercustomer=customer, DocNo="SO-FLOW-TEST")
    factory.sales.create("SalesOrderD", salesorderh=so_header, mastermaterial=material, Number=1)
    session.commit()
    print(f"    -> Berhasil membuat Sales Order: {so_header.DocNo}")

    # 3. Buat Goods Issue
    gi_header = factory.sales.create("GoodsIssueH", salesorderh=so_header, DocNo="GI-FLOW-TEST")
    session.commit()
    print(f"    -> Berhasil membuat Goods Issue: {gi_header.DocNo}")

    # 4. Buat Sales Invoice
    si_header = factory.sales.create("SalesInvoiceH", salesorderh=so_header, goodsissueh=gi_header, DocNo="SI-FLOW-TEST")
    session.commit()
    print(f"    -> Berhasil membuat Sales Invoice: {si_header.DocNo}")

    # 5. Buat AR Book
    ar_entry = factory.sales.create("Arbook", salesinvoiceh=si_header)
    session.commit()
    print(f"    -> Berhasil membuat AR Book untuk Invoice: {ar_entry.DocNo}")

    # 6. Validasi relasi
    retrieved_si = session.query(db_models.SalesInvoiceH).filter_by(DocNo="SI-FLOW-TEST").one()
    assert retrieved_si.sales_order.DocNo == "SO-FLOW-TEST"
    assert retrieved_si.goods_issue.DocNo == "GI-FLOW-TEST"
    assert retrieved_si.ar_books[0].DocNo == "SI-FLOW-TEST"
    print(f"    -> Berhasil memvalidasi relasi alur penjualan lengkap.")


def run_all_sales_tests():
    TEST_DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    engine = create_engine(TEST_DATABASE_URL)
    
    print("-" * 50)
    print("Memulai tes untuk Sales (dengan validasi relasi)...")
    
    tests_to_run = {
        "Full Sales Flow with Relations": test_sales_order_flow_and_relations,
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