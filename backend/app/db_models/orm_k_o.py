from sqlalchemy import Column, Integer, String, Text, DECIMAL, Float, Date, DateTime, Boolean, TIMESTAMP, CHAR, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Masteraccount(Base):
    __tablename__ = 'masteraccount'

    AccountNo = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    Level = Column(Integer, nullable=False)
    AccountGroup = Column(String(5), nullable=False)
    ParentNo = Column(String(20), nullable=False)
    IsJournal = Column(Boolean, nullable=False)
    IsCashier = Column(Boolean, nullable=False)
    Users = Column(String(512), nullable=False)
    Department = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteraccountgroup(Base):
    __tablename__ = 'masteraccountgroup'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterapproval(Base):
    __tablename__ = 'masterapproval'

    Series = Column(String(3), primary_key=True, nullable=False)
    MinValue = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    MaxValue = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    Users = Column(String(2048), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterbank(Base):
    __tablename__ = 'masterbank'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterbin(Base):
    __tablename__ = 'masterbin'

    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    Type = Column(String(15), nullable=False)
    VolumeCapacity = Column(DECIMAL(18, 0), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Masterbomcoproduct(Base):
    __tablename__ = 'masterbomcoproduct'

    Formula = Column(String(40), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    PercentValue = Column(DECIMAL(18, 4), nullable=False)

class Masterbomd(Base):
    __tablename__ = 'masterbomd'

    Formula = Column(String(40), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_masterbomd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="masterbomd_collection", foreign_keys=[MaterialCode, Unit])

class Masterbomh(Base):
    __tablename__ = 'masterbomh'

    Formula = Column(String(40), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    IsAverageCOGM = Column(Boolean, nullable=False)
    CompositionCode = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_masterbomh_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="masterbomh_collection", foreign_keys=[MaterialCode, Unit])

class Masterbudgetd(Base):
    __tablename__ = 'masterbudgetd'

    Code = Column(String(15), primary_key=True, nullable=False)
    Year = Column(Integer, primary_key=True, nullable=False)
    AccountNo = Column(String(20), primary_key=True, nullable=False)
    Budget = Column(DECIMAL(18, 4), nullable=False)

class Masterbudgeth(Base):
    __tablename__ = 'masterbudgeth'

    Code = Column(String(15), primary_key=True, nullable=False)
    Year = Column(Integer, primary_key=True, nullable=False)
    Name = Column(String(100), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterbusinessunit(Base):
    __tablename__ = 'masterbusinessunit'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercashflowd(Base):
    __tablename__ = 'mastercashflowd'

    CashflowGroup = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    AccountNo = Column(String(20), primary_key=True, nullable=False)

class Mastercashflowh(Base):
    __tablename__ = 'mastercashflowh'

    CashflowGroup = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    ItemText = Column(String(100), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercfdumptruck(Base):
    __tablename__ = 'mastercfdumptruck'

    Code = Column(String(10), primary_key=True, nullable=False)
    LicensePlate = Column(String(10), nullable=False)
    Length = Column(DECIMAL(18, 4), nullable=False)
    Width = Column(DECIMAL(18, 4), nullable=False)
    Height = Column(DECIMAL(18, 4), nullable=False)
    Volume = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterchatbotpath(Base):
    __tablename__ = 'masterchatbotpath'

    Path = Column(String(255), primary_key=True, nullable=False)
    Roles = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterchatbotschedule(Base):
    __tablename__ = 'masterchatbotschedule'

    ID = Column(String(50), primary_key=True, nullable=False)
    StateID = Column(String(50), nullable=False)
    Schedule = Column(String(50), nullable=False)
    Enabled = Column(Boolean, nullable=False)
    Multicast = Column(Boolean, nullable=False)
    AddParam = Column(String(255), nullable=False)
    Roles = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterchatbotstate(Base):
    __tablename__ = 'masterchatbotstate'

    ID = Column(String(50), primary_key=True, nullable=False)
    StateType = Column(String(10), nullable=False)
    Description = Column(String(255), nullable=False)
    Param = Column(String(50), nullable=False)
    Accept = Column(String(20), nullable=False)
    Keywords = Column(String(255), nullable=False)
    Answer = Column(String(255), nullable=False)
    Service = Column(String(50), nullable=False)
    Help = Column(String(255), nullable=False)
    AddParam = Column(String(255), nullable=False)
    QueryFunction = Column(Text, nullable=False)
    MessageFunction = Column(Text, nullable=False)
    Roles = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercity(Base):
    __tablename__ = 'mastercity'

    Country = Column(String(5), primary_key=True, nullable=False)
    Province = Column(String(20), primary_key=True, nullable=False)
    City = Column(String(50), primary_key=True, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercollector(Base):
    __tablename__ = 'mastercollector'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    Address = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Phone = Column(String(20), nullable=False)
    Mobile = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercompositiond(Base):
    __tablename__ = 'mastercompositiond'

    Code = Column(String(40), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Percentage = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_mastercompositiond_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="mastercompositiond_collection", foreign_keys=[MaterialCode, Unit])

class Mastercompositionh(Base):
    __tablename__ = 'mastercompositionh'

    Code = Column(String(40), primary_key=True, nullable=False)
    Description = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercostdistribution(Base):
    __tablename__ = 'mastercostdistribution'

    AccountNo = Column(String(20), primary_key=True, nullable=False)
    Department = Column(String(10), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    Percent = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercountry(Base):
    __tablename__ = 'mastercountry'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    mastercustomer_collection = relationship("Mastercustomer", back_populates="mastercountry_ref", primaryjoin="Mastercountry.Code == Mastercustomer.Country")
    mastersupplier_collection = relationship("Mastersupplier", back_populates="mastercountry_ref", primaryjoin="Mastercountry.Code == Mastersupplier.Country")

class Mastercubeh(Base):
    __tablename__ = 'mastercubeh'

    Name = Column(String(50), primary_key=True, nullable=False)
    Description = Column(String(100), nullable=False)
    Query = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercurrency(Base):
    __tablename__ = 'mastercurrency'

    Code = Column(String(3), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    mastercustomer_collection = relationship("Mastercustomer", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Mastercustomer.Currency")
    masterprice_collection = relationship("Masterprice", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Masterprice.Currency")
    mastersupplier_collection = relationship("Mastersupplier", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Mastersupplier.Currency")
    purchasecosth_collection = relationship("Purchasecosth", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Purchasecosth.Currency")
    purchaseinvoiceh_collection = relationship("Purchaseinvoiceh", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Purchaseinvoiceh.Currency")
    purchasereturnh_collection = relationship("Purchasereturnh", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Purchasereturnh.Currency")
    salesinvoiceh_collection = relationship("Salesinvoiceh", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Salesinvoiceh.Currency")
    salesorderh_collection = relationship("Salesorderh", back_populates="mastercurrency_ref", primaryjoin="Mastercurrency.Code == Salesorderh.Currency")

class Mastercustomer(Base):
    __tablename__ = 'mastercustomer'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(120), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Country = Column(String(5), nullable=False)
    Phone = Column(String(50), nullable=False)
    Fax = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)
    Contact = Column(String(40), nullable=False)
    Mobile = Column(String(50), nullable=False)
    WhatsAppSession = Column(String(20), nullable=False)
    WhatsAppNo = Column(String(20), nullable=False)
    TaxNumber = Column(String(21), nullable=False)
    CustomerGroup = Column(String(10), nullable=False)
    PriceListType = Column(String(5), nullable=False)
    SalesArea1 = Column(String(10), nullable=False)
    SalesArea2 = Column(String(10), nullable=False)
    SalesArea3 = Column(String(10), nullable=False)
    TOP = Column(Integer, nullable=False)
    Currency = Column(String(3), nullable=False)
    Limit = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    TransactionType2 = Column(String(20), nullable=False)
    CutPPh = Column(Boolean, nullable=False)
    IsBlacklisted = Column(Boolean, nullable=False)
    IsDeleted = Column(Boolean, nullable=False)
    Latitude = Column(DECIMAL(18, 7), nullable=False)
    Longitude = Column(DECIMAL(18, 7), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    Znowa = Column(String(1))

    __table_args__ = (ForeignKeyConstraint(['Country'], ['mastercountry.Code'], name='fk_mastercustomer_mastercountry_0', use_alter=True), ForeignKeyConstraint(['CustomerGroup'], ['mastercustomergroup.Code'], name='fk_mastercustomer_mastercustomergroup_1', use_alter=True), ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_mastercustomer_mastercurrency_2', use_alter=True), ForeignKeyConstraint(['PriceListType'], ['masterpricelisttype.Code'], name='fk_mastercustomer_masterpricelisttype_3', use_alter=True),)

    # --- Relationships ---
    mastercountry_ref = relationship("Mastercountry", back_populates="mastercustomer_collection", foreign_keys=[Country])
    mastercustomergroup_ref = relationship("Mastercustomergroup", back_populates="mastercustomer_collection", foreign_keys=[CustomerGroup])
    mastercurrency_ref = relationship("Mastercurrency", back_populates="mastercustomer_collection", foreign_keys=[Currency])
    masterpricelisttype_ref = relationship("Masterpricelisttype", back_populates="mastercustomer_collection", foreign_keys=[PriceListType])
    mastercustomerpartner_collection = relationship("Mastercustomerpartner", back_populates="mastercustomer_ref", primaryjoin="Mastercustomer.Code == Mastercustomerpartner.CustomerCode")
    pointofsaleh_collection = relationship("Pointofsaleh", back_populates="mastercustomer_ref", primaryjoin="Mastercustomer.Code == Pointofsaleh.CustomerCode")
    salesinvoiceh_collection_via_CustomerCode = relationship("Salesinvoiceh", back_populates="mastercustomer_ref_via_CustomerCode", primaryjoin="Mastercustomer.Code == Salesinvoiceh.CustomerCode")
    salesinvoiceh_collection_via_TaxToCode = relationship("Salesinvoiceh", back_populates="mastercustomer_ref_via_TaxToCode", primaryjoin="Mastercustomer.Code == Salesinvoiceh.TaxToCode")
    salesreturnh_collection_via_CustomerCode = relationship("Salesreturnh", back_populates="mastercustomer_ref_via_CustomerCode", primaryjoin="Mastercustomer.Code == Salesreturnh.CustomerCode")
    salesreturnh_collection_via_CustomerTaxTo = relationship("Salesreturnh", back_populates="mastercustomer_ref_via_CustomerTaxTo", primaryjoin="Mastercustomer.Code == Salesreturnh.CustomerTaxTo")

class Mastercustomergroup(Base):
    __tablename__ = 'mastercustomergroup'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    mastercustomer_collection = relationship("Mastercustomer", back_populates="mastercustomergroup_ref", primaryjoin="Mastercustomergroup.Code == Mastercustomer.CustomerGroup")

class Mastercustomerpartner(Base):
    __tablename__ = 'mastercustomerpartner'

    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    PartnerFunc = Column(String(10), primary_key=True, nullable=False)
    PartnerCode = Column(String(10), primary_key=True, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['CustomerCode'], ['mastercustomer.Code'], name='fk_mastercustomerpartner_mastercustomer_0', use_alter=True),)

    # --- Relationships ---
    mastercustomer_ref = relationship("Mastercustomer", back_populates="mastercustomerpartner_collection", foreign_keys=[CustomerCode])

class Mastercustomervisitscheduled(Base):
    __tablename__ = 'mastercustomervisitscheduled'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    DivideWeek = Column(Integer, nullable=False)
    RemainderWeek = Column(Integer, nullable=False)
    Sunday = Column(Boolean, nullable=False)
    Monday = Column(Boolean, nullable=False)
    Tuesday = Column(Boolean, nullable=False)
    Wednesday = Column(Boolean, nullable=False)
    Thursday = Column(Boolean, nullable=False)
    Friday = Column(Boolean, nullable=False)
    Saturday = Column(Boolean, nullable=False)

class Mastercustomervisitscheduleh(Base):
    __tablename__ = 'mastercustomervisitscheduleh'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastercustomervisitscheduleo(Base):
    __tablename__ = 'mastercustomervisitscheduleo'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    DayOfWeek = Column(String(10), primary_key=True, nullable=False)
    DivideWeek = Column(Integer, primary_key=True, nullable=False)
    RemainderWeek = Column(Integer, primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    OrderNo = Column(Integer, nullable=False)

class Masterdashboardd(Base):
    __tablename__ = 'masterdashboardd'

    Code = Column(String(20), primary_key=True, nullable=False)
    ItemCode = Column(String(20), primary_key=True, nullable=False)
    Width = Column(Integer, nullable=False)
    Height = Column(Integer, nullable=False)
    Left = Column(Integer, nullable=False)
    Top = Column(Integer, nullable=False)

class Masterdashboardh(Base):
    __tablename__ = 'masterdashboardh'

    Code = Column(String(20), primary_key=True, nullable=False)
    Description = Column(String(100), nullable=False)
    Width = Column(Integer, nullable=False)
    Height = Column(Integer, nullable=False)
    Users = Column(String(512), nullable=False)
    Layout = Column(Text, nullable=False)
    InitializationCode = Column(Text, nullable=False)
    Password = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterdashboarditem(Base):
    __tablename__ = 'masterdashboarditem'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(100), nullable=False)
    Query = Column(Text, nullable=False)
    Sort = Column(String(50), nullable=False)
    LayoutCode = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterdashboarditemp(Base):
    __tablename__ = 'masterdashboarditemp'

    Code = Column(String(20), primary_key=True, nullable=False)
    ParameterName = Column(String(50), primary_key=True, nullable=False)
    ParameterValue = Column(String(100), nullable=False)

class Masterdatatransfer(Base):
    __tablename__ = 'masterdatatransfer'

    Mode = Column(String(10), primary_key=True, nullable=False)
    Server = Column(String(10), primary_key=True, nullable=False)
    Table = Column(String(30), primary_key=True, nullable=False)
    Key = Column(String(30), nullable=False)
    WithDetail = Column(Boolean, nullable=False)
    Condition = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterdepartment(Base):
    __tablename__ = 'masterdepartment'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterdocumentseries(Base):
    __tablename__ = 'masterdocumentseries'

    Document = Column(String(20), primary_key=True, nullable=False)
    Series = Column(String(3), primary_key=True, nullable=False)
    Description = Column(String(255), nullable=False)
    Users = Column(String(2048), nullable=False)
    NeedQC = Column(Boolean, nullable=False)
    NoTaxNo = Column(Boolean, nullable=False)
    AutoTaxNo = Column(Boolean, nullable=False)
    ISO = Column(String(30), nullable=False)
    BusinessUnit = Column(String(20), nullable=False)
    CustomerFilter = Column(String(512), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterdocumentseriesl(Base):
    __tablename__ = 'masterdocumentseriesl'

    Document = Column(String(20), primary_key=True, nullable=False)
    Series = Column(String(3), primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)

class Masterdocumentseriesmt(Base):
    __tablename__ = 'masterdocumentseriesmt'

    Document = Column(String(20), primary_key=True, nullable=False)
    Series = Column(String(3), primary_key=True, nullable=False)
    MaterialType = Column(String(5), primary_key=True, nullable=False)

class Masterdocumentseriestt(Base):
    __tablename__ = 'masterdocumentseriestt'

    Document = Column(String(20), primary_key=True, nullable=False)
    Series = Column(String(3), primary_key=True, nullable=False)
    TransactionType = Column(String(20), primary_key=True, nullable=False)

class Masterdowntimereason(Base):
    __tablename__ = 'masterdowntimereason'

    Code = Column(String(10), primary_key=True, nullable=False)
    Description = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterdriver(Base):
    __tablename__ = 'masterdriver'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    Address = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Phone = Column(String(20), nullable=False)
    Mobile = Column(String(20), nullable=False)
    Password = Column(String(45), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteremployeea(Base):
    __tablename__ = 'masteremployeea'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    AddressType = Column(String(20), primary_key=True, nullable=False)
    Country = Column(String(5), nullable=False)
    Province = Column(String(20), nullable=False)
    City = Column(String(50), nullable=False)
    Address = Column(String(255), nullable=False)
    PostalCode = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteremployeec(Base):
    __tablename__ = 'masteremployeec'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    ContactType = Column(String(20), primary_key=True, nullable=False)
    ContactValue = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteremployeee(Base):
    __tablename__ = 'masteremployeee'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    StartYear = Column(Integer, primary_key=True, nullable=False)
    EndYear = Column(Integer, primary_key=True, nullable=False)
    EducationLevel = Column(String(20), primary_key=True, nullable=False)
    InstitutionName = Column(String(50), primary_key=True, nullable=False)
    Subject = Column(String(50), primary_key=True, nullable=False)
    IsCompleted = Column(Boolean, nullable=False)
    Score = Column(DECIMAL(18, 4), nullable=False)
    Country = Column(String(5), nullable=False)
    Province = Column(String(20), nullable=False)
    City = Column(String(50), nullable=False)
    Info = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteremployeeh(Base):
    __tablename__ = 'masteremployeeh'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    Gender = Column(CHAR(1), nullable=False)
    BirthDate = Column(Date, nullable=False)
    Religion = Column(String(20), nullable=False)
    IsActive = Column(Boolean, nullable=False)
    JoinDate = Column(Date, nullable=False)
    ResignDate = Column(Date)
    ResignReason = Column(String(50), nullable=False)
    Information = Column(String(1024), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteremployeer(Base):
    __tablename__ = 'masteremployeer'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    RelationType = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), primary_key=True, nullable=False)
    Gender = Column(CHAR(1), nullable=False)
    BirthDate = Column(Date)
    Country = Column(String(5), nullable=False)
    Province = Column(String(20), nullable=False)
    City = Column(String(50), nullable=False)
    Address = Column(String(255), nullable=False)
    IDNo = Column(String(50), nullable=False)
    PhoneNo = Column(String(50), nullable=False)
    Info = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masteremployeev(Base):
    __tablename__ = 'masteremployeev'

    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    VariableName = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    StringValue = Column(String(100))
    DecimalValue = Column(DECIMAL(18, 4))
    BoolValue = Column(Boolean)
    DateValue = Column(Date)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterexchangerate(Base):
    __tablename__ = 'masterexchangerate'

    Periode = Column(Date, primary_key=True, nullable=False)
    Currency = Column(String(3), primary_key=True, nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterformshortcut(Base):
    __tablename__ = 'masterformshortcut'

    Form = Column(String(50), primary_key=True, nullable=False)
    Ctrl = Column(Boolean, primary_key=True, nullable=False)
    Alt = Column(Boolean, primary_key=True, nullable=False)
    Key = Column(String(20), primary_key=True, nullable=False)
    Description = Column(String(255), nullable=False)
    Instruction = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterglseriescontent(Base):
    __tablename__ = 'masterglseriescontent'

    GLSeries = Column(String(3), primary_key=True, nullable=False)
    DocType = Column(String(20), primary_key=True, nullable=False)
    DocSeries = Column(String(3), primary_key=True, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Masterhrcomponent(Base):
    __tablename__ = 'masterhrcomponent'

    Code = Column(String(50), primary_key=True, nullable=False)
    Name = Column(String(100), nullable=False)
    RootComponent = Column(String(50), nullable=False)
    IsSaveToDatabase = Column(Boolean, nullable=False)
    ViewRoles = Column(String(1024), nullable=False)
    ProcessRoles = Column(String(1024), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrdynamicvariable(Base):
    __tablename__ = 'masterhrdynamicvariable'

    Name = Column(String(20), primary_key=True, nullable=False)
    Query = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrfilter(Base):
    __tablename__ = 'masterhrfilter'

    VariableName = Column(String(20), primary_key=True, nullable=False)
    FilterName = Column(String(50), primary_key=True, nullable=False)
    Roles = Column(String(1024), nullable=False)
    MenuNames = Column(String(2048), nullable=False)
    VariableValue = Column(String(2048), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrformula(Base):
    __tablename__ = 'masterhrformula'

    Component = Column(String(50), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Condition = Column(String(2048), nullable=False)
    Formula = Column(String(2048))
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrglobalvariable(Base):
    __tablename__ = 'masterhrglobalvariable'

    Name = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    Value = Column(DECIMAL(18, 4))
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrholiday(Base):
    __tablename__ = 'masterhrholiday'

    HolidayDate = Column(Date, primary_key=True, nullable=False)
    Description = Column(String(50), nullable=False)
    Shift = Column(String(20), nullable=False)
    ExcludedWorkgroups = Column(String(2048), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrorganizationalunit(Base):
    __tablename__ = 'masterhrorganizationalunit'

    Type = Column(String(20), primary_key=True, nullable=False)
    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    Level = Column(Integer, nullable=False)
    Parent = Column(String(20), nullable=False)
    IsLeaf = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrperiod(Base):
    __tablename__ = 'masterhrperiod'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrperiodcycle(Base):
    __tablename__ = 'masterhrperiodcycle'

    Period = Column(String(20), primary_key=True, nullable=False)
    Component = Column(String(50), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrpermissiontype(Base):
    __tablename__ = 'masterhrpermissiontype'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    Quota = Column(String(20), nullable=False)
    QuotaValue = Column(DECIMAL(18, 4), nullable=False)
    QuotaValueFormula = Column(String(50), nullable=False)
    IsQuotaValueEditable = Column(Boolean, nullable=False)
    IsMultiDays = Column(Boolean, nullable=False)
    IsSkipHoliday = Column(Boolean, nullable=False)
    IsNoAttendance = Column(Boolean, nullable=False)
    IsPaid = Column(Boolean, nullable=False)
    IsLossTime = Column(Boolean, nullable=False)
    IsFixShift = Column(Boolean, nullable=False)
    IsFixWorkingStartTime = Column(Boolean, nullable=False)
    IsFixWorkingEndTime = Column(Boolean, nullable=False)
    IsFixBreak1StartTime = Column(Boolean, nullable=False)
    IsFixBreak1EndTime = Column(Boolean, nullable=False)
    IsFixBreak2StartTime = Column(Boolean, nullable=False)
    IsFixBreak2EndTime = Column(Boolean, nullable=False)
    IsFixValid = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrquota(Base):
    __tablename__ = 'masterhrquota'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    MaxValue = Column(DECIMAL(18, 4), nullable=False)
    IsAllowNegative = Column(Boolean, nullable=False)
    IsAutomaticRollOver = Column(Boolean, nullable=False)
    IsProportional = Column(Boolean, nullable=False)
    EmployeeCondition = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrshift(Base):
    __tablename__ = 'masterhrshift'

    Code = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    Name = Column(String(50), nullable=False)
    WorkingStartTime = Column(String(255), nullable=False)
    WorkingEndTime = Column(String(255), nullable=False)
    WorkingDuration = Column(DECIMAL(18, 4), nullable=False)
    Break1StartTime = Column(String(255), nullable=False)
    Break1EndTime = Column(String(255), nullable=False)
    Break1Duration = Column(DECIMAL(18, 4), nullable=False)
    Break2StartTime = Column(String(255), nullable=False)
    Break2EndTime = Column(String(255), nullable=False)
    Break2Duration = Column(DECIMAL(18, 4), nullable=False)
    NettoWorkingDuration = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrvariable(Base):
    __tablename__ = 'masterhrvariable'

    Name = Column(String(20), primary_key=True, nullable=False)
    Label = Column(String(50), nullable=False)
    Type = Column(CHAR(10), nullable=False)
    RangeSelector = Column(String(40), nullable=False)
    IsRequired = Column(Boolean, nullable=False)
    ViewRoles = Column(String(1024), nullable=False)
    EditRoles = Column(String(1024), nullable=False)
    IsSystem = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrvariableview(Base):
    __tablename__ = 'masterhrvariableview'

    MenuName = Column(String(50), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    VariableName = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterhrworkgroup(Base):
    __tablename__ = 'masterhrworkgroup'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterinstructionsetd(Base):
    __tablename__ = 'masterinstructionsetd'

    Name = Column(String(50), primary_key=True, nullable=False)
    ColumnName = Column(String(50), primary_key=True, nullable=False)
    OrderNo = Column(Integer, nullable=False)
    Instruction = Column(String(255), nullable=False)
    AutoFlag = Column(String(255), nullable=False)
    AutoNumber = Column(String(255), nullable=False)

class Masterinstructionseth(Base):
    __tablename__ = 'masterinstructionseth'

    Name = Column(String(50), primary_key=True, nullable=False)
    Description = Column(String(255), nullable=False)
    Form = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterlanguage(Base):
    __tablename__ = 'masterlanguage'

    Language = Column(String(2), primary_key=True, nullable=False)
    Sentence = Column(String(255), primary_key=True, nullable=False)
    Translation = Column(String(255), nullable=False)

class Masterlocation(Base):
    __tablename__ = 'masterlocation'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    IsWarehouseManagement = Column(Boolean, nullable=False)
    IsQualityControl = Column(Boolean, nullable=False)
    VolumeCapacity = Column(DECIMAL(18, 0), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(80), nullable=False)
    Country = Column(String(80), nullable=False)
    Latitude = Column(DECIMAL(18, 7), nullable=False)
    Longitude = Column(DECIMAL(18, 7), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    adjustinh_collection = relationship("Adjustinh", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Adjustinh.Location")
    adjustouth_collection = relationship("Adjustouth", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Adjustouth.Location")
    joborder_collection = relationship("Joborder", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Joborder.Location")
    jobresulth_collection = relationship("Jobresulth", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Jobresulth.Location")
    materialusageh_collection = relationship("Materialusageh", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Materialusageh.Location")
    materialusagereturnh_collection = relationship("Materialusagereturnh", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Materialusagereturnh.Location")
    stock_collection = relationship("Stock", back_populates="masterlocation_ref", primaryjoin="Masterlocation.Code == Stock.Location")
    stocktransferh_collection_via_FromLocation = relationship("Stocktransferh", back_populates="masterlocation_ref_via_FromLocation", primaryjoin="Masterlocation.Code == Stocktransferh.FromLocation")
    stocktransferh_collection_via_ToLocation = relationship("Stocktransferh", back_populates="masterlocation_ref_via_ToLocation", primaryjoin="Masterlocation.Code == Stocktransferh.ToLocation")

class Mastermachine(Base):
    __tablename__ = 'mastermachine'

    Code = Column(String(10), primary_key=True, nullable=False)
    Description = Column(String(40), nullable=False)
    Department = Column(String(10), nullable=False)
    CapacityPerHour = Column(DECIMAL(18, 4), nullable=False)
    Unit = Column(String(5), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermasterh(Base):
    __tablename__ = 'mastermasterh'

    MasterTable = Column(String(50), primary_key=True, nullable=False)
    Title = Column(String(50), nullable=False)
    HeaderMaxControl = Column(Integer, nullable=False)
    KeyColumn = Column(String(50), nullable=False)
    KeySize = Column(Integer, nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermaterial(Base):
    __tablename__ = 'mastermaterial'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(80), nullable=False)
    NameInPO = Column(String(80), nullable=False)
    Substitute = Column(String(20), nullable=False)
    SmallestUnit = Column(String(5), nullable=False)
    SoldUnit = Column(String(5), nullable=False)
    SKUUnit = Column(String(5), nullable=False)
    Group1 = Column(String(10), nullable=False)
    Group2 = Column(String(10), nullable=False)
    Group3 = Column(String(10), nullable=False)
    Type = Column(String(5), nullable=False)
    IsBatch = Column(Boolean, nullable=False)
    IsService = Column(Boolean, nullable=False)
    IsAsset = Column(Boolean, nullable=False)
    IsPPh = Column(Boolean, nullable=False)
    HS = Column(String(20), nullable=False)
    Barcode = Column(String(20), nullable=False)
    MinStock = Column(DECIMAL(18, 0), nullable=False)
    MaxStock = Column(DECIMAL(18, 0), nullable=False)
    Currency = Column(String(3), nullable=False)
    DefaultPrice = Column(DECIMAL(18, 4), nullable=False)
    TransactionType1 = Column(String(20), nullable=False)
    TransactionType2 = Column(String(20), nullable=False)
    TransactionType3 = Column(String(20), nullable=False)
    TransactionType4 = Column(String(20), nullable=False)
    TransactionType5 = Column(String(20), nullable=False)
    Info = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    masterunitconversion_collection = relationship("Masterunitconversion", back_populates="mastermaterial_ref", primaryjoin="Mastermaterial.Code == Masterunitconversion.MaterialCode")
    stock_collection = relationship("Stock", back_populates="mastermaterial_ref", primaryjoin="Mastermaterial.Code == Stock.MaterialCode")

class Mastermaterialgroup1(Base):
    __tablename__ = 'mastermaterialgroup1'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    mastermaterialgroup2_collection = relationship("Mastermaterialgroup2", back_populates="mastermaterialgroup1_ref", primaryjoin="Mastermaterialgroup1.Code == Mastermaterialgroup2.Group1")

class Mastermaterialgroup2(Base):
    __tablename__ = 'mastermaterialgroup2'

    Group1 = Column(String(10), primary_key=True, nullable=False)
    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Group1'], ['mastermaterialgroup1.Code'], name='fk_mastermaterialgroup2_mastermaterialgroup1_0', use_alter=True),)

    # --- Relationships ---
    mastermaterialgroup1_ref = relationship("Mastermaterialgroup1", back_populates="mastermaterialgroup2_collection", foreign_keys=[Group1])
    mastermaterialgroup3_collection = relationship("Mastermaterialgroup3", back_populates="mastermaterialgroup2_ref", primaryjoin="Mastermaterialgroup2.Group1 == Mastermaterialgroup3.Group1 and Mastermaterialgroup2.Code == Mastermaterialgroup3.Group2")

class Mastermaterialgroup3(Base):
    __tablename__ = 'mastermaterialgroup3'

    Group1 = Column(String(10), primary_key=True, nullable=False)
    Group2 = Column(String(10), primary_key=True, nullable=False)
    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Group1', 'Group2'], ['mastermaterialgroup2.Group1', 'mastermaterialgroup2.Code'], name='fk_mastermaterialgroup3_mastermaterialgroup2_0', use_alter=True),)

    # --- Relationships ---
    mastermaterialgroup2_ref = relationship("Mastermaterialgroup2", back_populates="mastermaterialgroup3_collection", foreign_keys=[Group1, Group2])

class Mastermaterialpromo(Base):
    __tablename__ = 'mastermaterialpromo'

    Code = Column(String(50), primary_key=True, nullable=False)
    Name = Column(String(255), nullable=False)
    PromoType = Column(String(20), nullable=False)
    Description = Column(String(1024), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    OrderNo = Column(Integer, nullable=False)
    CustomerFilter = Column(String(1024), nullable=False)
    Filename = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermaterials(Base):
    __tablename__ = 'mastermaterials'

    Code = Column(String(20), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    Priority = Column(Integer, nullable=False)

class Mastermaterialtype(Base):
    __tablename__ = 'mastermaterialtype'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    IsWaste = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermobilereportd(Base):
    __tablename__ = 'mastermobilereportd'

    Code = Column(String(20), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Type = Column(String(50), nullable=False)
    Title = Column(String(50), nullable=False)

class Mastermobilereporth(Base):
    __tablename__ = 'mastermobilereporth'

    Code = Column(String(20), primary_key=True, nullable=False)
    Title = Column(String(100), nullable=False)
    ReportGroup = Column(String(50), nullable=False)
    Roles = Column(String(255), nullable=False)
    Query = Column(Text, nullable=False)
    Javascript = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermpmaterialconversion(Base):
    __tablename__ = 'mastermpmaterialconversion'

    SKU = Column(String(20), primary_key=True, nullable=False)
    Variant = Column(String(40), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermpshop(Base):
    __tablename__ = 'mastermpshop'

    ShopId = Column(String(20), primary_key=True, nullable=False)
    ShopName = Column(String(50), nullable=False)
    MarketPlace = Column(String(20), nullable=False)
    ClientId = Column(String(50), nullable=False)
    ClientSecret = Column(String(100), nullable=False)
    AppId = Column(String(50), nullable=False)
    IsDownload = Column(Boolean, nullable=False)
    SOSeries = Column(String(3), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    ShipToCode = Column(String(10), nullable=False)
    TaxToCode = Column(String(10), nullable=False)
    SalesCode = Column(String(10), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastermpstatus(Base):
    __tablename__ = 'mastermpstatus'

    MarketPlace = Column(String(20), primary_key=True, nullable=False)
    StatusCode = Column(String(20), primary_key=True, nullable=False)
    StatusText = Column(String(100), nullable=False)
    InternalStatus = Column(String(20), nullable=False)
    CanCreateSO = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterperiode(Base):
    __tablename__ = 'masterperiode'

    Periode = Column(Date, primary_key=True, nullable=False)
    IsClosed = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterprice(Base):
    __tablename__ = 'masterprice'

    Begda = Column(Date, primary_key=True, nullable=False)
    Endda = Column(Date, nullable=False)
    PriceListType = Column(String(5), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Currency = Column(String(3), primary_key=True, nullable=False)
    Unit = Column(String(5), primary_key=True, nullable=False)
    MinQty = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    MaxQty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    PercentDisc = Column(DECIMAL(18, 4), nullable=False)
    PercentDisc2 = Column(DECIMAL(18, 4), nullable=False)
    PercentDisc3 = Column(DECIMAL(18, 4), nullable=False)
    ValueDisc = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_masterprice_mastercurrency_0', use_alter=True), ForeignKeyConstraint(['PriceListType'], ['masterpricelisttype.Code'], name='fk_masterprice_masterpricelisttype_1', use_alter=True), ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_masterprice_masterunitconversion_2', use_alter=True),)

    # --- Relationships ---
    mastercurrency_ref = relationship("Mastercurrency", back_populates="masterprice_collection", foreign_keys=[Currency])
    masterpricelisttype_ref = relationship("Masterpricelisttype", back_populates="masterprice_collection", foreign_keys=[PriceListType])
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="masterprice_collection", foreign_keys=[MaterialCode, Unit])

class Masterpricelisttype(Base):
    __tablename__ = 'masterpricelisttype'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    mastercustomer_collection = relationship("Mastercustomer", back_populates="masterpricelisttype_ref", primaryjoin="Masterpricelisttype.Code == Mastercustomer.PriceListType")
    masterprice_collection = relationship("Masterprice", back_populates="masterpricelisttype_ref", primaryjoin="Masterpricelisttype.Code == Masterprice.PriceListType")

class Masterpromoc(Base):
    __tablename__ = 'masterpromoc'

    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Field = Column(String(50), nullable=False)
    Value = Column(String(50), nullable=False)

class Masterpromofg(Base):
    __tablename__ = 'masterpromofg'

    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Field1 = Column(String(50), nullable=False)
    Value1 = Column(String(50), nullable=False)
    Field2 = Column(String(50), nullable=False)
    Value2 = Column(String(50), nullable=False)
    Field3 = Column(String(50), nullable=False)
    Value3 = Column(String(50), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Masterpromoh(Base):
    __tablename__ = 'masterpromoh'

    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    StartTime = Column(String(255), nullable=False)
    EndTime = Column(String(255), nullable=False)
    DocumentSeries = Column(String(255), nullable=False)
    ExclusiveGroup = Column(String(20), nullable=False)
    IsSuggested = Column(Boolean, nullable=False)
    Currency = Column(String(3), nullable=False)
    MinTotalGross = Column(DECIMAL(18, 4), nullable=False)
    ExcludeRequirement = Column(Boolean, nullable=False)
    MustMultiple = Column(Boolean, nullable=False)
    CustomerCondition = Column(String(50), nullable=False)
    RequirementCondition = Column(String(50), nullable=False)
    MaxMultiple = Column(Integer, nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterpromor(Base):
    __tablename__ = 'masterpromor'

    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Field1 = Column(String(50), nullable=False)
    Value1 = Column(String(50), nullable=False)
    Field2 = Column(String(50), nullable=False)
    Value2 = Column(String(50), nullable=False)
    Field3 = Column(String(50), nullable=False)
    Value3 = Column(String(50), nullable=False)
    Unit = Column(String(5), nullable=False)
    MinQty = Column(DECIMAL(18, 4), nullable=False)
    MinNetto = Column(DECIMAL(18, 4), nullable=False)

class Masterprovince(Base):
    __tablename__ = 'masterprovince'

    Country = Column(String(5), primary_key=True, nullable=False)
    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterrangeselector(Base):
    __tablename__ = 'masterrangeselector'

    Name = Column(String(50), primary_key=True, nullable=False)
    Description = Column(String(50), nullable=False)
    Condition = Column(String(1024), nullable=False)
    DialogTitle = Column(String(50), nullable=False)
    FieldName = Column(String(50), nullable=False)
    LabelField = Column(String(50), nullable=False)
    FilterFields = Column(String(1024), nullable=False)
    SelectFields = Column(String(1024), nullable=False)
    GridFields = Column(String(1024), nullable=False)
    OrderBy = Column(String(1024), nullable=False)
    SimpleMode = Column(Boolean, nullable=False)
    SqlQuery = Column(String(1024), nullable=False)
    TableName = Column(String(1024), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterrebatec(Base):
    __tablename__ = 'masterrebatec'

    Code = Column(String(10), primary_key=True, nullable=False)
    ValidFrom = Column(Date, primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Condition = Column(String(2014), nullable=False)
    RebatePercent = Column(DECIMAL(18, 4), nullable=False)

class Masterrebateh(Base):
    __tablename__ = 'masterrebateh'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    ValidFrom = Column(Date, primary_key=True, nullable=False)
    ValidTo = Column(Date, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Masterrebates(Base):
    __tablename__ = 'masterrebates'

    Code = Column(String(10), primary_key=True, nullable=False)
    ValidFrom = Column(Date, primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)

class Masterreminder(Base):
    __tablename__ = 'masterreminder'

    Name = Column(String(50), primary_key=True, nullable=False)
    Description = Column(String(100), nullable=False)
    Query = Column(Text, nullable=False)
    Users = Column(String(512), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterreportd(Base):
    __tablename__ = 'masterreportd'

    Name = Column(String(50), primary_key=True, nullable=False)
    Variant = Column(String(50), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    RangeSelector = Column(String(40), nullable=False)
    Field = Column(String(255), nullable=False)

class Masterreporth(Base):
    __tablename__ = 'masterreporth'

    Name = Column(String(50), primary_key=True, nullable=False)
    Variant = Column(String(50), primary_key=True, nullable=False)
    Description = Column(String(100), nullable=False)
    Enabled = Column(Boolean, nullable=False)
    Query = Column(Text, nullable=False)
    OrderQuery = Column(String(512), nullable=False)
    ReportPassword = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterreportscheduleh(Base):
    __tablename__ = 'masterreportscheduleh'

    Name = Column(String(50), primary_key=True, nullable=False)
    IsEnabled = Column(Boolean, nullable=False)
    EmailTo = Column(String(512), nullable=False)
    EmailCC = Column(String(512), nullable=False)
    EmailBCC = Column(String(512), nullable=False)
    Subject = Column(String(255), nullable=False)
    Body = Column(Text, nullable=False)
    Api = Column(String(255), nullable=False)
    Parameters = Column(Text, nullable=False)
    FilterText = Column(String(512), nullable=False)
    Filename = Column(String(255), nullable=False)
    User = Column(String(16), nullable=False)
    Password = Column(String(50), nullable=False)
    Status = Column(String(20), nullable=False)
    NextRun = Column(DateTime)
    LastRun = Column(DateTime)
    LastError = Column(String(512), nullable=False)
    VariableQuery = Column(Text, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterreportschedulet(Base):
    __tablename__ = 'masterreportschedulet'

    Name = Column(String(50), primary_key=True, nullable=False)
    Repeat = Column(String(10), primary_key=True, nullable=False)
    Day = Column(String(10), primary_key=True, nullable=False)
    Date = Column(Integer, primary_key=True, nullable=False)
    Time = Column(String(255), primary_key=True, nullable=False)

class Masterroute(Base):
    __tablename__ = 'masterroute'

    Code = Column(String(10), primary_key=True, nullable=False)
    From = Column(String(5), nullable=False)
    Destination = Column(String(5), nullable=False)
    Distance = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastersales(Base):
    __tablename__ = 'mastersales'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    Address = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Phone = Column(String(20), nullable=False)
    Mobile = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    pointofsaleh_collection = relationship("Pointofsaleh", back_populates="mastersales_ref", primaryjoin="Mastersales.Code == Pointofsaleh.SalesCode")
    salesinvoiceh_collection = relationship("Salesinvoiceh", back_populates="mastersales_ref", primaryjoin="Mastersales.Code == Salesinvoiceh.SalesCode")

class Mastersalesarea1(Base):
    __tablename__ = 'mastersalesarea1'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    mastersalesarea2_collection = relationship("Mastersalesarea2", back_populates="mastersalesarea1_ref", primaryjoin="Mastersalesarea1.Code == Mastersalesarea2.Area1")

class Mastersalesarea2(Base):
    __tablename__ = 'mastersalesarea2'

    Area1 = Column(String(10), primary_key=True, nullable=False)
    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Area1'], ['mastersalesarea1.Code'], name='fk_mastersalesarea2_mastersalesarea1_0', use_alter=True),)

    # --- Relationships ---
    mastersalesarea1_ref = relationship("Mastersalesarea1", back_populates="mastersalesarea2_collection", foreign_keys=[Area1])
    mastersalesarea3_collection = relationship("Mastersalesarea3", back_populates="mastersalesarea2_ref", primaryjoin="Mastersalesarea2.Area1 == Mastersalesarea3.Area1 and Mastersalesarea2.Code == Mastersalesarea3.Area2")

class Mastersalesarea3(Base):
    __tablename__ = 'mastersalesarea3'

    Area1 = Column(String(10), primary_key=True, nullable=False)
    Area2 = Column(String(10), primary_key=True, nullable=False)
    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Area1', 'Area2'], ['mastersalesarea2.Area1', 'mastersalesarea2.Code'], name='fk_mastersalesarea3_mastersalesarea2_0', use_alter=True),)

    # --- Relationships ---
    mastersalesarea2_ref = relationship("Mastersalesarea2", back_populates="mastersalesarea3_collection", foreign_keys=[Area1, Area2])

class Masterserver(Base):
    __tablename__ = 'masterserver'

    Name = Column(String(10), primary_key=True, nullable=False)
    Address = Column(String(50), nullable=False)
    Port = Column(Integer, nullable=False)
    Database = Column(String(20), nullable=False)
    User = Column(String(20), nullable=False)
    Password = Column(String(20), nullable=False)
    ODBCConnectionString = Column(String(512), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastersetting(Base):
    __tablename__ = 'mastersetting'

    Name = Column(String(50), primary_key=True, nullable=False)
    Value = Column(String(512), nullable=False)

class Mastersmltarget(Base):
    __tablename__ = 'mastersmltarget'

    Periode = Column(Date, primary_key=True, nullable=False)
    TargetSalesInvoice = Column(DECIMAL(18, 4), nullable=False)
    TargetPOS = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Mastersupplier(Base):
    __tablename__ = 'mastersupplier'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(120), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Country = Column(String(5), nullable=False)
    Phone = Column(String(50), nullable=False)
    Fax = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)
    Contact = Column(String(40), nullable=False)
    Mobile = Column(String(50), nullable=False)
    TaxNumber = Column(String(21), nullable=False)
    TOP = Column(Integer, nullable=False)
    Currency = Column(String(3), nullable=False)
    Limit = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    TransactionType2 = Column(String(20), nullable=False)
    CutPPh = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Country'], ['mastercountry.Code'], name='fk_mastersupplier_mastercountry_0', use_alter=True), ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_mastersupplier_mastercurrency_1', use_alter=True),)

    # --- Relationships ---
    mastercountry_ref = relationship("Mastercountry", back_populates="mastersupplier_collection", foreign_keys=[Country])
    mastercurrency_ref = relationship("Mastercurrency", back_populates="mastersupplier_collection", foreign_keys=[Currency])
    mastersupplierpartner_collection = relationship("Mastersupplierpartner", back_populates="mastersupplier_ref", primaryjoin="Mastersupplier.Code == Mastersupplierpartner.SupplierCode")
    purchasecosth_collection = relationship("Purchasecosth", back_populates="mastersupplier_ref", primaryjoin="Mastersupplier.Code == Purchasecosth.SupplierCode")
    purchaseinvoiceh_collection_via_SupplierCode = relationship("Purchaseinvoiceh", back_populates="mastersupplier_ref_via_SupplierCode", primaryjoin="Mastersupplier.Code == Purchaseinvoiceh.SupplierCode")
    purchaseinvoiceh_collection_via_SupplierTaxTo = relationship("Purchaseinvoiceh", back_populates="mastersupplier_ref_via_SupplierTaxTo", primaryjoin="Mastersupplier.Code == Purchaseinvoiceh.SupplierTaxTo")
    purchasereturnh_collection_via_SupplierCode = relationship("Purchasereturnh", back_populates="mastersupplier_ref_via_SupplierCode", primaryjoin="Mastersupplier.Code == Purchasereturnh.SupplierCode")
    purchasereturnh_collection_via_SupplierTaxTo = relationship("Purchasereturnh", back_populates="mastersupplier_ref_via_SupplierTaxTo", primaryjoin="Mastersupplier.Code == Purchasereturnh.SupplierTaxTo")

class Mastersupplierpartner(Base):
    __tablename__ = 'mastersupplierpartner'

    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    PartnerFunc = Column(String(10), primary_key=True, nullable=False)
    PartnerCode = Column(String(10), primary_key=True, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['SupplierCode'], ['mastersupplier.Code'], name='fk_mastersupplierpartner_mastersupplier_0', use_alter=True),)

    # --- Relationships ---
    mastersupplier_ref = relationship("Mastersupplier", back_populates="mastersupplierpartner_collection", foreign_keys=[SupplierCode])

class Mastersurveya(Base):
    __tablename__ = 'mastersurveya'

    Code = Column(String(20), primary_key=True, nullable=False)
    QuestionNo = Column(Integer, primary_key=True, nullable=False)
    AnswerNo = Column(Integer, primary_key=True, nullable=False)
    Answer = Column(String(50), nullable=False)
    IsAllowFreeText = Column(Boolean, nullable=False)
    Score = Column(Integer, nullable=False)
    NextQuestion = Column(Integer)

class Mastersurveyh(Base):
    __tablename__ = 'mastersurveyh'

    Code = Column(String(20), primary_key=True, nullable=False)
    Name = Column(String(80), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastersurveyq(Base):
    __tablename__ = 'mastersurveyq'

    Code = Column(String(20), primary_key=True, nullable=False)
    QuestionNo = Column(Integer, primary_key=True, nullable=False)
    Question = Column(String(2048), nullable=False)
    ShortQuestion = Column(String(50), nullable=False)
    Option = Column(String(10), nullable=False)

class Mastertransactionh(Base):
    __tablename__ = 'mastertransactionh'

    Document = Column(String(20), primary_key=True, nullable=False)
    Title = Column(String(50), nullable=False)
    HeaderTable = Column(String(50), nullable=False)
    HeaderMaxControl = Column(Integer, nullable=False)
    SeriesRangeSelector = Column(String(40), nullable=False)
    DocNoRangeSelector = Column(String(40), nullable=False)
    DetailTable1 = Column(String(50), nullable=False)
    DetailCaption1 = Column(String(50), nullable=False)
    DetailTable2 = Column(String(50), nullable=False)
    DetailCaption2 = Column(String(50), nullable=False)
    DetailTable3 = Column(String(50), nullable=False)
    DetailCaption3 = Column(String(50), nullable=False)
    IsApprovable = Column(Boolean, nullable=False)
    ApprovableValueColumn = Column(String(50), nullable=False)
    IsPrintable = Column(Boolean, nullable=False)
    ResetPrintCounterStatus = Column(String(20), nullable=False)
    PrintQuery = Column(Text, nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastertransactiontype(Base):
    __tablename__ = 'mastertransactiontype'

    Type = Column(String(20), primary_key=True, nullable=False)
    Description = Column(String(40), nullable=False)
    AccountNo = Column(String(20), nullable=False)
    Purpose = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastertransportarea(Base):
    __tablename__ = 'mastertransportarea'

    City = Column(String(20), primary_key=True, nullable=False)
    Address = Column(String(80), primary_key=True, nullable=False)
    PostalCode = Column(String(10), nullable=False)
    Area = Column(String(30), nullable=False)
    SubArea = Column(String(30), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastertransportpackagetype(Base):
    __tablename__ = 'mastertransportpackagetype'

    Code = Column(String(10), primary_key=True, nullable=False)
    Description = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastertransportprice(Base):
    __tablename__ = 'mastertransportprice'

    Begda = Column(Date, primary_key=True, nullable=False)
    Endda = Column(Date, primary_key=True, nullable=False)
    PackageType = Column(String(10), primary_key=True, nullable=False)
    ServiceType = Column(String(10), primary_key=True, nullable=False)
    Route = Column(String(10), primary_key=True, nullable=False)
    VehicleType = Column(String(10), primary_key=True, nullable=False)
    PriceListType = Column(String(5), nullable=False)
    PriceList = Column(DECIMAL(18, 4), nullable=False)
    PricePerDay = Column(DECIMAL(18, 4), nullable=False)
    MinTonage = Column(DECIMAL(18, 4), nullable=False)
    MinTonageCharge = Column(DECIMAL(18, 4), nullable=False)
    PricePerKG = Column(DECIMAL(18, 4), nullable=False)
    MinVolume = Column(DECIMAL(18, 4), nullable=False)
    MinVolumeCharge = Column(DECIMAL(18, 4), nullable=False)
    PricePerM3 = Column(DECIMAL(18, 4), nullable=False)
    MaxLength = Column(DECIMAL(18, 4), nullable=False)
    MaxLengthCharge = Column(DECIMAL(18, 4), nullable=False)
    Coefficient = Column(DECIMAL(18, 4), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastertransportservicetype(Base):
    __tablename__ = 'mastertransportservicetype'

    Code = Column(String(10), primary_key=True, nullable=False)
    Description = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterunit(Base):
    __tablename__ = 'masterunit'

    Code = Column(String(5), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    masterunitconversion_collection = relationship("Masterunitconversion", back_populates="masterunit_ref", primaryjoin="Masterunit.Code == Masterunitconversion.Unit")

class Masterunitconversion(Base):
    __tablename__ = 'masterunitconversion'

    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Unit = Column(String(5), primary_key=True, nullable=False)
    Content = Column(DECIMAL(18, 4), nullable=False)
    Weight = Column(DECIMAL(18, 4), nullable=False)
    Volume = Column(DECIMAL(18, 4), nullable=False)
    IsInactive = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode'], ['mastermaterial.Code'], name='fk_masterunitconversion_mastermaterial_0', use_alter=True), ForeignKeyConstraint(['Unit'], ['masterunit.Code'], name='fk_masterunitconversion_masterunit_1', use_alter=True),)

    # --- Relationships ---
    adjustind_collection = relationship("Adjustind", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Adjustind.MaterialCode and Masterunitconversion.Unit == Adjustind.Unit")
    adjustoutd_collection = relationship("Adjustoutd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Adjustoutd.MaterialCode and Masterunitconversion.Unit == Adjustoutd.Unit")
    goodsissued_collection = relationship("Goodsissued", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Goodsissued.MaterialCode and Masterunitconversion.Unit == Goodsissued.Unit")
    goodsreceiptd_collection = relationship("Goodsreceiptd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Goodsreceiptd.MaterialCode and Masterunitconversion.Unit == Goodsreceiptd.Unit")
    joborder_collection = relationship("Joborder", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Joborder.MaterialCode and Masterunitconversion.Unit == Joborder.Unit")
    jobresultd_collection = relationship("Jobresultd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Jobresultd.MaterialCode and Masterunitconversion.Unit == Jobresultd.Unit")
    masterbomd_collection = relationship("Masterbomd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Masterbomd.MaterialCode and Masterunitconversion.Unit == Masterbomd.Unit")
    masterbomh_collection = relationship("Masterbomh", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Masterbomh.MaterialCode and Masterunitconversion.Unit == Masterbomh.Unit")
    mastercompositiond_collection = relationship("Mastercompositiond", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Mastercompositiond.MaterialCode and Masterunitconversion.Unit == Mastercompositiond.Unit")
    masterprice_collection = relationship("Masterprice", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Masterprice.MaterialCode and Masterunitconversion.Unit == Masterprice.Unit")
    mastermaterial_ref = relationship("Mastermaterial", back_populates="masterunitconversion_collection", foreign_keys=[MaterialCode])
    masterunit_ref = relationship("Masterunit", back_populates="masterunitconversion_collection", foreign_keys=[Unit])
    materialusaged_collection = relationship("Materialusaged", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Materialusaged.MaterialCode and Masterunitconversion.Unit == Materialusaged.Unit")
    materialusagereturnd_collection = relationship("Materialusagereturnd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Materialusagereturnd.MaterialCode and Masterunitconversion.Unit == Materialusagereturnd.Unit")
    pointofsaled_collection = relationship("Pointofsaled", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Pointofsaled.MaterialCode and Masterunitconversion.Unit == Pointofsaled.Unit")
    purchaseinvoiced_collection = relationship("Purchaseinvoiced", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Purchaseinvoiced.MaterialCode and Masterunitconversion.Unit == Purchaseinvoiced.Unit")
    purchaseorderd_collection = relationship("Purchaseorderd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Purchaseorderd.MaterialCode and Masterunitconversion.Unit == Purchaseorderd.Unit")
    purchasereturnd_collection = relationship("Purchasereturnd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Purchasereturnd.MaterialCode and Masterunitconversion.Unit == Purchasereturnd.Unit")
    salesinvoiced_collection = relationship("Salesinvoiced", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Salesinvoiced.MaterialCode and Masterunitconversion.Unit == Salesinvoiced.Unit")
    salesorderd_collection = relationship("Salesorderd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Salesorderd.MaterialCode and Masterunitconversion.Unit == Salesorderd.Unit")
    salesreturnd_collection = relationship("Salesreturnd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Salesreturnd.MaterialCode and Masterunitconversion.Unit == Salesreturnd.Unit")
    stocktransferd_collection = relationship("Stocktransferd", back_populates="masterunitconversion_ref", primaryjoin="Masterunitconversion.MaterialCode == Stocktransferd.MaterialCode and Masterunitconversion.Unit == Stocktransferd.Unit")

class Mastervehicle(Base):
    __tablename__ = 'mastervehicle'

    Code = Column(String(10), primary_key=True, nullable=False)
    LicensePlate = Column(String(10), nullable=False)
    VehicleType = Column(String(10), nullable=False)
    Tonage = Column(DECIMAL(18, 4), nullable=False)
    Volume = Column(DECIMAL(18, 4), nullable=False)
    DefaultDriver = Column(String(10), nullable=False)
    Route = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Mastervehicletype(Base):
    __tablename__ = 'mastervehicletype'

    Code = Column(String(10), primary_key=True, nullable=False)
    Description = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterwmequipment(Base):
    __tablename__ = 'masterwmequipment'

    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    VolumeCapacity = Column(DECIMAL(18, 0), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Masterwmroute(Base):
    __tablename__ = 'masterwmroute'

    Location = Column(String(5), primary_key=True, nullable=False)
    Group1 = Column(String(10), primary_key=True, nullable=False)
    Group2 = Column(String(10), primary_key=True, nullable=False)
    Group3 = Column(String(10), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    PickingPriority = Column(Integer, nullable=False)
    PutawayPriority = Column(Integer, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Masterworkordertemplated(Base):
    __tablename__ = 'masterworkordertemplated'

    Code = Column(String(40), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Series = Column(String(3), nullable=False)
    Department = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)

class Masterworkordertemplateh(Base):
    __tablename__ = 'masterworkordertemplateh'

    Code = Column(String(40), primary_key=True, nullable=False)
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    CheckQtyOutput = Column(Boolean, nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Masterzone(Base):
    __tablename__ = 'masterzone'

    Location = Column(String(5), primary_key=True, nullable=False)
    Code = Column(String(10), primary_key=True, nullable=False)
    Name = Column(String(40), nullable=False)
    Type = Column(String(15), nullable=False)
    VolumeCapacity = Column(DECIMAL(18, 0), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Materialusaged(Base):
    __tablename__ = 'materialusaged'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    BaseQty = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_materialusaged_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="materialusaged_collection", foreign_keys=[MaterialCode, Unit])

class Materialusagegeneratorb(Base):
    __tablename__ = 'materialusagegeneratorb'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Materialusagegeneratorc(Base):
    __tablename__ = 'materialusagegeneratorc'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    JRDocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Materialusagegeneratord(Base):
    __tablename__ = 'materialusagegeneratord'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    JRDocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocTime = Column(String(255), nullable=False)
    Information = Column(String(255), nullable=False)
    MUDocNo = Column(String(15), nullable=False)

class Materialusagegeneratordt(Base):
    __tablename__ = 'materialusagegeneratordt'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    JRDocNo = Column(String(15), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    StartTime = Column(String(255), primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    EndTime = Column(String(255), nullable=False)
    Duration = Column(DECIMAL(18, 4), nullable=False)
    Reason = Column(String(10), nullable=False)
    Info = Column(String(100), nullable=False)

class Materialusagegeneratorh(Base):
    __tablename__ = 'materialusagegeneratorh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16), nullable=False)
    ApprovedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Materialusagegeneratorm(Base):
    __tablename__ = 'materialusagegeneratorm'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Materialusageh(Base):
    __tablename__ = 'materialusageh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    DocTime = Column(String(255), nullable=False)
    JODocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    Machine = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    Znotransfer = Column(String(15))

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_materialusageh_masterlocation_0', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="materialusageh_collection", foreign_keys=[Location])

class Materialusagereturnd(Base):
    __tablename__ = 'materialusagereturnd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_materialusagereturnd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="materialusagereturnd_collection", foreign_keys=[MaterialCode, Unit])

class Materialusagereturnh(Base):
    __tablename__ = 'materialusagereturnh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    MUDocNo = Column(String(15), nullable=False)
    JODocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_materialusagereturnh_masterlocation_0', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="materialusagereturnh_collection", foreign_keys=[Location])

class Menu(Base):
    __tablename__ = 'menu'

    Role = Column(String(16), primary_key=True, nullable=False)
    Menu = Column(String(50), primary_key=True, nullable=False)
    SubMenu = Column(String(50), primary_key=True, nullable=False)

class Menulist(Base):
    __tablename__ = 'menulist'

    Menu = Column(String(50), primary_key=True, nullable=False)
    SubMenu = Column(String(50), primary_key=True, nullable=False)
    Filename = Column(String(50), nullable=False)
    FormName = Column(String(50), nullable=False)
    Parameters = Column(String(50))

class Movingaverageprice(Base):
    __tablename__ = 'movingaverageprice'

    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    DocDate = Column(Date, primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    DocNo = Column(String(15), nullable=False)
    PrevValue = Column(DECIMAL(18, 4), nullable=False)
    PrevQty = Column(DECIMAL(18, 4), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    DocQty = Column(DECIMAL(18, 4), nullable=False)
    TotalValue = Column(DECIMAL(18, 4), nullable=False)
    TotalQty = Column(DECIMAL(18, 4), nullable=False)
    AveragePrice = Column(DECIMAL(18, 4), nullable=False)

class Mporderd(Base):
    __tablename__ = 'mporderd'

    ShopId = Column(String(20), primary_key=True, nullable=False)
    OrderId = Column(String(40), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    ItemId = Column(String(40), nullable=False)
    Variant = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Name = Column(String(255), nullable=False)
    Info = Column(String(1024), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    TotalPrice = Column(DECIMAL(18, 4), nullable=False)
    TotalWeight = Column(DECIMAL(18, 4), nullable=False)

class Mporderh(Base):
    __tablename__ = 'mporderh'

    ShopId = Column(String(20), primary_key=True, nullable=False)
    OrderId = Column(String(40), primary_key=True, nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    ReferenceNo = Column(String(50), nullable=False)
    BuyerId = Column(String(50), nullable=False)
    PaymentId = Column(String(20), nullable=False)
    PaymentDate = Column(DateTime)
    RecipientName = Column(String(50), nullable=False)
    RecipientPhone = Column(String(50), nullable=False)
    RecipientAddress = Column(String(255), nullable=False)
    RecipientDistrict = Column(String(50), nullable=False)
    RecipientCity = Column(String(50), nullable=False)
    RecipientProvince = Column(String(50), nullable=False)
    RecipientCountry = Column(String(50), nullable=False)
    RecipientPostalCode = Column(String(50), nullable=False)
    RecipientGeo = Column(String(50), nullable=False)
    LogisticsShippingAgency = Column(String(50), nullable=False)
    LogisticsServiceType = Column(String(50), nullable=False)
    LogisticsAWB = Column(String(50), nullable=False)
    TotalProductPrice = Column(DECIMAL(18, 4), nullable=False)
    ShippingCost = Column(DECIMAL(18, 4), nullable=False)
    InsuranceCost = Column(DECIMAL(18, 4), nullable=False)
    TotalAmount = Column(DECIMAL(18, 4), nullable=False)
    OrderStatus = Column(String(20), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    DownloadedDate = Column(DateTime, nullable=False)
    UpdatedDate = Column(DateTime, nullable=False)

class Opendocument(Base):
    __tablename__ = 'opendocument'

    DocNo = Column(String(20), primary_key=True, nullable=False)
    User = Column(String(16), nullable=False)