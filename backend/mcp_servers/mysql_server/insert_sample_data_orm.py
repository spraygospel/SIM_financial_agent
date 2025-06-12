# scripts/insert_sample_data_orm.py

import sys
from pathlib import Path
from datetime import date, datetime # Tambahkan datetime

# --- Setup Path (Wajib ada di paling atas) ---
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# --- Impor yang Diperlukan ---
from main import get_db_session
from db_models.orm_k_o import Mastercustomer, Mastercountry, Mastercurrency, Mastercustomergroup, Masterpricelisttype
from db_models.orm_a_e import Arbook

def insert_data():
    """Menghapus data lama dan menyisipkan data sampel baru menggunakan ORM."""
    
    print("--- Memulai penyisipan data sampel via ORM ---")
    
    with get_db_session() as session:
        try:
            print("🔄 Menghapus data lama dari tabel 'arbook' dan 'mastercustomer'...")
            session.query(Arbook).delete(synchronize_session=False)
            session.query(Mastercustomer).delete(synchronize_session=False)
            print("✅ Data lama berhasil dihapus.")

            # --- Langkah Baru: Isi Tabel Master ---
            print("🔄 Mengisi tabel-tabel master...")
            session.merge(Mastercountry(Code="IDN", Name="Indonesia", CreatedBy="SCRIPT", CreatedDate=datetime.now(), ChangedBy="SCRIPT", ChangedDate=datetime.now()))
            session.merge(Mastercurrency(Code="IDR", Name="Indonesian Rupiah", CreatedBy="SCRIPT", CreatedDate=datetime.now(), ChangedBy="SCRIPT", ChangedDate=datetime.now()))
            session.merge(Mastercustomergroup(Code="G01", Name="General Customer", CreatedBy="SCRIPT", CreatedDate=datetime.now(), ChangedBy="SCRIPT", ChangedDate=datetime.now()))
            session.merge(Masterpricelisttype(Code="RTL", Name="Retail", CreatedBy="SCRIPT", CreatedDate=datetime.now(), ChangedBy="SCRIPT", ChangedDate=datetime.now()))
            print("✅ Data master siap.")

            # --- Data Sampel Baru ---
            print("🔄 Menyiapkan data sampel baru untuk customer dan arbook...")
            customer1 = Mastercustomer(
                Code="C-001-ORM", Name="PT Sukses via ORM", Address="Jl. SQLAlchemy No. 20", Address2="",
                City="Jakarta", Country="IDN", Phone="", Fax="", Email="", Contact="", Mobile="", WhatsAppSession="", WhatsAppNo="",
                TaxNumber="", CustomerGroup="G01", PriceListType="RTL", SalesArea1="SA1", SalesArea2="SA2", SalesArea3="SA3",
                TOP=30, Currency="IDR", Limit=100000000, TransactionType="TRN01", TransactionType2="TRN02",
                CutPPh=False, IsBlacklisted=False, IsDeleted=False, Latitude=0.0, Longitude=0.0, Information="Created via ORM script",
                CreatedBy="SCRIPT", CreatedDate=datetime.now(), ChangedBy="SCRIPT", ChangedDate=datetime.now(), Znowa=""
            )
            customer2 = Mastercustomer(
                Code="C-002-ORM", Name="CV Maju Koding", Address="Jl. Pydantic No. 1", Address2="",
                City="Surabaya", Country="IDN", Phone="", Fax="", Email="", Contact="", Mobile="", WhatsAppSession="", WhatsAppNo="",
                TaxNumber="", CustomerGroup="G01", PriceListType="RTL", SalesArea1="SA1", SalesArea2="SA2", SalesArea3="SA3",
                TOP=60, Currency="IDR", Limit=50000000, TransactionType="TRN01", TransactionType2="TRN02",
                CutPPh=False, IsBlacklisted=False, IsDeleted=False, Latitude=0.0, Longitude=0.0, Information="Created via ORM script",
                CreatedBy="SCRIPT", CreatedDate=datetime.now(), ChangedBy="SCRIPT", ChangedDate=datetime.now(), Znowa=""
            )
            arbook1 = Arbook(
                Periode=date(2024, 1, 1), CustomerCode="C-001-ORM", TransType="INVOICE", DocNo="INV/ORM/001",
                DocDate=date(2024, 5, 1), TOP=30, DueDate=date(2024, 6, 1), Currency="IDR", ExchangeRate=1,
                Information="Sample invoice 1", DC='D', DocValue=5000000, DocValueLocal=5000000,
                PaymentValue=2000000, PaymentValueLocal=2000000, ExchangeRateDiff=0
            )
            arbook2 = Arbook(
                Periode=date(2024, 1, 1), CustomerCode="C-002-ORM", TransType="INVOICE", DocNo="INV/ORM/002",
                DocDate=date(2024, 5, 10), TOP=30, DueDate=date(2024, 6, 10), Currency="IDR", ExchangeRate=1,
                Information="Sample invoice 2 (Lunas)", DC='D', DocValue=10000000, DocValueLocal=10000000,
                PaymentValue=10000000, PaymentValueLocal=10000000, ExchangeRateDiff=0
            )
            arbook3 = Arbook(
                Periode=date(2024, 1, 1), CustomerCode="C-001-ORM", TransType="INVOICE", DocNo="INV/ORM/003",
                DocDate=date(2024, 5, 15), TOP=30, DueDate=date(2024, 6, 15), Currency="IDR", ExchangeRate=1,
                Information="Sample invoice 3", DC='D', DocValue=7500000, DocValueLocal=7500000,
                PaymentValue=0, PaymentValueLocal=0, ExchangeRateDiff=0
            )
            print("🔄 Menambahkan data baru ke sesi...")
            session.add_all([customer1, customer2, arbook1, arbook2, arbook3])
            
            print("🔄 Melakukan commit transaksi ke database...")
            session.commit()
            print("✅ Data berhasil di-commit!")

        except Exception as e:
            print(f"🔥 GAGAL: Terjadi error saat transaksi. Melakukan rollback...")
            session.rollback()
            print(f"Error detail: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("🔄 Menutup sesi database...")
            session.close()

if __name__ == "__main__":
    insert_data()