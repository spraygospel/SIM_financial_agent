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