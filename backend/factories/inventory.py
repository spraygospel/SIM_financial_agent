# backend/factories/inventory.py
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal
import random

class InventoryFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("Stock", self._build_stock)
        self.main_factory.register_builder("StockBalance", self._build_stock_balance)
        self.main_factory.register_builder("GoodsIssueD", self._build_goods_issue_d)
        self.main_factory.register_builder("GoodsReceiptD", self._build_goods_receipt_d)
        self.main_factory.register_builder("AdjustInH", self._build_adjust_in_h)
        self.main_factory.register_builder("AdjustInD", self._build_adjust_in_d)
        self.main_factory.register_builder("AdjustOutH", self._build_adjust_out_h)
        self.main_factory.register_builder("AdjustOutD", self._build_adjust_out_d)

        self.main_factory.register_builder("Batch", self._build_batch)
        self.main_factory.register_builder("DeliveryReturnH", self._build_delivery_return_h)
        self.main_factory.register_builder("DeliveryReturnD", self._build_delivery_return_d)
        
    def _build_stock(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        location = params.get('masterlocation') or self.main_factory.create('MasterLocation')

        return db_models.Stock(
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            MaterialCode=material.Code,
            DocNo=params.get('DocNo', self.main_factory.get_unique_value('DOC', 15)),
            DocDate=params.get('DocDate', now.date()),
            Location=location.Code,
            Zone=params.get('Zone', ''),
            Bin=params.get('Bin', ''),
            Number=params.get('Number', 0),
            Qty=params.get('Qty', Decimal(random.randint(10, 100))),
            Price=params.get('Price', Decimal(random.randint(1000, 5000)))
        )

    def _build_stock_balance(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        location = params.get('masterlocation') or self.main_factory.create('MasterLocation')
        self.main_factory.register_builder("DeliveryReturnH", self._build_delivery_return_h)
        self.main_factory.register_builder("DeliveryReturnD", self._build_delivery_return_d)

        return db_models.StockBalance(
            Periode=params.get('Periode', now.date().replace(day=1)),
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            MaterialCode=material.Code,
            Location=location.Code,
            Zone=params.get('Zone', ''),
            Bin=params.get('Bin', ''),
            Price=params.get('Price', Decimal('0.0')),
            QtyStart=params.get('QtyStart', Decimal('0.0')),
            QtyIn=params.get('QtyIn', Decimal('0.0')),
            QtyOut=params.get('QtyOut', Decimal('0.0')),
            QtyEnd=params.get('QtyEnd', Decimal('0.0')),
            QtyBook=params.get('QtyBook', Decimal('0.0'))
        )
        
    def _build_goods_issue_d(self, params):
        # Catatan: Kita butuh builder untuk GoodsIssueH terlebih dahulu
        header = params.get('goodsissueh') or self.main_factory.create('GoodsIssueH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit')

        return db_models.GoodsIssueD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code,
            Info=params.get('Info', ''),
            Qty=params.get('Qty', Decimal('1.0')),
            BaseQty=params.get('BaseQty', Decimal('1.0')),
            QtyReturn=params.get('QtyReturn', Decimal('0.0')),
            QtyNetto=params.get('QtyNetto', Decimal('1.0'))
        )

    def _build_goods_receipt_d(self, params):
        # Catatan: Kita butuh builder untuk GoodsReceiptH terlebih dahulu
        header = params.get('goodsreceipth') or self.main_factory.create('GoodsReceiptH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit')

        return db_models.GoodsReceiptD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code,
            Info=params.get('Info', ''),
            BatchNo=params.get('BatchNo', ''),
            BatchInfo=params.get('BatchInfo', ''),
            Qty=params.get('Qty', Decimal('1.0'))
        )
    def _build_adjust_in_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        location = params.get('masterlocation') or self.main_factory.create('MasterLocation')
        trans_type = params.get('mastertransactiontype') or self.main_factory.create('MasterTransactionType')

        return db_models.AdjustInH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("AIH", 15)),
            Series='AIG', TransactionType=trans_type.Type, DocDate=now.date(),
            Location=location.Code, AODocNo='', IsOutsource=False, Information='Test Adj In',
            Status='OPEN', TotalPrice=0, TotalAssumedPrice=0, IsApproved=True, ApprovedBy='test',
            PrintCounter=0, CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_adjust_in_d(self, params):
        header = params.get('adjustinh') or self.main_factory.create('AdjustInH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        # PERBAIKAN: Buat/dapatkan unit secara eksplisit, jangan andalkan relasi
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit', Code=material.SmallestUnit)

        return db_models.AdjustInD(
            DocNo=header.DocNo,
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Zone=params.get('Zone', ''),
            Bin=params.get('Bin', ''),
            BatchNo='', BatchInfo='', Unit=unit.Code, Qty=Decimal('1.0'), Price=0, AssumedPrice=0
        )

    def _build_adjust_out_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        location = params.get('masterlocation') or self.main_factory.create('MasterLocation')
        trans_type = params.get('mastertransactiontype') or self.main_factory.create('MasterTransactionType')

        return db_models.AdjustOutH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("AOH", 15)),
            Series='AOG', TransactionType=trans_type.Type, DocDate=now.date(),
            Location=location.Code, Information='Test Adj Out', Status='OPEN',
            TotalCost=0, IsApproved=True, ApprovedBy='test', PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_adjust_out_d(self, params):
        header = params.get('adjustouth') or self.main_factory.create('AdjustOutH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        # PERBAIKAN: Buat/dapatkan unit secara eksplisit, jangan andalkan relasi
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit', Code=material.SmallestUnit)

        return db_models.AdjustOutD(
            DocNo=header.DocNo,
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Zone=params.get('Zone', ''),
            Bin=params.get('Bin', ''),
            Unit=unit.Code, Qty=Decimal('1.0'), BaseQty=Decimal('1.0'), Cost=0
        )
    def _build_batch(self, params):
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')

        return db_models.Batch(
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            MaterialCode=material.Code,
            BatchNo=params.get('BatchNo', self.main_factory.get_unique_value('B', 20)),
            BatchInfo=params.get('BatchInfo', 'Info Batch Default'),
            ExpiryDate=params.get('ExpiryDate', None)
        )
    def _build_delivery_return_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        gi_header = params.get('goodsissueh') or self.main_factory.create('GoodsIssueH')
        customer = gi_header.sales_order.customer # Ambil customer dari SO di dalam GI

        return db_models.DeliveryReturnH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("DR", 15)),
            Series='DR', DocDate=now.date(), GIDocNo=gi_header.DocNo,
            CustomerCode=customer.Code,
            Location=gi_header.Location, Zone='', Information='Test Delivery Return',
            Status='OPEN', PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_delivery_return_d(self, params):
        header = params.get('deliveryreturnh') or self.main_factory.create('DeliveryReturnH')
        # Buat dummy material karena tidak ada hubungan langsung
        material = self.main_factory.create('MasterMaterial')
        unit = material.smallest_unit_ref

        return db_models.DeliveryReturnD(
            DocNo=header.DocNo, Number=1, MaterialCode=material.Code, Info='',
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code, QtyReturn=1
        )
    