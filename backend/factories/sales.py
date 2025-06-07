# backend/factories/sales.py
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal
import random

class SalesFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("SalesOrderH", self._build_sales_order_h)
        self.main_factory.register_builder("SalesOrderD", self._build_sales_order_d)
        self.main_factory.register_builder("Arbook", self._build_ar_book)
        self.main_factory.register_builder("ArRequestListH", self._build_ar_request_list_h)
        self.main_factory.register_builder("SalesInvoiceH", self._build_sales_invoice_h)
        self.main_factory.register_builder("SalesInvoiceD", self._build_sales_invoice_d)
        self.main_factory.register_builder("GoodsIssueH", self._build_goods_issue_h)
        self.main_factory.register_builder("SalesReturnH", self._build_sales_return_h)
        self.main_factory.register_builder("SalesReturnD", self._build_sales_return_d)
        self.main_factory.register_builder("CustomerPaymentH", self._build_customer_payment_h)
        self.main_factory.register_builder("CustomerPaymentD", self._build_customer_payment_d)

        self.main_factory.register_builder("SalesInvoiceDP", self._build_sales_invoice_dp)
        self.main_factory.register_builder("SalesInvoiceGI", self._build_sales_invoice_gi)
        self.main_factory.register_builder("SalesOrderRD", self._build_sales_order_rd)
        self.main_factory.register_builder("SalesOrderRS", self._build_sales_order_rs)
        self.main_factory.register_builder("SalesOrderSch", self._build_sales_order_sch)
        

    def _build_sales_order_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Buat dependensi secara otomatis jika tidak disediakan
        customer = params.get('mastercustomer') or self.main_factory.create('MasterCustomer')
        tax_to_customer = params.get('tax_to_customer') or customer # Gunakan customer yang sama jika tidak ada
        sales_person = params.get('mastersales') or self.main_factory.create('MasterSales')
        currency = params.get('mastercurrency') or self.main_factory.create('MasterCurrency')
        
        return db_models.SalesOrderH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("SO", 15)),
            Series='SO',
            DocDate=now.date(),
            CustomerCode=customer.Code,
            ShipToCode=params.get('ShipToCode', customer.Code),
            TaxToCode=tax_to_customer.Code,
            SalesCode=sales_person.Code,
            DeliveryDate=now.date() + datetime.timedelta(days=7),
            PONo='', TOP=30, DiscPercent=Decimal('0.0'), TaxStatus='Include', TaxPercent=Decimal('11.0'),
            Currency=currency.Code, ExchangeRate=Decimal('1.0'), TotalGross=Decimal('0.0'),
            TotalDisc=Decimal('0.0'), TaxValue=Decimal('0.0'), TotalNetto=Decimal('0.0'),
            PPhStatus='', CutPPh=False, PPhPercent=Decimal('0.0'), PPhValue=Decimal('0.0'),
            Information='', Status='OPEN', IsPurchaseReturn=False, IsApproved=False,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_sales_order_d(self, params):
        header = params.get('salesorderh') or self.main_factory.create('SalesOrderH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')

        qty = params.get('Qty', Decimal(random.randint(1, 10)))
        price = params.get('Price', Decimal(random.randint(1000, 5000)))
        gross = qty * price

        return db_models.SalesOrderD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            Unit=material.SmallestUnit,
            Qty=qty, Price=price, Gross=gross, Netto=gross,
            Info='', DiscPercent=0, DiscPercent2=0, DiscPercent3=0, DiscValue=0, DiscNominal=0,
            QtyDelivered=0, QtyWO=0, QtyBooked=0, PromoQty=0
        )
    def _build_sales_invoice_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        
        so_header = params.get('salesorderh') or self.main_factory.create('SalesOrderH')
        goods_issue = params.get('goodsissueh') or self.main_factory.create('GoodsIssueH', salesorderh=so_header)
        location = goods_issue.location_ref
        
        customer = so_header.customer
        tax_to_customer = so_header.tax_to_customer_ref
        sales_person = so_header.sales_person_ref

        return db_models.SalesInvoiceH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("SI", 15)),
            Series='SI', DocDate=now.date(), SODocNo=so_header.DocNo, GIDocNo=goods_issue.DocNo,
            Location=location.Code, PONo='', CustomerCode=customer.Code,
            TaxToCode=tax_to_customer.Code, SalesCode=sales_person.Code, TOP=so_header.TOP,
            Currency=so_header.Currency, ExchangeRate=so_header.ExchangeRate, TaxStatus='Include',
            TaxPercent=11, TaxPrefix='', TaxNo='', DiscPercent=0, TotalGross=0, TotalDisc=0,
            DownPayment=0, TaxValue=0, TaxValueInTaxCur=0, TotalNetto=0, TotalCost=0,
            PPhStatus='', CutPPh=False, PPhPercent=0, PPhValue=0, Information='', Status='OPEN',
            PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_ar_book(self, params):
        print("  [DEBUG] Membangun Arbook...")
        now = datetime.datetime.now(datetime.timezone.utc)
        invoice = params.get('salesinvoiceh') or self.main_factory.create('SalesInvoiceH')

        if not invoice: print("    [DEBUG] invoice TIDAK ADA!")
        elif not invoice.customer: print("    [DEBUG] invoice.customer TIDAK ADA!")
        else: print(f"    [DEBUG] invoice.customer.Code: {invoice.customer.Code}")

        customer = invoice.customer
        trans_type = params.get('mastertransactiontype') or self.main_factory.create('MasterTransactionType')
        return db_models.Arbook(
            Periode=now.date().replace(day=1),
            CustomerCode=customer.Code,
            TransType=trans_type.Type,
            DocNo=invoice.DocNo,
            DocDate=invoice.DocDate,
            TOP=invoice.TOP,
            DueDate=invoice.DocDate + datetime.timedelta(days=invoice.TOP),
            Currency=invoice.Currency,
            ExchangeRate=invoice.ExchangeRate,
            Information='',
            DC='D',
            DocValue=params.get('DocValue', Decimal('1000.0')),
            DocValueLocal=params.get('DocValueLocal', Decimal('1000.0')),
            PaymentValue=Decimal('0.0'),
            PaymentValueLocal=Decimal('0.0'),
            ExchangeRateDiff=Decimal('0.0')
        )
    def _build_goods_issue_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        so_header = params.get('salesorderh') or self.main_factory.create('SalesOrderH')
        location = params.get('masterlocation') or self.main_factory.create('MasterLocation')
        
        return db_models.GoodsIssueH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("GI", 15)),
            Series='GI',
            DocDate=now.date(),
            SODocNo=so_header.DocNo,
            CustomerCode=so_header.CustomerCode,
            ShipToCode=so_header.ShipToCode,
            Location=location.Code,
            Zone='', PONo='', VehicleNo='', PackingListNo='', ShipmentDocNo='',
            Information='Test Goods Issue', Status='OPEN', PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    def _build_sales_return_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        customer = params.get('mastercustomer') or self.main_factory.create('MasterCustomer')
        
        return db_models.SalesReturnH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("SR", 15)),
            Series='SAR', DocDate=now.date(), PODocNo='', GRDocNo='', SIDocNo='',
            CustomerCode=customer.Code, CustomerTaxTo=customer.Code, SalesCode='',
            Currency=customer.Currency, ExchangeRate=Decimal('1.0'), TaxStatus='No', TaxPercent=0,
            TaxPrefix='', TaxNo='', TaxDate=now.date(), DiscPercent=0, TotalGross=0,
            TotalDisc=0, TaxValue=0, TaxValueInTaxCur=0, TotalNetto=0, TotalCost=0,
            Information='Test Sales Return', Status='OPEN', PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_sales_return_d(self, params):
        header = params.get('salesreturnh') or self.main_factory.create('SalesReturnH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit', Code=material.SmallestUnit)
        
        return db_models.SalesReturnD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code,
            Info='', OriginalTagNo='', Qty=Decimal('1.0'), Price=Decimal('0.0'), Gross=Decimal('0.0'),
            DiscPercent=0, DiscPercent2=0, DiscPercent3=0, DiscValue=0, DiscNominal=0,
            Netto=Decimal('0.0'), Cost=Decimal('0.0')
        )
    def _build_ar_request_list_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        collector = params.get('mastercollector') or self.main_factory.create('MasterCollector')
        return db_models.ArRequestListH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value('ARL', 15)),
            Series='ARL', DocDate=now.date(), CollectorCode=collector.Code,
            TotalCustomer=0, TotalDocument=0, TotalValue=0, Information='', Status='OPEN',
            PrintCounter=0, CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_customer_payment_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        ar_req_list = params.get('arrequestlisth') or self.main_factory.create('ArRequestListH')
        return db_models.CustomerPaymentH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value('CP', 15)),
            Series='CUP', DocDate=now.date(), ARReqListNo=ar_req_list.DocNo,
            TotalCustomer=0, TotalDocument=0, TotalPayment=0, Information='', Status='OPEN',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_customer_payment_d(self, params):
        header = params.get('customerpaymenth') or self.main_factory.create('CustomerPaymentH')
        customer = params.get('mastercustomer') or self.main_factory.create('MasterCustomer')
        trans_type = params.get('mastertransactiontype') or self.main_factory.create('MasterTransactionType')
        currency = customer.currency_ref
        return db_models.CustomerPaymentD(
            DocNo=header.DocNo, TransactionType=trans_type.Type, CustomerCode=customer.Code,
            ARDocNo=params.get('ARDocNo', self.main_factory.get_unique_value('ARD', 16)),
            DC='D', Currency=currency.Code, Payment=0, ExchangeRate=1, PaymentLocal=0,
            TaxPrefix='', TaxNo='', Information=''
        )

    def _build_sales_invoice_d(self, params):
        header = params.get('salesinvoiceh') or self.main_factory.create('SalesInvoiceH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        unit = material.smallest_unit_ref
        return db_models.SalesInvoiceD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code, Info='', Qty=1, Price=0, Gross=0, DiscPercent=0,
            DiscPercent2=0, DiscPercent3=0, DiscValue=0, DiscNominal=0, Netto=0, Cost=0
        )
    def _build_sales_invoice_dp(self, params):
        header = params.get('salesinvoiceh') or self.main_factory.create('SalesInvoiceH')
        return db_models.SalesInvoiceDP(DocNo=header.DocNo, DPDocNo='DP-DUMMY', Usage=1000)

    def _build_sales_invoice_gi(self, params):
        header = params.get('salesinvoiceh') or self.main_factory.create('SalesInvoiceH')
        gi_header = self.main_factory.create('GoodsIssueH')
        return db_models.SalesInvoiceGI(DocNo=header.DocNo, GIDocNo=gi_header.DocNo)

    def _build_sales_order_rd(self, params):
        so_detail = params.get('salesorderd') or self.main_factory.create('SalesOrderD')
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        return db_models.SalesOrderRD(DocNo=so_detail.DocNo, Number=so_detail.Number, SupplierCode=supplier.Code, RebateCode='', RebatePercent=0, DocValue=0, RebateValue=0)

    def _build_sales_order_rs(self, params):
        header = params.get('salesorderh') or self.main_factory.create('SalesOrderH')
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        return db_models.SalesOrderRS(DocNo=header.DocNo, SupplierCode=supplier.Code)

    def _build_sales_order_sch(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        so_detail = params.get('salesorderd') or self.main_factory.create('SalesOrderD')
        return db_models.SalesOrderSch(DocNo=so_detail.DocNo, Number=so_detail.Number, DeliveryDate=now.date(), Qty=1)