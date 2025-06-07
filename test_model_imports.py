# test_model_imports.py
def test_imports():
    print("Mencoba mengimpor semua model dari backend.app.db_models...")
    try:
        from backend.app.db_models import (
            Base,
            MasterCountry, MasterCity, MasterUnit, MasterCurrency,
            MasterCustomerGroup, MasterPriceListType, MasterSalesArea1,
            MasterAccount, MasterTransactionType, MasterMaterialGroup1, MasterMaterialType,
            MasterEmployeeH, MasterSales, MasterLocation, MasterCustomer, MasterMaterial,
            ArRequestListH,
            GoodsIssueH,
            SalesOrderH,
            SalesOrderD,
            SalesInvoiceH,
            SalesInvoiceD,
            Arbook,
            CustomerPaymentH,
            CustomerPaymentD
        )
        print("Semua model berhasil diimpor.")
        
        # Anda bisa menambahkan print untuk beberapa model untuk memastikan kelasnya ada
        print(f"Contoh model: {MasterCustomer}")
        print(f"Contoh model: {SalesOrderH}")

    except ImportError as e:
        print(f"Gagal mengimpor model: {e}")
    except Exception as e:
        print(f"Error lain terjadi saat impor: {e}")

if __name__ == "__main__":
    test_imports()