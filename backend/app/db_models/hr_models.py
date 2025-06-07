# backend/app/db_models/hr_models.py
from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey, DateTime, Time
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import relationship
from .base import Base

class HrChangeShiftH(Base):
    __tablename__ = 'hrchangeshifth'
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(BIT, nullable=False)
    ApprovedBy = Column(String(16), nullable=True)
    ApprovedDate = Column(DateTime, nullable=True)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=True)
    PrintedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    details = relationship("HrChangeShiftD", back_populates="header")

class HrChangeShiftD(Base):
    __tablename__ = 'hrchangeshiftd'
    DocNo = Column(String(15), ForeignKey('hrchangeshifth.DocNo'), primary_key=True)
    EmployeeNo = Column(String(10), ForeignKey('masteremployeeh.EmployeeNo'), primary_key=True)
    NewShift = Column(String(20), nullable=False)
    header = relationship("HrChangeShiftH", back_populates="details")
    employee_ref = relationship("MasterEmployeeH")

class HrOvertimeH(Base):
    __tablename__ = 'hrovertimeh'
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Reason = Column(String(50), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(BIT, nullable=False)
    ApprovedBy = Column(String(16), nullable=True)
    ApprovedDate = Column(DateTime, nullable=True)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=True)
    PrintedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    details = relationship("HrOvertimeD", back_populates="header")

class HrOvertimeD(Base):
    __tablename__ = 'hrovertimed'
    DocNo = Column(String(15), ForeignKey('hrovertimeh.DocNo'), primary_key=True)
    EmployeeNo = Column(String(10), ForeignKey('masteremployeeh.EmployeeNo'), primary_key=True)
    StartTime = Column(Time, nullable=False)
    EndTime = Column(Time, nullable=False)
    Duration = Column(Numeric(18, 4), nullable=False)
    header = relationship("HrOvertimeH", back_populates="details")
    employee_ref = relationship("MasterEmployeeH")

class HrAttendance(Base):
    __tablename__ = 'hrattendance'
    AttendanceDate = Column(Date, primary_key=True)
    EmployeeNo = Column(String(20), ForeignKey('masteremployeeh.EmployeeNo'), primary_key=True)
    WorkingStartTime = Column(DateTime, nullable=True)
    WorkingEndTime = Column(DateTime, nullable=True)
    Break1StartTime = Column(DateTime, nullable=True)
    Break1EndTime = Column(DateTime, nullable=True)
    Break2StartTime = Column(DateTime, nullable=True)
    Break2EndTime = Column(DateTime, nullable=True)
    Shift = Column(String(20), nullable=False)
    WorkingDuration = Column(Numeric(18, 4), nullable=False)
    Break1Duration = Column(Numeric(18, 4), nullable=False)
    Break2Duration = Column(Numeric(18, 4), nullable=False)
    NettoWorkingDuration = Column(Numeric(18, 4), nullable=False)
    StartEarlyMinute = Column(Numeric(18, 4), nullable=False)
    StartLateMinute = Column(Numeric(18, 4), nullable=False)
    EndEarlyMinute = Column(Numeric(18, 4), nullable=False)
    EndLateMinute = Column(Numeric(18, 4), nullable=False)
    Overtime = Column(Numeric(18, 4), nullable=False)
    IsValid = Column(BIT, nullable=False)
    DocNo = Column(String(15), nullable=False)
    Problem = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

    employee_ref = relationship("MasterEmployeeH")

class HrPayroll(Base):
    __tablename__ = 'hrpayroll'
    PayrollDate = Column(Date, primary_key=True)
    RootComponent = Column(String(50), primary_key=True)
    EmployeeNo = Column(String(20), ForeignKey('masteremployeeh.EmployeeNo'), primary_key=True)
    Component = Column(String(50), primary_key=True)
    IsFinal = Column(BIT, primary_key=True)
    Value = Column(Numeric(18, 4), nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)

    employee_ref = relationship("MasterEmployeeH")