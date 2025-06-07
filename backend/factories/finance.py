# backend/factories/finance.py
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal
import random

class FinanceFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("GeneralJournalH", self._build_general_journal_h)
        self.main_factory.register_builder("GeneralJournalD", self._build_general_journal_d)
        self.main_factory.register_builder("Apbook", self._build_ap_book)
        self.main_factory.register_builder("CustomerBalance", self._build_customer_balance)
        self.main_factory.register_builder("SupplierBalance", self._build_supplier_balance)
        self.main_factory.register_builder("CustomerDPBalance", self._build_customer_dp_balance)
        self.main_factory.register_builder("SupplierDPBalance", self._build_supplier_dp_balance)

    def _build_general_journal_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.GeneralJournalH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("GJ", 15)),
            Series='GJP', DocDate=now.date(), TotalDebet=0, TotalCredit=0,
            Information='Test Journal', Status='OPEN', PrintCounter=0, PrintedBy='',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_general_journal_d(self, params):
        header = params.get('generaljournalh') or self.main_factory.create('GeneralJournalH')
        account = params.get('masteraccount') or self.main_factory.create('MasterAccount')
        # PERBAIKAN: Buat/dapatkan currency secara eksplisit, jangan andalkan relasi
        currency = params.get('mastercurrency') or self.main_factory.create('MasterCurrency', Code=account.Currency)

        return db_models.GeneralJournalD(
            DocNo=header.DocNo,
            Number=params.get('Number', self.main_factory.get_unique_value('Line', 3)),
            AccountNo=account.AccountNo,
            Info='Test Journal Detail',
            Currency=currency.Code,
            Debet=params.get('Debet', Decimal('100.0')),
            Credit=params.get('Credit', Decimal('0.0')),
            ExchangeRate=Decimal('1.0'),
            DebetLocal=params.get('Debet', Decimal('100.0')),
            CreditLocal=params.get('Credit', Decimal('0.0')),
        )
    def _build_ap_book(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        trans_type = params.get('mastertransactiontype') or self.main_factory.create('MasterTransactionType')
        
        return db_models.Apbook(
            Periode=now.date().replace(day=1),
            SupplierCode=supplier.Code,
            TransType=trans_type.Type,
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("AP", 40)),
            DocDate=now.date(),
            TOP=30,
            DueDate=now.date() + datetime.timedelta(days=30),
            Currency=supplier.Currency,
            ExchangeRate=Decimal('1.0'),
            Information='Test AP Book', DC='D', DocValue=Decimal('100.0'),
            DocValueLocal=Decimal('100.0'), PaymentValue=0, PaymentValueLocal=0, ExchangeRateDiff=0
        )

    def _build_customer_balance(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        customer = params.get('mastercustomer') or self.main_factory.create('MasterCustomer')
        return db_models.CustomerBalance(
            Periode=now.date().replace(day=1), CustomerCode=customer.Code,
            StartBalance=0, InValue=0, OutValue=0, EndBalance=0,
            LocalStartBalance=0, LocalInValue=0, LocalOutValue=0, LocalEndBalance=0,
            ExchangeRate=1, LocalEndBalance2=0, ExchangeRateDiff=0
        )

    def _build_supplier_balance(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        return db_models.SupplierBalance(
            Periode=now.date().replace(day=1), SupplierCode=supplier.Code,
            StartBalance=0, InValue=0, OutValue=0, EndBalance=0,
            LocalStartBalance=0, LocalInValue=0, LocalOutValue=0, LocalEndBalance=0,
            ExchangeRate=1, LocalEndBalance2=0, ExchangeRateDiff=0
        )

    def _build_customer_dp_balance(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        customer = params.get('mastercustomer') or self.main_factory.create('MasterCustomer')
        return db_models.CustomerDPBalance(
            Periode=now.date().replace(day=1), CustomerCode=customer.Code,
            StartBalance=0, InValue=0, OutValue=0, EndBalance=0,
            LocalStartBalance=0, LocalInValue=0, LocalOutValue=0, LocalEndBalance=0,
            ExchangeRate=1, LocalEndBalance2=0, ExchangeRateDiff=0
        )

    def _build_supplier_dp_balance(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        supplier = params.get('mastersupplier') or self.main_factory.create('MasterSupplier')
        return db_models.SupplierDPBalance(
            Periode=now.date().replace(day=1), SupplierCode=supplier.Code,
            StartBalance=0, InValue=0, OutValue=0, EndBalance=0,
            LocalStartBalance=0, LocalInValue=0, LocalOutValue=0, LocalEndBalance=0,
            ExchangeRate=1, LocalEndBalance2=0, ExchangeRateDiff=0
        )