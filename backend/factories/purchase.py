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
        self.main_factory.register_builder("PurchaseReturnH", self._build_purchase_return_h)
        self.main_factory.register_builder("PurchaseReturnD", self._build_purchase_return_d)
        self.main_factory.register_builder("GoodsReceiptH", self._build_goods_receipt_h)

        self.main_factory.register_builder("PurchaseCostH", self._build_purchase_cost_h)
        self.main_factory.register_builder("PurchaseCostD", self._build_purchase_cost_d)
        self.main_factory.register_builder("PurchaseInvoiceC", self._build_purchase_invoice_c)
        self.main_factory.register_builder("PurchaseInvoiceDP", self._build_purchase_invoice_dp)
        self.main_factory.register_builder("PurchaseInvoiceGR", self._build_purchase_invoice_gr)
        self.main_factory.register_builder("PurchaseInvoiceH", self._build_purchase_invoice_h)

    def _build_purchase_order_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        currency = supplier.currency_ref or self.main_factory.create('MasterCurrency')
        
        return db_models.PurchaseOrderH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("PO", 15)),
            Series='PO', 
            TransactionType='', 
            DocDate=now.date(), 
            SupplierCode=supplier.Code,
            # PERBAIKAN: Isi SupplierTaxTo dengan nilai yang valid
            SupplierTaxTo=params.get('SupplierTaxTo', supplier.Code),
            DeliveryDate=now.date() + datetime.timedelta(days=7),
            TOP=30, 
            DiscPercent=Decimal('0.0'), 
            TaxStatus='Include', 
            TaxPercent=Decimal('11.0'), 
            Currency=currency.Code, 
            ExchangeRate=Decimal('1.0'), 
            JODocNo='', Trip='', SIDocNo='', 
            TotalGross=Decimal('0.0'), TotalDisc=Decimal('0.0'), TaxValue=Decimal('0.0'), TotalNetto=Decimal('0.0'), 
            CutPPh=False, PPhPercent=Decimal('0.0'), PPhValue=Decimal('0.0'), 
            SendTo='', Information='', Status='OPEN',
            IsApproved=False, 
            PrintCounter=0, 
            IsSalesReturn=False,
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
    def _build_purchase_return_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        # PERBAIKAN: Buat/dapatkan currency secara eksplisit
        currency = params.get('mastercurrency') or self.main_factory.create('MasterCurrency', Code=supplier.Currency)

        return db_models.PurchaseReturnH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("PR", 15)),
            Series='PRT', DocDate=now.date(), SODocNo='', GIDocNo='',
            SupplierCode=supplier.Code, SupplierTaxTo=supplier.Code,
            SupplierDocNo='', TaxNo='', TaxDate=now.date(), Currency=currency.Code,
            ExchangeRate=Decimal('1.0'), TaxStatus='No', TaxPercent=0, TaxPrefix='',
            DiscPercent=0, TotalGross=0, TotalDisc=0, TaxValue=0, TaxValueInTaxCur=0,
            TotalNetto=0, TotalCost=0, Information='Test Purchase Return', Status='OPEN',
            PrintCounter=0, CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_purchase_return_d(self, params):
        header = params.get('purchasereturnh') or self.main_factory.create('PurchaseReturnH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        # PERBAIKAN: Buat/dapatkan unit secara eksplisit, jangan andalkan relasi
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit', Code=material.SmallestUnit)

        return db_models.PurchaseReturnD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code,
            Info='', Qty=Decimal('1.0'), Price=0, Gross=0, DiscPercent=0, DiscPercent2=0,
            DiscPercent3=0, DiscValue=0, DiscNominal=0, Netto=0, Cost=0
        )
    def _build_goods_receipt_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        po = params.get('purchaseorderh') or self.main_factory.create('PurchaseOrderH')
        return db_models.GoodsReceiptH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value('GR', 15)),
            Series='GR', DocDate=now.date(), SupplierCode=po.SupplierCode,
            PODocNo=po.DocNo, Location='', Zone='', SupplierDlvDocNo='',
            VehicleNo='', Information='Test GR', Status='OPEN', PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    def _build_purchase_cost_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        return db_models.PurchaseCostH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("PC", 15)),
            Series='CST', DocDate=now.date(), TransactionType='', SupplierCode=supplier.Code, SupplierTaxTo=supplier.Code,
            SupplierInvNo='', TOP=0, TaxStatus='No', TaxPercent=0, TaxPrefix='', TaxNo='',
            Currency=supplier.Currency, ExchangeRate=1, TotalCost=0, TaxValue=0, TaxValueInTaxCur=0, TotalNetto=0,
            Information='', InvoiceDocNo='', Status='OPEN', IsApproved=True,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    
    def _build_purchase_cost_d(self, params):
        header = params.get('purchasecosth') or self.main_factory.create('PurchaseCostH')
        return db_models.PurchaseCostD(DocNo=header.DocNo, Description='Default Cost', Cost=100)

    def _build_purchase_invoice_c(self, params):
        header = params.get('purchaseinvoiceh') or self.main_factory.create('PurchaseInvoiceH')
        cost_header = self.main_factory.create('PurchaseCostH')
        return db_models.PurchaseInvoiceC(DocNo=header.DocNo, PCDocNo=cost_header.DocNo)

    def _build_purchase_invoice_dp(self, params):
        header = params.get('purchaseinvoiceh') or self.main_factory.create('PurchaseInvoiceH')
        return db_models.PurchaseInvoiceDP(DocNo=header.DocNo, DPDocNo='DP-DUMMY', Usage=1000)

    def _build_purchase_invoice_gr(self, params):
        header = params.get('purchaseinvoiceh') or self.main_factory.create('PurchaseInvoiceH')
        gr_header = self.main_factory.create('GoodsReceiptH')
        return db_models.PurchaseInvoiceGR(DocNo=header.DocNo, GRDocNo=gr_header.DocNo)
    
    def _build_purchase_invoice_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        currency = supplier.currency_ref
        
        return db_models.PurchaseInvoiceH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("PI", 15)),
            Series='INV', DocDate=now.date(), PODocNo='', JODocNo='', Trip='', TransactionType='',
            GRDocNo='', Location='', SupplierCode=supplier.Code, SupplierTaxTo=supplier.Code,
            SupplierInvNo='', TOP=30, Currency=currency.Code, ExchangeRate=1, TotalCost=0,
            CostDistribution='Value', TaxStatus='No', TaxPercent=0, TaxPrefix='', TaxNo='',
            DiscPercent=0, TotalGross=0, TotalDisc=0, DownPayment=0, TaxValue=0,
            TaxValueInTaxCur=0, TotalNetto=0, CutPPh=False, PPhPercent=0, PPhValue=0,
            Information='Test PI', Status='OPEN', PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )