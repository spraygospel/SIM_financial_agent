from sqlalchemy import Column, Integer, String, Text, DECIMAL, Float, Date, DateTime, Boolean, TIMESTAMP, CHAR, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'user'

    User = Column(String(16), primary_key=True, nullable=False)
    Name = Column(String(45), nullable=False)
    Password = Column(String(45), nullable=False)
    Role = Column(String(16), nullable=False)
    Language = Column(String(2), nullable=False)
    WhatsAppNo = Column(String(15), nullable=False)
    Email = Column(String(50), nullable=False)

class Userlog(Base):
    __tablename__ = 'userlog'

    LogDate = Column(Date, primary_key=True, nullable=False)
    LogTime = Column(String(255), nullable=False)
    User = Column(String(16), nullable=False)
    Status = Column(String(25), nullable=False)
    IP = Column(String(50), nullable=False)
    LoginDate = Column(Date, nullable=False)

class Wip(Base):
    __tablename__ = 'wip'

    Periode = Column(Date, primary_key=True, nullable=False)
    JODocNo = Column(String(15), primary_key=True, nullable=False)
    StartWIP = Column(DECIMAL(18, 4), nullable=False)
    DirectMaterialCost = Column(DECIMAL(18, 4), nullable=False)
    DirectLaborCost = Column(DECIMAL(18, 4), nullable=False)
    OverheadCost = Column(DECIMAL(18, 4), nullable=False)
    WIPProduced = Column(DECIMAL(18, 4), nullable=False)
    QtyProduced = Column(DECIMAL(18, 4), nullable=False)
    COGM = Column(DECIMAL(18, 4), nullable=False)
    EndWIP = Column(DECIMAL(18, 4), nullable=False)
    Variant = Column(DECIMAL(18, 4), nullable=False)

class Wmtransferind(Base):
    __tablename__ = 'wmtransferind'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Wmtransferinh(Base):
    __tablename__ = 'wmtransferinh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    WMTODocNo = Column(String(15), nullable=False)
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

class Wmtransferoutd(Base):
    __tablename__ = 'wmtransferoutd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Wmtransferouth(Base):
    __tablename__ = 'wmtransferouth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    FromLocation = Column(String(5), nullable=False)
    ToLocation = Column(String(5), nullable=False)
    RequestDocNo = Column(String(15), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Workorderd(Base):
    __tablename__ = 'workorderd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Series = Column(String(3), nullable=False)
    Department = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    StartDate = Column(Date, nullable=False)
    FinishDate = Column(Date, nullable=False)
    JODocNo = Column(String(15), nullable=False)

class Workorderh(Base):
    __tablename__ = 'workorderh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    Template = Column(String(40), nullable=False)
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    CheckQtyOutput = Column(Boolean, nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16), nullable=False)
    ApprovedDate = Column(DateTime)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Zstockopname(Base):
    __tablename__ = 'zstockopname'

    OpnameDate = Column(Date, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Diff = Column(DECIMAL(18, 4), nullable=False)