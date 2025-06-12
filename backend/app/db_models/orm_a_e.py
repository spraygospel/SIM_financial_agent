from sqlalchemy import Column, Integer, String, Text, DECIMAL, Float, Date, DateTime, Boolean, TIMESTAMP, CHAR, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Accountbalance(Base):
    __tablename__ = 'accountbalance'

    Year = Column(Integer, primary_key=True, nullable=False)
    AccountNo = Column(String(20), primary_key=True, nullable=False)
    Debet = Column(DECIMAL(18, 4), nullable=False)
    Credit = Column(DECIMAL(18, 4), nullable=False)
    DebetLocal = Column(DECIMAL(18, 4), nullable=False)
    CreditLocal = Column(DECIMAL(18, 4), nullable=False)

class Accounttotal(Base):
    __tablename__ = 'accounttotal'

    Periode = Column(Date, primary_key=True, nullable=False)
    AccountNo = Column(String(20), primary_key=True, nullable=False)
    BusinessUnit = Column(String(20), primary_key=True, nullable=False)
    Debet = Column(DECIMAL(18, 4), nullable=False)
    Credit = Column(DECIMAL(18, 4), nullable=False)
    DebetLocal = Column(DECIMAL(18, 4), nullable=False)
    CreditLocal = Column(DECIMAL(18, 4), nullable=False)

class Actionlog(Base):
    __tablename__ = 'actionlog'

    ActionTime = Column(DateTime, primary_key=True, nullable=False)
    ActionBy = Column(String(16), primary_key=True, nullable=False)
    Action = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    Reason = Column(String(255), nullable=False)

class Adjustind(Base):
    __tablename__ = 'adjustind'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    AssumedPrice = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_adjustind_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="adjustind_collection", foreign_keys=[MaterialCode, Unit])

class Adjustinh(Base):
    __tablename__ = 'adjustinh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    AODocNo = Column(String(15), nullable=False)
    IsOutsource = Column(Boolean, nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    TotalPrice = Column(DECIMAL(18, 4), nullable=False)
    TotalAssumedPrice = Column(DECIMAL(18, 4), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16), nullable=False)
    ApprovedDate = Column(DateTime)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_adjustinh_masterlocation_0', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="adjustinh_collection", foreign_keys=[Location])

class Adjustoutd(Base):
    __tablename__ = 'adjustoutd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    BaseQty = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_adjustoutd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="adjustoutd_collection", foreign_keys=[MaterialCode, Unit])

class Adjustouth(Base):
    __tablename__ = 'adjustouth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16), nullable=False)
    ApprovedDate = Column(DateTime)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_adjustouth_masterlocation_0', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="adjustouth_collection", foreign_keys=[Location])

class Apbook(Base):
    __tablename__ = 'apbook'

    Periode = Column(Date, primary_key=True, nullable=False)
    SupplierCode = Column(String(15), primary_key=True, nullable=False)
    TransType = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(40), primary_key=True, nullable=False)
    DocDate = Column(Date, nullable=False)
    TOP = Column(Integer, nullable=False)
    DueDate = Column(Date, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    DC = Column(CHAR(1), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    DocValueLocal = Column(DECIMAL(18, 4), nullable=False)
    PaymentValue = Column(DECIMAL(18, 4), nullable=False)
    PaymentValueLocal = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRateDiff = Column(DECIMAL(18, 4), nullable=False)

class Apclearinggirod(Base):
    __tablename__ = 'apclearinggirod'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    CashierPaymentNo = Column(String(15), primary_key=True, nullable=False)
    Bank = Column(String(5), primary_key=True, nullable=False)
    GiroNo = Column(String(20), primary_key=True, nullable=False)

class Apclearinggiroh(Base):
    __tablename__ = 'apclearinggiroh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TransType = Column(String(20), nullable=False)
    TotalDocument = Column(Integer, nullable=False)
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Apcreditnote(Base):
    __tablename__ = 'apcreditnote'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    TaxToCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Apdebetnote(Base):
    __tablename__ = 'apdebetnote'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    TaxToCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Apdownpayment(Base):
    __tablename__ = 'apdownpayment'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    SupplierTaxTo = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    DownPayment = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    DownPaymentNetto = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Apreceiptlistd(Base):
    __tablename__ = 'apreceiptlistd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    APDocNo = Column(String(17), primary_key=True, nullable=False)

class Apreceiptlisth(Base):
    __tablename__ = 'apreceiptlisth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TotalSupplier = Column(Integer, nullable=False)
    TotalDocument = Column(Integer, nullable=False)
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Aprejectgiro(Base):
    __tablename__ = 'aprejectgiro'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CashierPaymentNo = Column(String(15), nullable=False)
    Bank = Column(String(5), nullable=False)
    GiroNo = Column(String(20), nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    GiroValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Apsettlement(Base):
    __tablename__ = 'apsettlement'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    APRecListNo = Column(String(15))
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Arbook(Base):
    __tablename__ = 'arbook'

    Periode = Column(Date, primary_key=True, nullable=False)
    CustomerCode = Column(String(15), primary_key=True, nullable=False)
    TransType = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(40), primary_key=True, nullable=False)
    DocDate = Column(Date, nullable=False)
    TOP = Column(Integer, nullable=False)
    DueDate = Column(Date, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    DC = Column(CHAR(1), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    DocValueLocal = Column(DECIMAL(18, 4), nullable=False)
    PaymentValue = Column(DECIMAL(18, 4), nullable=False)
    PaymentValueLocal = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRateDiff = Column(DECIMAL(18, 4), nullable=False)

class Arclearinggirod(Base):
    __tablename__ = 'arclearinggirod'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    CashierReceiptNo = Column(String(15), primary_key=True, nullable=False)
    Bank = Column(String(5), primary_key=True, nullable=False)
    GiroNo = Column(String(20), primary_key=True, nullable=False)

class Arclearinggiroh(Base):
    __tablename__ = 'arclearinggiroh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TransType = Column(String(20), nullable=False)
    TotalDocument = Column(Integer, nullable=False)
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Arcreditnote(Base):
    __tablename__ = 'arcreditnote'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    TaxToCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Ardebetnote(Base):
    __tablename__ = 'ardebetnote'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    TaxToCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Ardownpayment(Base):
    __tablename__ = 'ardownpayment'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    CustomerTaxTo = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    DownPayment = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    DownPaymentNetto = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Arperiode(Base):
    __tablename__ = 'arperiode'

    Periode = Column(Date, primary_key=True, nullable=False)
    IsClosed = Column(Boolean, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Arrejectgiro(Base):
    __tablename__ = 'arrejectgiro'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CashierReceiptNo = Column(String(15), nullable=False)
    Bank = Column(String(5), nullable=False)
    GiroNo = Column(String(20), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    GiroValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Arrequestlistd(Base):
    __tablename__ = 'arrequestlistd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    ARDocNo = Column(String(17), primary_key=True, nullable=False)

class Arrequestlisth(Base):
    __tablename__ = 'arrequestlisth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CollectorCode = Column(String(10), nullable=False)
    TotalCustomer = Column(Integer, nullable=False)
    TotalDocument = Column(Integer, nullable=False)
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Arsettlement(Base):
    __tablename__ = 'arsettlement'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    ARReqListNo = Column(String(15), nullable=False)
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Asset(Base):
    __tablename__ = 'asset'

    AssetNo = Column(String(20), primary_key=True, nullable=False)
    AssetName = Column(String(80), nullable=False)
    BusinessUnit = Column(String(20), nullable=False)
    DocNo = Column(String(15), nullable=False)
    Number = Column(Integer, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    PurchaseDate = Column(Date, nullable=False)
    PurchaseValue = Column(DECIMAL(18, 4), nullable=False)
    BaseDate = Column(Date, nullable=False)
    BaseValue = Column(DECIMAL(18, 4), nullable=False)
    SalvagePercentage = Column(DECIMAL(18, 4), nullable=False)
    SalvageValue = Column(DECIMAL(18, 4), nullable=False)
    DepreciationRun = Column(Boolean, nullable=False)
    DepreciationStartDate = Column(Date)
    Age = Column(Integer, nullable=False)
    DepreciationValuePerYear = Column(DECIMAL(18, 4), nullable=False)
    LastDepreciationRun = Column(Date, nullable=False)
    AccDepreciationValue = Column(DECIMAL(18, 4), nullable=False)
    BookValue = Column(DECIMAL(18, 4), nullable=False)
    SellDocNo = Column(String(15), nullable=False)
    SellNumber = Column(Integer, nullable=False)
    SellDate = Column(Date)
    SellValue = Column(DECIMAL(18, 4), nullable=False)

class Assetdd(Base):
    __tablename__ = 'assetdd'

    AssetNo = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    Percentage = Column(DECIMAL(18, 4), nullable=False)
    DepreciationValue = Column(DECIMAL(18, 4), nullable=False)

class Aucsettlement(Base):
    __tablename__ = 'aucsettlement'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TransactionType = Column(String(20), nullable=False)
    AssetNo = Column(String(20), nullable=False)
    AssetName = Column(String(80), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    DepreciationRun = Column(Boolean, nullable=False)
    Age = Column(Integer, nullable=False)
    SalvagePercentage = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Batch(Base):
    __tablename__ = 'batch'

    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date)

class Booking(Base):
    __tablename__ = 'booking'

    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(50), primary_key=True, nullable=False)
    DocDate = Column(Date, primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Bookstockb(Base):
    __tablename__ = 'bookstockb'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Bookstockd(Base):
    __tablename__ = 'bookstockd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(255), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    QtyUsed = Column(DECIMAL(18, 4), nullable=False)

class Bookstockh(Base):
    __tablename__ = 'bookstockh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    JODocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Cashierpaymentd(Base):
    __tablename__ = 'cashierpaymentd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    TransType = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(255), nullable=False)
    DC = Column(CHAR(1), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    Value = Column(DECIMAL(18, 4), nullable=False)
    ValueLocal = Column(DECIMAL(18, 4), nullable=False)
    JODocNo = Column(String(15), nullable=False)

class Cashierpaymentg(Base):
    __tablename__ = 'cashierpaymentg'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Bank = Column(String(5), primary_key=True, nullable=False)
    GiroNo = Column(String(20), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    GiroValue = Column(DECIMAL(18, 4), nullable=False)
    GiroValueLocal = Column(DECIMAL(18, 4), nullable=False)
    TransType = Column(String(20), nullable=False)
    IssuedDate = Column(Date, nullable=False)
    DueDate = Column(Date)
    ClearingDate = Column(Date)
    ClearExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    ClearValue = Column(DECIMAL(18, 4), nullable=False)
    RejectDate = Column(Date)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Cashierpaymenth(Base):
    __tablename__ = 'cashierpaymenth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    APRecListNo = Column(String(15))
    TotalDebet = Column(DECIMAL(18, 4), nullable=False)
    TotalCredit = Column(DECIMAL(18, 4), nullable=False)
    TotalGiro = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Cashierreceiptd(Base):
    __tablename__ = 'cashierreceiptd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    TransType = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(255), nullable=False)
    DC = Column(CHAR(1), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    Value = Column(DECIMAL(18, 4), nullable=False)
    ValueLocal = Column(DECIMAL(18, 4), nullable=False)

class Cashierreceiptg(Base):
    __tablename__ = 'cashierreceiptg'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Bank = Column(String(5), primary_key=True, nullable=False)
    GiroNo = Column(String(20), primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    GiroValue = Column(DECIMAL(18, 4), nullable=False)
    GiroValueLocal = Column(DECIMAL(18, 4), nullable=False)
    TransType = Column(String(20), nullable=False)
    ReceivedDate = Column(Date, nullable=False)
    DepositDate = Column(Date)
    DueDate = Column(Date)
    ClearingDate = Column(Date)
    ClearExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    ClearValue = Column(DECIMAL(18, 4), nullable=False)
    RejectDate = Column(Date)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Cashierreceipth(Base):
    __tablename__ = 'cashierreceipth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    ARReqListNo = Column(String(15), nullable=False)
    TotalDebet = Column(DECIMAL(18, 4), nullable=False)
    TotalCredit = Column(DECIMAL(18, 4), nullable=False)
    TotalGiro = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Cfproject(Base):
    __tablename__ = 'cfproject'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    PlannedStartDate = Column(Date, nullable=False)
    PlannedFinishDate = Column(Date, nullable=False)
    ActualStartDate = Column(Date, nullable=False)
    ActualFinishDate = Column(Date, nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    PIC = Column(String(40), nullable=False)
    Priority = Column(Integer, nullable=False)
    Location = Column(String(80), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    Status = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(15), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(15), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Changepriced(Base):
    __tablename__ = 'changepriced'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    PriceListType = Column(String(5), primary_key=True, nullable=False)
    Unit = Column(String(5), primary_key=True, nullable=False)
    MinQty = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    MaxQty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    PercentDisc = Column(DECIMAL(18, 4), nullable=False)
    PercentDisc2 = Column(DECIMAL(18, 4), nullable=False)
    PercentDisc3 = Column(DECIMAL(18, 4), nullable=False)
    ValueDisc = Column(DECIMAL(18, 4), nullable=False)

class Changepriceh(Base):
    __tablename__ = 'changepriceh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Currency = Column(String(3), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16))
    ApprovedDate = Column(DateTime)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Controlposition(Base):
    __tablename__ = 'controlposition'

    Form = Column(String(50), primary_key=True, nullable=False)
    Control = Column(String(50), primary_key=True, nullable=False)
    Left = Column(Integer, nullable=False)
    Top = Column(Integer, nullable=False)
    Width = Column(Integer, nullable=False)
    Height = Column(Integer, nullable=False)
    Container = Column(String(50), nullable=False)

class Cubepointofsale(Base):
    __tablename__ = 'cubepointofsale'

    DocDate = Column(Date, primary_key=True, nullable=False)
    Series = Column(String(3), primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    SalesCode = Column(String(10), primary_key=True, nullable=False)
    CustomerCode = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    BaseQty = Column(DECIMAL(40, 4))
    Netto = Column(DECIMAL(40, 4))
    Cost = Column(DECIMAL(40, 4))
    DiscNominalAndHeaderDisc = Column(DECIMAL(63, 12))
    NettoAfterHeaderDisc = Column(DECIMAL(63, 12))

class Customerbalance(Base):
    __tablename__ = 'customerbalance'

    Periode = Column(Date, primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    StartBalance = Column(DECIMAL(18, 4), nullable=False)
    InValue = Column(DECIMAL(18, 4), nullable=False)
    OutValue = Column(DECIMAL(18, 4), nullable=False)
    EndBalance = Column(DECIMAL(18, 4), nullable=False)
    LocalStartBalance = Column(DECIMAL(18, 4), nullable=False)
    LocalInValue = Column(DECIMAL(18, 4), nullable=False)
    LocalOutValue = Column(DECIMAL(18, 4), nullable=False)
    LocalEndBalance = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    LocalEndBalance2 = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRateDiff = Column(DECIMAL(18, 4), nullable=False)

class Customerdpbalance(Base):
    __tablename__ = 'customerdpbalance'

    Periode = Column(Date, primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    StartBalance = Column(DECIMAL(18, 4), nullable=False)
    InValue = Column(DECIMAL(18, 4), nullable=False)
    OutValue = Column(DECIMAL(18, 4), nullable=False)
    EndBalance = Column(DECIMAL(18, 4), nullable=False)
    LocalStartBalance = Column(DECIMAL(18, 4), nullable=False)
    LocalInValue = Column(DECIMAL(18, 4), nullable=False)
    LocalOutValue = Column(DECIMAL(18, 4), nullable=False)
    LocalEndBalance = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    LocalEndBalance2 = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRateDiff = Column(DECIMAL(18, 4), nullable=False)

class Customerpaymentd(Base):
    __tablename__ = 'customerpaymentd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TransactionType = Column(String(20), primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    ARDocNo = Column(String(16), primary_key=True, nullable=False)
    DC = Column(CHAR(1), nullable=False)
    Currency = Column(String(3), nullable=False)
    Payment = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    PaymentLocal = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    Information = Column(String(255))

class Customerpaymenth(Base):
    __tablename__ = 'customerpaymenth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    ARReqListNo = Column(String(15), nullable=False)
    TotalCustomer = Column(Integer, nullable=False)
    TotalDocument = Column(Integer, nullable=False)
    TotalPayment = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Customerpoint(Base):
    __tablename__ = 'customerpoint'

    DocDate = Column(Date, primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Customerpointbalance(Base):
    __tablename__ = 'customerpointbalance'

    Year = Column(Integer, primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    StartQty = Column(DECIMAL(18, 4), nullable=False)
    InQty = Column(DECIMAL(18, 4), nullable=False)
    OutQty = Column(DECIMAL(18, 4), nullable=False)
    EndQty = Column(DECIMAL(18, 4), nullable=False)

class Customervisitd(Base):
    __tablename__ = 'customervisitd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    OrderNo = Column(Integer, nullable=False)
    IsScheduled = Column(Boolean, nullable=False)
    StartTime = Column(String(255))
    EndTime = Column(String(255))
    Latitude = Column(DECIMAL(18, 7))
    Longitude = Column(DECIMAL(18, 7))
    Distance = Column(DECIMAL(18, 4))

class Customervisith(Base):
    __tablename__ = 'customervisith'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    EmployeeNo = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    StartTime = Column(String(255))
    EndTime = Column(String(255))
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Cyclecountd(Base):
    __tablename__ = 'cyclecountd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    CountQty = Column(DECIMAL(18, 4))
    StockQty = Column(DECIMAL(18, 4))
    DiffQty = Column(DECIMAL(18, 4))

class Cyclecounth(Base):
    __tablename__ = 'cyclecounth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    UseTagNo = Column(Boolean, nullable=False)
    NoCountSince = Column(Date, nullable=False)
    AdjustInDocNo = Column(String(15), nullable=False)
    AdjustOutDocNo = Column(String(15), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16))
    ApprovedDate = Column(DateTime)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Datalog(Base):
    __tablename__ = 'datalog'

    LogDate = Column(Date, primary_key=True, nullable=False)
    LogTime = Column(String(255), nullable=False)
    User = Column(String(16), nullable=False)
    Query = Column(String(4096), nullable=False)

class Datatransferlog(Base):
    __tablename__ = 'datatransferlog'

    Server = Column(String(10), primary_key=True, nullable=False)
    Table = Column(String(30), primary_key=True, nullable=False)
    KeyValue = Column(String(50), primary_key=True, nullable=False)
    AllowChange = Column(Boolean, nullable=False)
    TransferDate = Column(DateTime, nullable=False)

class Datatransferlogsummary(Base):
    __tablename__ = 'datatransferlogsummary'

    TransferDate = Column(DateTime, primary_key=True, nullable=False)
    TransferBy = Column(String(16), primary_key=True, nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    Mode = Column(String(10), primary_key=True, nullable=False)
    Server = Column(String(10), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Title = Column(String(100), nullable=False)
    TotalRow = Column(Integer, nullable=False)
    Error = Column(Text, nullable=False)

class Debtpaymentd(Base):
    __tablename__ = 'debtpaymentd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TransactionType = Column(String(20), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    APDocNo = Column(String(16), primary_key=True, nullable=False)
    DC = Column(CHAR(1), nullable=False)
    Currency = Column(String(3), nullable=False)
    Payment = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    PaymentLocal = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    Information = Column(String(255))

class Debtpaymenth(Base):
    __tablename__ = 'debtpaymenth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    APRecListNo = Column(String(15))
    TotalSupplier = Column(Integer, nullable=False)
    TotalDocument = Column(Integer, nullable=False)
    TotalPayment = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Deliveryreturnd(Base):
    __tablename__ = 'deliveryreturnd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    QtyReturn = Column(DECIMAL(18, 4), nullable=False)

class Deliveryreturnh(Base):
    __tablename__ = 'deliveryreturnh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    GIDocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    Zone = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Dialogcustomization(Base):
    __tablename__ = 'dialogcustomization'

    DialogName = Column(String(50), primary_key=True, nullable=False)
    Variant = Column(String(20), primary_key=True, nullable=False)
    SimpleMode = Column(Boolean, nullable=False)
    SelectFields = Column(String(2048), nullable=False)
    FilterFields = Column(String(2048), nullable=False)
    OrderBy = Column(String(255), nullable=False)

class Employeegps(Base):
    __tablename__ = 'employeegps'

    GPSDate = Column(Date, primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    GPSTime = Column(String(255), primary_key=True, nullable=False)
    Latitude = Column(DECIMAL(18, 7), nullable=False)
    Longitude = Column(DECIMAL(18, 7), nullable=False)
    Accuracy = Column(DECIMAL(18, 7), nullable=False)
    Speed = Column(DECIMAL(18, 7), nullable=False)

class Expansiondefinition(Base):
    __tablename__ = 'expansiondefinition'

    Table = Column(String(50), primary_key=True, nullable=False)
    Field = Column(String(50), primary_key=True, nullable=False)
    OrderNo = Column(Integer, nullable=False)
    Label = Column(String(50), nullable=False)
    IsFilter = Column(Boolean, nullable=False)
    IsSelect = Column(Boolean, nullable=False)
    Type = Column(String(10), nullable=False)
    MinValue = Column(DECIMAL(18, 4), nullable=False)
    MaxValue = Column(DECIMAL(18, 4), nullable=False)
    RangeSelector = Column(String(40), nullable=False)
    IsLookup = Column(Boolean, nullable=False)
    IsRequired = Column(Boolean, nullable=False)
    IsEditable = Column(Boolean, nullable=False)
    RequiredMessage = Column(String(255), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Expansionformtable(Base):
    __tablename__ = 'expansionformtable'

    Form = Column(String(50), primary_key=True, nullable=False)
    Table = Column(String(50), primary_key=True, nullable=False)

class Expansionhook(Base):
    __tablename__ = 'expansionhook'

    Form = Column(String(50), primary_key=True, nullable=False)
    FormParameter = Column(String(50), primary_key=True, nullable=False)
    Enabled = Column(Boolean, nullable=False)
    References = Column(Text, nullable=False)
    SourceCode = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Expansionhookhistory(Base):
    __tablename__ = 'expansionhookhistory'

    Form = Column(String(50), primary_key=True, nullable=False)
    FormParameter = Column(String(50), primary_key=True, nullable=False)
    Version = Column(Integer, primary_key=True, nullable=False)
    Description = Column(String(1024), nullable=False)
    SourceCode = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

class Expansionlookup(Base):
    __tablename__ = 'expansionlookup'

    Table = Column(String(50), primary_key=True, nullable=False)
    Field = Column(String(50), primary_key=True, nullable=False)
    Value = Column(String(50), primary_key=True, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Expansionui(Base):
    __tablename__ = 'expansionui'

    Form = Column(String(50), primary_key=True, nullable=False)
    Table = Column(String(50), primary_key=True, nullable=False)
    Field = Column(String(50), primary_key=True, nullable=False)
    IsDetail = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)