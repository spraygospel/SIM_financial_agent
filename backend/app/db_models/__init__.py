# backend/app/db_models/__init__.py
import logging
from sqlalchemy.orm import configure_mappers

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Impor Base terlebih dahulu
from .base import Base

# 2. Impor semua kelas model dari semua modul.
#    Gunakan 'import *' untuk kemudahan, karena __all__ di setiap modul akan mengontrol apa yang diimpor.
#    Atau impor secara eksplisit jika Anda lebih suka.
from .master_data_models import *
from .sales_models import *
from .inventory_models import *
from .purchase_models import *
from .finance_models import *
from .production_models import *
from .hr_models import *
# Tambahkan impor untuk modul model lain di sini saat dibuat

# 3. Panggil configure_mappers() untuk menyelesaikan semua relasi
try:
    logger.info("Memulai konfigurasi SQLAlchemy mappers...")
    configure_mappers()
    logger.info("Semua SQLAlchemy mappers berhasil dikonfigurasi.")
except Exception as e:
    logger.error(f"Error saat konfigurasi mapper: {e}", exc_info=True)
    raise

# 4. Definisikan __all__ untuk mengekspor semua model agar mudah diimpor dari luar
__all__ = [
    'Base',
    # Master Data Models
    'MasterCountry', 'MasterCity', 'MasterUnit', 'MasterCurrency',
    'MasterCustomerGroup', 'MasterPriceListType', 'MasterSalesArea1',
    'MasterAccount', 'MasterTransactionType', 'MasterMaterialGroup1', 'MasterMaterialType',
    'MasterEmployeeH', 'MasterSales', 'MasterLocation', 'MasterCustomer', 'MasterMaterial',
    'MasterAccountGroup', 'MasterDepartment', 'MasterCustomerPartner',
    'MasterMaterialGroup2', 'MasterMaterialGroup3', 'MasterSalesArea2', 'MasterSalesArea3',
    'MasterSupplier', 'MasterUnitConversion', 'MasterBank', 'MasterCollector', 'MasterProvince',

    # Sales Models
    'ArRequestListH', 'CustomerPaymentD', 'CustomerPaymentH', 'Arbook',
    'GoodsIssueH', 'SalesInvoiceD', 'SalesInvoiceH', 'SalesOrderD', 'SalesOrderH',
    'SalesReturnH', 'SalesReturnD', 'SalesInvoiceDP', 'SalesInvoiceGI',
    'SalesOrderRD', 'SalesOrderRS', 'SalesOrderSch',

    # Inventory Models
    'Stock', 'StockBalance', 'GoodsIssueD', 'GoodsReceiptD', 'AdjustInH', 'AdjustInD',
    'AdjustOutH', 'AdjustOutD', 'Batch', 'DeliveryReturnH', 'DeliveryReturnD',
    
    # Purchase Models
    'GoodsReceiptH', 'PurchaseOrderH', 'PurchaseOrderD', 'PurchaseReturnH', 'PurchaseReturnD',
    'PurchaseCostH', 'PurchaseCostD', 'PurchaseInvoiceC', 'PurchaseInvoiceDP', 'PurchaseInvoiceGR',
    
    # Finance Models
    'GeneralJournalH', 'GeneralJournalD', 'Apbook', 'CustomerBalance', 
    'SupplierBalance', 'CustomerDPBalance', 'SupplierDPBalance',

    # Production Models
    'JobOrder', 'MaterialUsageH', 'MaterialUsageD', 'JobResultH', 'JobResultD',

    # HR Models
    'HrChangeShiftH', 'HrChangeShiftD', 'HrOvertimeH', 'HrOvertimeD',
]

ALL_DEFINED_MODELS = {
    mapper.local_table.name: mapper.class_ for mapper in Base.registry.mappers
}