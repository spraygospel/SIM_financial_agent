from sqlalchemy import Column, Integer, String, Text, DECIMAL, Float, Date, DateTime, Boolean, TIMESTAMP, CHAR, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Files(Base):
    __tablename__ = 'files'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Filename = Column(String(255), primary_key=True, nullable=False)
    Size = Column(Integer, nullable=False)
    LastModified = Column(DateTime, nullable=False)
    UploadedDate = Column(DateTime, nullable=False)
    UploadedBy = Column(String(16), nullable=False)

class Formmanagement(Base):
    __tablename__ = 'formmanagement'

    role = Column(String(16), primary_key=True, nullable=False)
    form = Column(String(50), primary_key=True, nullable=False)
    variant = Column(String(50), primary_key=True, nullable=False)
    control = Column(String(50), primary_key=True, nullable=False)
    property = Column(String(50), primary_key=True, nullable=False)
    value = Column(String(50), nullable=False)

class Generaljournald(Base):
    __tablename__ = 'generaljournald'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    AccountNo = Column(String(20), nullable=False)
    Info = Column(String(255), nullable=False)
    Currency = Column(String(3), nullable=False)
    Debet = Column(DECIMAL(18, 4), nullable=False)
    Credit = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    DebetLocal = Column(DECIMAL(18, 4), nullable=False)
    CreditLocal = Column(DECIMAL(18, 4), nullable=False)

class Generaljournalh(Base):
    __tablename__ = 'generaljournalh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TotalDebet = Column(DECIMAL(18, 4), nullable=False)
    TotalCredit = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Goodsissueb(Base):
    __tablename__ = 'goodsissueb'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Goodsissued(Base):
    __tablename__ = 'goodsissued'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    BaseQty = Column(DECIMAL(18, 4), nullable=False)
    QtyReturn = Column(DECIMAL(18, 4), nullable=False)
    QtyNetto = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_goodsissued_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="goodsissued_collection", foreign_keys=[MaterialCode, Unit])

class Goodsissueh(Base):
    __tablename__ = 'goodsissueh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    ShipToCode = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    Zone = Column(String(10), nullable=False)
    PONo = Column(String(50), nullable=False)
    VehicleNo = Column(String(10), nullable=False)
    PackingListNo = Column(String(15), nullable=False)
    ShipmentDocNo = Column(String(15), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    # --- Relationships ---
    packinglistd_collection = relationship("Packinglistd", back_populates="goodsissueh_ref", primaryjoin="Goodsissueh.DocNo == Packinglistd.GIDocNo")

class Goodsreceiptd(Base):
    __tablename__ = 'goodsreceiptd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(1024), nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_goodsreceiptd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="goodsreceiptd_collection", foreign_keys=[MaterialCode, Unit])

class Goodsreceipth(Base):
    __tablename__ = 'goodsreceipth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    PODocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    Zone = Column(String(10), nullable=False)
    SupplierDlvDocNo = Column(String(20), nullable=False)
    VehicleNo = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Hrattendance(Base):
    __tablename__ = 'hrattendance'

    AttendanceDate = Column(Date, primary_key=True, nullable=False)
    EmployeeNo = Column(String(20), primary_key=True, nullable=False)
    WorkingStartTime = Column(DateTime)
    WorkingEndTime = Column(DateTime)
    Break1StartTime = Column(DateTime)
    Break1EndTime = Column(DateTime)
    Break2StartTime = Column(DateTime)
    Break2EndTime = Column(DateTime)
    Shift = Column(String(20), nullable=False)
    WorkingDuration = Column(DECIMAL(18, 4), nullable=False)
    Break1Duration = Column(DECIMAL(18, 4), nullable=False)
    Break2Duration = Column(DECIMAL(18, 4), nullable=False)
    NettoWorkingDuration = Column(DECIMAL(18, 4), nullable=False)
    StartEarlyMinute = Column(DECIMAL(18, 4), nullable=False)
    StartLateMinute = Column(DECIMAL(18, 4), nullable=False)
    EndEarlyMinute = Column(DECIMAL(18, 4), nullable=False)
    EndLateMinute = Column(DECIMAL(18, 4), nullable=False)
    Overtime = Column(DECIMAL(18, 4), nullable=False)
    IsValid = Column(Boolean, nullable=False)
    DocNo = Column(String(15), nullable=False)
    Problem = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

class Hrattendanceoriginal(Base):
    __tablename__ = 'hrattendanceoriginal'

    AttendanceDate = Column(Date, primary_key=True, nullable=False)
    EmployeeNo = Column(String(20), primary_key=True, nullable=False)
    WorkingStartTime = Column(DateTime)
    WorkingEndTime = Column(DateTime)
    Break1StartTime = Column(DateTime)
    Break1EndTime = Column(DateTime)
    Break2StartTime = Column(DateTime)
    Break2EndTime = Column(DateTime)
    Shift = Column(String(20), nullable=False)
    WorkingDuration = Column(DECIMAL(18, 4), nullable=False)
    Break1Duration = Column(DECIMAL(18, 4), nullable=False)
    Break2Duration = Column(DECIMAL(18, 4), nullable=False)
    NettoWorkingDuration = Column(DECIMAL(18, 4), nullable=False)
    StartEarlyMinute = Column(DECIMAL(18, 4), nullable=False)
    StartLateMinute = Column(DECIMAL(18, 4), nullable=False)
    EndEarlyMinute = Column(DECIMAL(18, 4), nullable=False)
    EndLateMinute = Column(DECIMAL(18, 4), nullable=False)
    Overtime = Column(DECIMAL(18, 4), nullable=False)
    IsValid = Column(Boolean, nullable=False)
    DocNo = Column(String(15), nullable=False)
    Problem = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

class Hrattendancerawmachine(Base):
    __tablename__ = 'hrattendancerawmachine'

    AttendanceDate = Column(DateTime, primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    Machine = Column(String(50), nullable=False)
    Direction = Column(String(5), nullable=False)

class Hrchangeshiftd(Base):
    __tablename__ = 'hrchangeshiftd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    NewShift = Column(String(20), nullable=False)

class Hrchangeshifth(Base):
    __tablename__ = 'hrchangeshifth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
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

class Hrgeneratequotad(Base):
    __tablename__ = 'hrgeneratequotad'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    QuotaValue = Column(DECIMAL(18, 4), nullable=False)

class Hrgeneratequotah(Base):
    __tablename__ = 'hrgeneratequotah'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Quota = Column(String(20), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
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

class Hrirregularpaymentd(Base):
    __tablename__ = 'hrirregularpaymentd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    Value = Column(DECIMAL(18, 4), nullable=False)

class Hrirregularpaymenth(Base):
    __tablename__ = 'hrirregularpaymenth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    IsDeduction = Column(Boolean, nullable=False)
    Type = Column(String(20), nullable=False)
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

class Hrloand(Base):
    __tablename__ = 'hrloand'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    PaymentDate = Column(Date, nullable=False)
    PaymentValue = Column(DECIMAL(18, 4), nullable=False)
    IsPaidAutomatic = Column(Boolean, nullable=False)
    IsPaidManual = Column(Boolean, nullable=False)
    Info = Column(String(255), nullable=False)

class Hrloanh(Base):
    __tablename__ = 'hrloanh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    EmployeeNo = Column(String(10), nullable=False)
    LoanValue = Column(DECIMAL(18, 4), nullable=False)
    PaidValue = Column(DECIMAL(18, 4), nullable=False)
    OutstandingValue = Column(DECIMAL(18, 4), nullable=False)
    InstallmentValue = Column(DECIMAL(18, 4), nullable=False)
    RepeatEvery = Column(String(10), nullable=False)
    RepeatValue = Column(Integer, nullable=False)
    StartPaymentDate = Column(Date, nullable=False)
    EndPaymentDate = Column(Date, nullable=False)
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

class Hrovertimed(Base):
    __tablename__ = 'hrovertimed'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    StartTime = Column(String(255), nullable=False)
    EndTime = Column(String(255), nullable=False)
    Duration = Column(DECIMAL(18, 4), nullable=False)

class Hrovertimeh(Base):
    __tablename__ = 'hrovertimeh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Reason = Column(String(50), nullable=False)
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

class Hrpayroll(Base):
    __tablename__ = 'hrpayroll'

    PayrollDate = Column(Date, primary_key=True, nullable=False)
    RootComponent = Column(String(50), primary_key=True, nullable=False)
    EmployeeNo = Column(String(20), primary_key=True, nullable=False)
    Component = Column(String(50), primary_key=True, nullable=False)
    IsFinal = Column(Boolean, primary_key=True, nullable=False)
    Value = Column(DECIMAL(18, 4))
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

class Hrpermissiond(Base):
    __tablename__ = 'hrpermissiond'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    Shift = Column(String(20), nullable=False)
    WorkingStartTime = Column(String(255))
    WorkingEndTime = Column(String(255))
    Break1StartTime = Column(String(255))
    Break1EndTime = Column(String(255))
    Break2StartTime = Column(String(255))
    Break2EndTime = Column(String(255))
    QuotaValue = Column(DECIMAL(18, 4), nullable=False)

class Hrpermissionh(Base):
    __tablename__ = 'hrpermissionh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    PermissionType = Column(String(20), nullable=False)
    Quota = Column(String(20), nullable=False)
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

class Hrquota(Base):
    __tablename__ = 'hrquota'

    StartDate = Column(Date, primary_key=True, nullable=False)
    EndDate = Column(Date, primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    Quota = Column(String(20), primary_key=True, nullable=False)
    StartValue = Column(DECIMAL(18, 4), nullable=False)
    RollOverValue = Column(DECIMAL(18, 4), nullable=False)
    UsageValue = Column(DECIMAL(18, 4), nullable=False)
    EndValue = Column(DECIMAL(18, 4), nullable=False)

class Hrschedule(Base):
    __tablename__ = 'hrschedule'

    ScheduleDate = Column(Date, primary_key=True, nullable=False)
    Workgroup = Column(String(20), primary_key=True, nullable=False)
    Shift = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

class Jobcostdistribution(Base):
    __tablename__ = 'jobcostdistribution'

    Periode = Column(Date, primary_key=True, nullable=False)
    AccountNo = Column(String(20), primary_key=True, nullable=False)
    Department = Column(String(10), primary_key=True, nullable=False)
    MUDocNo = Column(String(15), primary_key=True, nullable=False)
    JODocNo = Column(String(15), primary_key=True, nullable=False)
    Info = Column(String(255), nullable=False)
    BaseValue = Column(DECIMAL(18, 4), nullable=False)
    Percent = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

class Joborder(Base):
    __tablename__ = 'joborder'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    PlannedStartDate = Column(Date, nullable=False)
    PlannedFinishDate = Column(Date, nullable=False)
    ActualStartDate = Column(Date, nullable=False)
    ActualStartTime = Column(String(255), nullable=False)
    ActualFinishDate = Column(Date, nullable=False)
    ActualFinishTime = Column(String(255), nullable=False)
    RequiredDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    IODocNo = Column(String(20), nullable=False)
    WODocNo = Column(String(15), nullable=False)
    ParentJODocNo = Column(String(15), nullable=False)
    Level = Column(Integer, nullable=False)
    Priority = Column(Integer, nullable=False)
    Location = Column(String(5), nullable=False)
    Department = Column(String(10), nullable=False)
    ExcludeCostDistribution = Column(Boolean, nullable=False)
    CostDistributionMinMU = Column(DECIMAL(18, 4))
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Unit = Column(String(5), nullable=False)
    QtyTarget = Column(DECIMAL(18, 4), nullable=False)
    QtyOutput = Column(DECIMAL(18, 4), nullable=False)
    CheckQtyOutput = Column(Boolean, nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    Status = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(15), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(15), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_joborder_masterlocation_0', use_alter=True), ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_joborder_masterunitconversion_1', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="joborder_collection", foreign_keys=[Location])
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="joborder_collection", foreign_keys=[MaterialCode, Unit])

class Jobresultd(Base):
    __tablename__ = 'jobresultd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(255), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    COGM = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_jobresultd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="jobresultd_collection", foreign_keys=[MaterialCode, Unit])

class Jobresultdt(Base):
    __tablename__ = 'jobresultdt'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    StartDate = Column(Date, primary_key=True, nullable=False)
    StartTime = Column(String(255), primary_key=True, nullable=False)
    EndDate = Column(Date, nullable=False)
    EndTime = Column(String(255), nullable=False)
    Duration = Column(DECIMAL(18, 4), nullable=False)
    Reason = Column(String(10), nullable=False)
    Info = Column(String(100), nullable=False)

class Jobresulth(Base):
    __tablename__ = 'jobresulth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    DocTime = Column(String(255), nullable=False)
    JODocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    Machine = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_jobresulth_masterlocation_0', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="jobresulth_collection", foreign_keys=[Location])

class Jobstandardcost(Base):
    __tablename__ = 'jobstandardcost'

    Periode = Column(Date, primary_key=True, nullable=False)
    JODocNo = Column(String(15), primary_key=True, nullable=False)
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    QtyOutput = Column(DECIMAL(18, 4), nullable=False)
    MaterialInput = Column(String(20), primary_key=True, nullable=False)
    QtyInput = Column(DECIMAL(18, 4), nullable=False)
    PriceInput = Column(DECIMAL(18, 4), nullable=False)