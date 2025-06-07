# test_orm_definitions.py
import sys
import traceback



def run_test():
    print("-" * 50)
    print("MEMULAI TES DEFINISI MODEL ORM DAN IMPOR")
    print("-" * 50)

    required_models = [
        "Base",
        "MasterCountry", "MasterCity", "MasterUnit", "MasterCurrency",
        "MasterCustomerGroup", "MasterPriceListType", "MasterSalesArea1",
        "MasterAccount", "MasterTransactionType", "MasterMaterialGroup1", "MasterMaterialType",
        "MasterEmployeeH", "MasterSales", "MasterLocation", "MasterCustomer", "MasterMaterial",
        "ArRequestListH", "GoodsIssueH", "SalesOrderH", "SalesOrderD",
        "SalesInvoiceH", "SalesInvoiceD", "Arbook",
        "CustomerPaymentH", "CustomerPaymentD"
    ]

    print("\n[INFO] Mencoba mengimpor semua model yang diperlukan...")
    all_models_imported = True
    imported_objects = {}

    try:
        # Ini akan memicu pemuatan semua model karena __init__.py
        from backend.app.db_models import Base 
        imported_objects["Base"] = Base
        
        # Impor spesifik untuk verifikasi nama
        from backend.app.db_models.master_data_models import (
            MasterCountry, MasterCity, MasterUnit, MasterCurrency,
            MasterCustomerGroup, MasterPriceListType, MasterSalesArea1,
            MasterAccount, MasterTransactionType, MasterMaterialGroup1, MasterMaterialType,
            MasterEmployeeH, MasterSales, MasterLocation, MasterCustomer, MasterMaterial
        )
        imported_objects.update(locals()) # Menambahkan semua yang baru diimpor

        from backend.app.db_models.sales_models import (
            ArRequestListH, GoodsIssueH, SalesOrderH, SalesOrderD,
            SalesInvoiceH, SalesInvoiceD, Arbook,
            CustomerPaymentH, CustomerPaymentD
        )
        imported_objects.update(locals()) # Menambahkan semua yang baru diimpor
        
        print("[SUCCESS] Semua modul model dasar berhasil diimpor.")

    except ImportError as e:
        print(f"[ERROR] Gagal mengimpor modul model dasar: {e}")
        traceback.print_exc()
        all_models_imported = False
    except Exception as e:
        print(f"[ERROR] Error lain saat impor modul model dasar: {e}")
        traceback.print_exc()
        all_models_imported = False

    if not all_models_imported:
        print("\n[KESIMPULAN] Ada masalah saat impor modul model dasar. Tidak dapat melanjutkan.")
        return

    print("\n[INFO] Memverifikasi ketersediaan semua kelas model yang diharapkan...")
    all_classes_found = True
    for model_name in required_models:
        if model_name not in imported_objects:
            print(f"[ERROR] Kelas model '{model_name}' tidak ditemukan setelah impor.")
            all_classes_found = False
    
    if all_classes_found:
        print("[SUCCESS] Semua kelas model yang diharapkan berhasil ditemukan dan diimpor.")
    else:
        print("\n[KESIMPULAN] Tidak semua kelas model ditemukan. Periksa __init__.py dan file model terkait.")
        return

    print("\n[INFO] Mencoba menginisialisasi engine dan sesi SQLAlchemy...")
    engine = None
    SessionLocal = None
    try:
        from backend.app.db.session import engine as db_engine, SessionLocal as db_SessionLocal, get_db_session
        engine = db_engine
        SessionLocal = db_SessionLocal
        assert engine is not None, "Engine SQLAlchemy tidak boleh None."
        assert SessionLocal is not None, "SessionLocal tidak boleh None."
        if not hasattr(SessionLocal, "configure"): # Cek apakah dummy
             raise RuntimeError("SessionLocal adalah dummy, engine mungkin gagal dibuat.")
        print("[SUCCESS] Engine dan SessionLocal SQLAlchemy berhasil diimpor dan diinisialisasi.")
        
        print("\n[INFO] Menguji koneksi database dengan query ORM sederhana (MasterCountry)...")
        db_gen = get_db_session()
        db = next(db_gen)
        try:
            country_count = db.query(MasterCountry).count()
            print(f"[SUCCESS] Query ORM ke MasterCountry berhasil. Jumlah record: {country_count}")
            
            # Tes query yang melibatkan relasi yang baru diperbaiki
            print("\n[INFO] Menguji query ORM yang melibatkan relasi (MasterSales & SalesOrderH)...")
            # Ambil satu sales order dan coba akses sales person-nya
            first_so = db.query(SalesOrderH).first()
            if first_so:
                print(f"Sales Order pertama: {first_so.DocNo}")
                if first_so.sales_person_ref:
                    print(f"  Sales Person (dari SO): {first_so.sales_person_ref.Name}")
                else:
                    print(f"  Tidak ada sales person terkait untuk SO {first_so.DocNo}")
                
                # Ambil satu sales person dan coba akses sales order-nya
                first_sales_person = db.query(MasterSales).first()
                if first_sales_person:
                    print(f"Sales Person pertama: {first_sales_person.Name}")
                    # Coba akses relasi sales_orders_by_sales_code
                    related_sos_count = len(first_sales_person.sales_orders_by_sales_code)
                    print(f"  Jumlah Sales Orders terkait (via sales_orders_by_sales_code): {related_sos_count}")
                    if related_sos_count > 0:
                        print(f"    Contoh SO pertama: {first_sales_person.sales_orders_by_sales_code[0].DocNo}")

                else:
                    print("Tidak ada data MasterSales.")

            else:
                print("Tidak ada data SalesOrderH.")

            print("[SUCCESS] Tes query relasi ORM selesai (tidak ada error berarti konfigurasi relasi kemungkinan besar benar).")

        except Exception as e:
            print(f"[ERROR] Gagal melakukan query ORM atau mengakses relasi: {e}")
            traceback.print_exc()
        finally:
            try:
                next(db_gen) # close session
            except StopIteration:
                pass


    except ImportError as e:
        print(f"[ERROR] Gagal mengimpor engine/SessionLocal: {e}")
        traceback.print_exc()
    except RuntimeError as e:
        print(f"[ERROR] RuntimeError saat inisialisasi sesi: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"[ERROR] Error lain saat inisialisasi engine/sesi: {e}")
        traceback.print_exc()

    print("-" * 50)
    print("TES DEFINISI MODEL ORM DAN IMPOR SELESAI")
    print("-" * 50)

if __name__ == "__main__":
    run_test()