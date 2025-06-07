# backend/app/db_models/finance_models.py
from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class GeneralJournalH(Base):
    __tablename__ = 'generaljournalh'
    
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TotalDebet = Column(Numeric(18, 4), nullable=False)
    TotalCredit = Column(Numeric(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    details = relationship("GeneralJournalD", back_populates="header", cascade="all, delete-orphan")

class GeneralJournalD(Base):
    __tablename__ = 'generaljournald'

    DocNo = Column(String(15), ForeignKey('generaljournalh.DocNo'), primary_key=True)
    Number = Column(Integer, primary_key=True)
    AccountNo = Column(String(20), ForeignKey('masteraccount.AccountNo'), nullable=False)
    Info = Column(String(255), nullable=False)
    Currency = Column(String(3), ForeignKey('mastercurrency.Code'), nullable=False)
    Debet = Column(Numeric(18, 4), nullable=False)
    Credit = Column(Numeric(18, 4), nullable=False)
    ExchangeRate = Column(Numeric(18, 4), nullable=False)
    DebetLocal = Column(Numeric(18, 4), nullable=False)
    CreditLocal = Column(Numeric(18, 4), nullable=False)

    header = relationship("GeneralJournalH", back_populates="details")
    account_ref = relationship("MasterAccount")
    currency_ref = relationship("MasterCurrency")

class Apbook(Base):
    __tablename__ = 'apbook'
    Periode = Column(Date, primary_key=True)
    SupplierCode = Column(String(15), ForeignKey('mastersupplier.Code'), primary_key=True)
    TransType = Column(String(20), ForeignKey('mastertransactiontype.Type'), primary_key=True)
    DocNo = Column(String(40), primary_key=True)
    DocDate = Column(Date, nullable=False)
    TOP = Column(Integer, nullable=False)
    DueDate = Column(Date, nullable=False)
    Currency = Column(String(3), ForeignKey('mastercurrency.Code'), nullable=False)
    ExchangeRate = Column(Numeric(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    DC = Column(String(1), nullable=False)
    DocValue = Column(Numeric(18, 4), nullable=False)
    DocValueLocal = Column(Numeric(18, 4), nullable=False)
    PaymentValue = Column(Numeric(18, 4), nullable=False)
    PaymentValueLocal = Column(Numeric(18, 4), nullable=False)
    ExchangeRateDiff = Column(Numeric(18, 4), nullable=False)

    supplier = relationship("MasterSupplier")
    transaction_type_ref = relationship("MasterTransactionType")
    currency_ref = relationship("MasterCurrency")

class CustomerBalance(Base):
    __tablename__ = 'customerbalance'
    Periode = Column(Date, primary_key=True)
    CustomerCode = Column(String(10), ForeignKey('mastercustomer.Code'), primary_key=True)
    StartBalance = Column(Numeric(18, 4), nullable=False)
    InValue = Column(Numeric(18, 4), nullable=False)
    OutValue = Column(Numeric(18, 4), nullable=False)
    EndBalance = Column(Numeric(18, 4), nullable=False)
    LocalStartBalance = Column(Numeric(18, 4), nullable=False)
    LocalInValue = Column(Numeric(18, 4), nullable=False)
    LocalOutValue = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance = Column(Numeric(18, 4), nullable=False)
    ExchangeRate = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance2 = Column(Numeric(18, 4), nullable=False)
    ExchangeRateDiff = Column(Numeric(18, 4), nullable=False)

    customer = relationship("MasterCustomer")

class SupplierBalance(Base):
    __tablename__ = 'supplierbalance'
    Periode = Column(Date, primary_key=True)
    SupplierCode = Column(String(10), ForeignKey('mastersupplier.Code'), primary_key=True)
    StartBalance = Column(Numeric(18, 4), nullable=False)
    InValue = Column(Numeric(18, 4), nullable=False)
    OutValue = Column(Numeric(18, 4), nullable=False)
    EndBalance = Column(Numeric(18, 4), nullable=False)
    LocalStartBalance = Column(Numeric(18, 4), nullable=False)
    LocalInValue = Column(Numeric(18, 4), nullable=False)
    LocalOutValue = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance = Column(Numeric(18, 4), nullable=False)
    ExchangeRate = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance2 = Column(Numeric(18, 4), nullable=False)
    ExchangeRateDiff = Column(Numeric(18, 4), nullable=False)

    supplier = relationship("MasterSupplier")

class CustomerDPBalance(Base):
    __tablename__ = 'customerdpbalance'
    Periode = Column(Date, primary_key=True)
    CustomerCode = Column(String(10), ForeignKey('mastercustomer.Code'), primary_key=True)
    StartBalance = Column(Numeric(18, 4), nullable=False)
    InValue = Column(Numeric(18, 4), nullable=False)
    OutValue = Column(Numeric(18, 4), nullable=False)
    EndBalance = Column(Numeric(18, 4), nullable=False)
    LocalStartBalance = Column(Numeric(18, 4), nullable=False)
    LocalInValue = Column(Numeric(18, 4), nullable=False)
    LocalOutValue = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance = Column(Numeric(18, 4), nullable=False)
    ExchangeRate = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance2 = Column(Numeric(18, 4), nullable=False)
    ExchangeRateDiff = Column(Numeric(18, 4), nullable=False)

    customer = relationship("MasterCustomer")

class SupplierDPBalance(Base):
    __tablename__ = 'supplierdpbalance'
    Periode = Column(Date, primary_key=True)
    SupplierCode = Column(String(10), ForeignKey('mastersupplier.Code'), primary_key=True)
    StartBalance = Column(Numeric(18, 4), nullable=False)
    InValue = Column(Numeric(18, 4), nullable=False)
    OutValue = Column(Numeric(18, 4), nullable=False)
    EndBalance = Column(Numeric(18, 4), nullable=False)
    LocalStartBalance = Column(Numeric(18, 4), nullable=False)
    LocalInValue = Column(Numeric(18, 4), nullable=False)
    LocalOutValue = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance = Column(Numeric(18, 4), nullable=False)
    ExchangeRate = Column(Numeric(18, 4), nullable=False)
    LocalEndBalance2 = Column(Numeric(18, 4), nullable=False)
    ExchangeRateDiff = Column(Numeric(18, 4), nullable=False)
    
    supplier = relationship("MasterSupplier")