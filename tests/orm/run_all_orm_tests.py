# tests/orm/run_all_orm_tests.py
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.app.db_models import ALL_DEFINED_MODELS
from sqlalchemy import create_engine
from backend.app.core.config import settings
from backend.factories.base import test_session_scope, MainTestDataFactory

from tests.orm.test_factory_master_data import run_all_master_data_tests
from tests.orm.test_factory_purchase import run_all_purchase_tests
from tests.orm.test_factory_inventory import run_all_inventory_tests
from tests.orm.test_factory_sales import run_all_sales_tests
from tests.orm.test_factory_production import run_all_production_tests
from tests.orm.test_factory_hr import run_all_hr_tests
from tests.orm.test_factory_finance import run_all_finance_tests

def main(show_untested=False):
    print("="*20 + " MEMULAI SEMUA TES ORM " + "="*20)

    # 1. Jalankan semua grup tes
    test_groups = [
        ("Master Data", run_all_master_data_tests),
        ("Purchase", run_all_purchase_tests),
        ("Inventory", run_all_inventory_tests),
        ("Sales", run_all_sales_tests),
        ("Production", run_all_production_tests),
        ("Finance", run_all_finance_tests),
        ("HR", run_all_hr_tests),
    ]

    all_ok = all(run_func() for _, run_func in test_groups)

    # 2. Setelah semua tes selesai, buat satu factory HANYA untuk melacak model
    print("\n" + "="*20 + " MENGHITUNG CAKUPAN TES " + "="*20)
    successfully_tested_models = set()
    try:
        TEST_DATABASE_URL = (
            f"mysql+mysqlconnector://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}"
            f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
        )
        engine = create_engine(TEST_DATABASE_URL)
        with test_session_scope(engine) as (session, factory):
            for group_name, run_func in test_groups:
                # Kita tidak menjalankan tes lagi, hanya memanggil builder yang ada di factory
                # Ini akan mengisi `successfully_built_models`
                if group_name == "Master Data": factory.master._register_builders()
                if group_name == "Purchase": factory.purchase._register_builders()
                if group_name == "Inventory": factory.inventory._register_builders()
                if group_name == "Sales": factory.sales._register_builders()
                if group_name == "Production": factory.production._register_builders()
                if group_name == "Finance": factory.finance._register_builders()
                if group_name == "HR": factory.hr._register_builders()
            
            # Ambil semua model yang builder-nya sudah terdaftar
            successfully_tested_models = {
                factory.get_model_class(model_name).__tablename__ 
                for model_name in factory._builders.keys()
            }
    except Exception as e:
        print(f"Gagal menghitung cakupan tes: {e}")


    print("\n" + "="*20 + " RINGKASAN HASIL TES " + "="*20)
    
    total_defined = len(ALL_DEFINED_MODELS)
    total_tested_via_builder = len(successfully_tested_models)
    print(f"📊 Progres ORM: {total_tested_via_builder} dari {total_defined} model memiliki builder yang terdaftar.")

    if all_ok:
        print("✅ SEMUA TES ORM YANG DIJALANKAN BERHASIL.")
    else:
        print("❌ BEBERAPA TES ORM GAGAL.")
    
    if show_untested:
        print("\n" + "="*20 + " LAPORAN MODEL YANG BELUM MEMILIKI BUILDER " + "="*20)
        untested_models = sorted([
            name for name in ALL_DEFINED_MODELS.keys() if name not in successfully_tested_models
        ])
        if not untested_models:
            print("✨ Semua model yang terdefinisi telah memiliki builder! ✨")
        else:
            print(f"Ditemukan {len(untested_models)} model yang belum memiliki builder:")
            for model_name in untested_models:
                print(f"  - {model_name}")

if __name__ == "__main__":
    show_untested_list = True 
    main(show_untested=show_untested_list)