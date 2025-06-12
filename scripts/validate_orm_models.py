# File: scripts/validate_orm_models.py (v1.2 - Final)

import os
import sys
from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Setup Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ------------------

try:
    from backend.app.core.config import settings
    from backend.mcp_servers.mysql_server.db_models import (
        Base, Arbook, Mastercustomer, Mastercountry, Mastercurrency, 
        Mastercustomergroup, Masterpricelisttype, Customerpaymentd
    )
    print("Successfully imported settings and ORM models.")
except ImportError as e:
    print(f"Error during import: {e}")
    print("Please ensure the project structure is correct and all __init__.py files are present.")
    sys.exit(1)

def validate_crud_and_relations():
    """
    Fungsi utama untuk menjalankan validasi CRUD pada model ORM.
    """
    print(f"Connecting to TEST database: {settings.TEST_DATABASE_URL}")
    
    try:
        engine = create_engine(settings.TEST_DATABASE_URL, echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        print("Database connection successful.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return

    master_data_to_create = []
    
    try:
        print("Creating all tables based on ORM models (if they don't exist)...")
        Base.metadata.create_all(bind=engine)
        print("Tables created.")

        print("\n--- Preparing Master Data ---")

        # Data master yang dibutuhkan
        country_id = 'ID'
        currency_idr = 'IDR'
        cust_group_rtl = 'RTL'
        price_list_rp = 'RP'

        # Cek dan siapkan data master jika belum ada
        if not db.get(Mastercountry, country_id):
            master_data_to_create.append(Mastercountry(Code=country_id, Name='Indonesia', CreatedBy='VALIDATOR', CreatedDate=datetime.now(), ChangedBy='VALIDATOR', ChangedDate=datetime.now()))
            print(f"  - Queued Mastercountry '{country_id}'")

        if not db.get(Mastercurrency, currency_idr):
            master_data_to_create.append(Mastercurrency(Code=currency_idr, Name='Indonesian Rupiah', CreatedBy='VALIDATOR', CreatedDate=datetime.now(), ChangedBy='VALIDATOR', ChangedDate=datetime.now()))
            print(f"  - Queued Mastercurrency '{currency_idr}'")

        if not db.get(Mastercustomergroup, cust_group_rtl):
            master_data_to_create.append(Mastercustomergroup(Code=cust_group_rtl, Name='Retail Customers', CreatedBy='VALIDATOR', CreatedDate=datetime.now(), ChangedBy='VALIDATOR', ChangedDate=datetime.now()))
            print(f"  - Queued Mastercustomergroup '{cust_group_rtl}'")

        if not db.get(Masterpricelisttype, price_list_rp):
            master_data_to_create.append(Masterpricelisttype(Code=price_list_rp, Name='Rupiah Price List', CreatedBy='VALIDATOR', CreatedDate=datetime.now(), ChangedBy='VALIDATOR', ChangedDate=datetime.now()))
            print(f"  - Queued Masterpricelisttype '{price_list_rp}'")

        if master_data_to_create:
            db.add_all(master_data_to_create)
            db.commit()
            print("  - Committed all master data.")

        print("\n--- Testing CREATE ---")
        
        new_customer = Mastercustomer(
            Code='TESTCUST01', Name='PT Uji Coba ORM', Address='Jl. Validasi No. 123',
            City='Jakarta', Country=country_id, PriceListType=price_list_rp,
            CustomerGroup=cust_group_rtl, Currency=currency_idr,
            Address2='', Phone='12345', Fax='', Email='test@orm.com', Contact='Tester',
            Mobile='08123', WhatsAppSession='', WhatsAppNo='', TaxNumber='12345',
            SalesArea1='JKT', SalesArea2='JKT', SalesArea3='JKT', TOP=30, Limit=10000000,
            TransactionType='TUNAI', TransactionType2='TUNAI', CutPPh=False,
            IsBlacklisted=False, IsDeleted=False, Latitude=0, Longitude=0,
            Information='Created by validation script', CreatedBy='VALIDATOR',
            CreatedDate=datetime.now(), ChangedBy='VALIDATOR', ChangedDate=datetime.now()
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        print(f"  - Created Mastercustomer: {new_customer.Name} (Code: {new_customer.Code})")

        new_arbook = Arbook(
            Periode=date.today(), CustomerCode=new_customer.Code, TransType='Piutang Usaha',
            DocNo='INV/TEST/001', DocDate=date.today(), TOP=30, DueDate=date(2025, 1, 1),
            Currency=currency_idr, ExchangeRate=1, Information='Test AR Book Entry', DC='D',
            DocValue=1500000, DocValueLocal=1500000, PaymentValue=0,
            PaymentValueLocal=0, ExchangeRateDiff=0
        )
        db.add(new_arbook)
        db.commit()
        db.refresh(new_arbook)
        print(f"  - Created Arbook: {new_arbook.DocNo} for Customer {new_arbook.CustomerCode}")

        print("\n--- Testing READ ---")
        retrieved_customer = db.query(Mastercustomer).filter(Mastercustomer.Code == 'TESTCUST01').first()
        if retrieved_customer and retrieved_customer.Name == 'PT Uji Coba ORM':
            print(f"  - SUCCESS: Retrieved customer '{retrieved_customer.Name}' correctly.")
        else:
            print(f"  - FAILURE: Could not retrieve customer correctly. Found: {retrieved_customer}")

        retrieved_arbook = db.query(Arbook).filter(Arbook.DocNo == 'INV/TEST/001').first()
        if retrieved_arbook and retrieved_arbook.DocValue == 1500000:
            print(f"  - SUCCESS: Retrieved arbook '{retrieved_arbook.DocNo}' correctly.")
        else:
            print(f"  - FAILURE: Could not retrieve arbook correctly. Found: {retrieved_arbook}")

        print("\n--- Testing UPDATE ---")
        if retrieved_arbook:
            retrieved_arbook.PaymentValue = 500000
            retrieved_arbook.PaymentValueLocal = 500000
            db.commit()
            db.refresh(retrieved_arbook)
            
            updated_arbook = db.query(Arbook).filter(Arbook.DocNo == 'INV/TEST/001').first()
            if updated_arbook.PaymentValue == 500000:
                print(f"  - SUCCESS: Arbook payment was updated to {updated_arbook.PaymentValue}.")
            else:
                print(f"  - FAILURE: Arbook payment update failed.")
        else:
            print("  - SKIPPED: Cannot test update because arbook was not retrieved.")

        print("\n--- Testing DELETE ---")
        if retrieved_arbook:
            db.delete(retrieved_arbook)
            print(f"  - Deleting Arbook: {retrieved_arbook.DocNo}")
        
        if retrieved_customer:
            db.delete(retrieved_customer)
            print(f"  - Deleting Mastercustomer: {retrieved_customer.Code}")

        db.commit()

        # --- REVISI MENGGUNAKAN db.get() UNTUK MODERNISASI ---
        master_data_to_delete = [
            db.get(Mastercountry, country_id),
            db.get(Mastercurrency, currency_idr),
            db.get(Mastercustomergroup, cust_group_rtl),
            db.get(Masterpricelisttype, price_list_rp)
        ]
        for item in master_data_to_delete:
            if item:
                db.delete(item)
        db.commit()
        print("  - Deleting master data created for the test.")

        deleted_customer = db.query(Mastercustomer).filter(Mastercustomer.Code == 'TESTCUST01').first()
        deleted_arbook = db.query(Arbook).filter(Arbook.DocNo == 'INV/TEST/001').first()

        if not deleted_customer and not deleted_arbook:
            print("  - SUCCESS: Test data cleaned up successfully.")
        else:
            print("  - FAILURE: Cleanup failed. Some test data might remain in the database.")

    except Exception as e:
        print(f"\nAn error occurred during validation: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        print("\nDatabase session closed.")
        print("ORM Validation Script Finished.")


if __name__ == "__main__":
    validate_crud_and_relations()