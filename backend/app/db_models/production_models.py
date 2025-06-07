# backend/app/db_models/production_models.py
from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey, DateTime, Time
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import relationship
from .base import Base

class JobOrder(Base):
    __tablename__ = 'joborder'
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    PlannedStartDate = Column(Date, nullable=False)
    PlannedFinishDate = Column(Date, nullable=False)
    ActualStartDate = Column(Date, nullable=False)
    ActualStartTime = Column(Time, nullable=False)
    ActualFinishDate = Column(Date, nullable=False)
    ActualFinishTime = Column(Time, nullable=False)
    RequiredDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), ForeignKey('salesorderh.DocNo'), nullable=False)
    IODocNo = Column(String(20), nullable=False)
    WODocNo = Column(String(15), nullable=False)
    ParentJODocNo = Column(String(15), nullable=False)
    Level = Column(Integer, nullable=False)
    Priority = Column(Integer, nullable=False)
    Location = Column(String(5), ForeignKey('masterlocation.Code'), nullable=False)
    Department = Column(String(10), nullable=False)
    ExcludeCostDistribution = Column(BIT, nullable=False)
    CostDistributionMinMU = Column(Numeric(18, 4), nullable=True)
    Formula = Column(String(40), nullable=False)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), nullable=False)
    Unit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    QtyTarget = Column(Numeric(18, 4), nullable=False)
    QtyOutput = Column(Numeric(18, 4), nullable=False)
    CheckQtyOutput = Column(BIT, nullable=False)
    TotalCost = Column(Numeric(18, 4), nullable=False)
    Status = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(15), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(15), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    location_ref = relationship("MasterLocation")
    material_ref = relationship("MasterMaterial")
    unit_ref = relationship("MasterUnit")
    sales_order_ref = relationship("SalesOrderH")
    job_results = relationship(
        "JobResultH", 
        foreign_keys="[JobResultH.JODocNo]", 
        back_populates="job_order_ref"
    )

class MaterialUsageH(Base):
    __tablename__ = 'materialusageh'
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    DocTime = Column(Time, nullable=False)
    JODocNo = Column(String(15), ForeignKey('joborder.DocNo'), nullable=False)
    Location = Column(String(5), ForeignKey('masterlocation.Code'), nullable=False)
    Machine = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    TotalCost = Column(Numeric(18, 4), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=True)
    PrintedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    Znotransfer = Column(String(15), nullable=True)

    job_order_ref = relationship("JobOrder")
    location_ref = relationship("MasterLocation")
    details = relationship("MaterialUsageD", back_populates="header")

class MaterialUsageD(Base):
    __tablename__ = 'materialusaged'
    DocNo = Column(String(15), ForeignKey('materialusageh.DocNo'), primary_key=True)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), primary_key=True)
    TagNo = Column(String(10), primary_key=True)
    Unit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    Qty = Column(Numeric(18, 4), nullable=False)
    BaseQty = Column(Numeric(18, 4), nullable=False)
    Cost = Column(Numeric(18, 4), nullable=False)
    
    header = relationship("MaterialUsageH", back_populates="details")
    material_ref = relationship("MasterMaterial")
    unit_ref = relationship("MasterUnit")

class JobResultH(Base):
    __tablename__ = 'jobresulth'
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    DocTime = Column(Time, nullable=False)
    JODocNo = Column(String(15), ForeignKey('joborder.DocNo'), nullable=False)
    Location = Column(String(5), ForeignKey('masterlocation.Code'), nullable=False)
    Machine = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=True)
    PrintedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    job_order_ref = relationship(
        "JobOrder", 
        foreign_keys=[JODocNo], 
        back_populates="job_results"
    )
    location_ref = relationship("MasterLocation")
    details = relationship("JobResultD", back_populates="header")

class JobResultD(Base):
    __tablename__ = 'jobresultd'
    DocNo = Column(String(15), ForeignKey('jobresulth.DocNo'), primary_key=True)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), primary_key=True)
    TagNo = Column(String(10), primary_key=True)
    Info = Column(String(255), nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date, nullable=True)
    Unit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    Qty = Column(Numeric(18, 4), nullable=False)
    COGM = Column(Numeric(18, 4), nullable=False)
    Cost = Column(Numeric(18, 4), nullable=False)
    
    header = relationship("JobResultH", back_populates="details")
    material_ref = relationship("MasterMaterial")
    unit_ref = relationship("MasterUnit")