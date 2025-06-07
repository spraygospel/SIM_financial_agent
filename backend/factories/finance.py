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
        currency = account.currency_ref

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