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