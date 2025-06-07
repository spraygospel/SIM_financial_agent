# tests/orm/run_all_orm_tests.py
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from tests.orm.test_factory_master_data import run_all_master_data_tests
from tests.orm.test_factory_purchase import run_all_purchase_tests
from tests.orm.test_factory_inventory import run_all_inventory_tests
from tests.orm.test_factory_sales import run_all_sales_tests
from tests.orm.test_factory_finance import run_all_finance_tests # TAMBAHKAN INI
from tests.orm.test_factory_production import run_all_production_tests

def main():
    print("="*20 + " MEMULAI SEMUA TES ORM " + "="*20)
    
    master_data_ok = run_all_master_data_tests()
    purchase_ok = run_all_purchase_tests()
    inventory_ok = run_all_inventory_tests()
    sales_ok = run_all_sales_tests()
    finance_ok = run_all_finance_tests() # TAMBAHKAN INI
    production_ok = run_all_production_tests()
    
    print("\n" + "="*20 + " RINGKASAN HASIL TES " + "="*20)
    all_ok = master_data_ok and purchase_ok and inventory_ok and sales_ok and finance_ok and production_ok # TAMBAHKAN INI
    if all_ok:
        print("✅ SEMUA TES ORM BERHASIL.")
    else:
        print("❌ BEBERAPA TES ORM GAGAL.")
        if not master_data_ok: print("  - Tes Master Data Gagal")
        if not purchase_ok: print("  - Tes Purchase Gagal")
        if not inventory_ok: print("  - Tes Inventory Gagal")
        if not sales_ok: print("  - Tes Sales Gagal")
        if not finance_ok: print("  - Tes Finance Gagal") # TAMBAHKAN INI
        if not production_ok: print("  - Tes Production Gagal") 

if __name__ == "__main__":
    main()