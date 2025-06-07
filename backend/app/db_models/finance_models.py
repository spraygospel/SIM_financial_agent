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