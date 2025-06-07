# backend/factories/purchase.py
import random
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal

class PurchaseFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("PurchaseOrderH", self._build_purchase_order_h)
        self.main_factory.register_builder("PurchaseOrderD", self._build_purchase_order_d)

    def _build_purchase_order_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        
        return db_models.PurchaseOrderH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("PO", 15)),
            SupplierCode=supplier.Code,
            Currency=supplier.Currency,
            Series='PO', TransactionType='', DocDate=now.date(), DeliveryDate=now.date() + datetime.timedelta(days=7),
            TOP=30, DiscPercent=Decimal('0.0'), TaxStatus='Include', TaxPercent=Decimal('11.0'),
            ExchangeRate=Decimal('1.0'), JODocNo='', Trip='', SIDocNo='', TotalGross=Decimal('0.0'),
            TotalDisc=Decimal('0.0'), TaxValue=Decimal('0.0'), TotalNetto=Decimal('0.0'), CutPPh=False,
            PPhPercent=Decimal('0.0'), PPhValue=Decimal('0.0'), SendTo='', Information='', Status='OPEN',
            IsApproved=False, PrintCounter=0, IsSalesReturn=False,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_purchase_order_d(self, params):
        header = params.get('purchaseorderh') or self.main_factory.create('PurchaseOrderH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')

        qty = params.get('Qty', Decimal(random.randint(1, 10)))
        price = params.get('Price', Decimal(random.randint(100, 1000)))
        gross = qty * price

        return db_models.PurchaseOrderD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            Unit=material.SmallestUnit,
            Qty=qty,
            Price=price,
            Gross=gross,
            Netto=gross, # Sederhanakan untuk sekarang
            Info='', DiscPercent=0, DiscPercent2=0, DiscPercent3=0, DiscValue=0, DiscNominal=0, QtyReceived=0
        )