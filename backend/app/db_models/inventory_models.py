# backend/app/db_models/inventory_models.py
from sqlalchemy import Column, String, Date, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import relationship
from .base import Base

class Stock(Base):
    __tablename__ = 'stock'
    TagNo = Column(String(10), primary_key=True)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), primary_key=True)
    DocNo = Column(String(15), primary_key=True)
    DocDate = Column(Date, primary_key=True)
    Location = Column(String(5), ForeignKey('masterlocation.Code'), primary_key=True)
    Zone = Column(String(10), primary_key=True)
    Bin = Column(String(10), primary_key=True)
    Number = Column(Integer, primary_key=True, default=0)
    Qty = Column(Numeric(18, 4), nullable=False)
    Price = Column(Numeric(18, 4), nullable=False)
    material_ref = relationship("MasterMaterial")
    location_ref = relationship("MasterLocation")

class StockBalance(Base):
    __tablename__ = 'stockbalance'
    Periode = Column(Date, primary_key=True)
    TagNo = Column(String(10), primary_key=True)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), primary_key=True)
    Location = Column(String(5), ForeignKey('masterlocation.Code'), primary_key=True)
    Zone = Column(String(10), primary_key=True)
    Bin = Column(String(10), primary_key=True)
    Price = Column(Numeric(18, 4), nullable=False)
    QtyStart = Column(Numeric(18, 4), nullable=False)
    QtyIn = Column(Numeric(18, 4), nullable=False)
    QtyOut = Column(Numeric(18, 4), nullable=False)
    QtyEnd = Column(Numeric(18, 4), nullable=False)
    QtyBook = Column(Numeric(18, 4), nullable=False)
    material_ref = relationship("MasterMaterial")
    location_ref = relationship("MasterLocation")

class GoodsIssueD(Base):
    __tablename__ = 'goodsissued'
    DocNo = Column(String(15), ForeignKey('goodsissueh.DocNo'), primary_key=True)
    Number = Column(Integer, primary_key=True)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True)
    Unit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    Qty = Column(Numeric(18, 4), nullable=False)
    BaseQty = Column(Numeric(18, 4), nullable=False)
    QtyReturn = Column(Numeric(18, 4), nullable=False)
    QtyNetto = Column(Numeric(18, 4), nullable=False)
    header = relationship("GoodsIssueH", back_populates="details")
    material = relationship("MasterMaterial")
    unit_ref = relationship("MasterUnit")

class GoodsReceiptD(Base):
    __tablename__ = 'goodsreceiptd'
    DocNo = Column(String(15), ForeignKey('goodsreceipth.DocNo'), primary_key=True)
    Number = Column(Integer, primary_key=True)
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), primary_key=True)
    Info = Column(String(1024), nullable=False)
    BatchNo = Column(String(20), nullable=False)
    BatchInfo = Column(String(50), nullable=False)
    ExpiryDate = Column(Date, nullable=True)
    TagNo = Column(String(10), primary_key=True)
    Unit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    Qty = Column(Numeric(18, 4), nullable=False)

    header = relationship("GoodsReceiptH", back_populates="details")
    material = relationship("MasterMaterial")
    unit_ref = relationship("MasterUnit")

class GoodsReceiptH(Base):
    __tablename__ = 'goodsreceipth'
    # ... (semua kolom Anda)
    DocNo = Column(String(15), primary_key=True)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SupplierCode = Column(String(10), ForeignKey('mastersupplier.Code'), nullable=False)
    PODocNo = Column(String(15), ForeignKey('purchaseorderh.DocNo'), nullable=False)
    Location = Column(String(5), nullable=False)
    Zone = Column(String(10), nullable=False)
    SupplierDlvDocNo = Column(String(20), nullable=False)
    VehicleNo = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=True)
    PrintedDate = Column(DateTime, nullable=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    # TAMBAHKAN RELASI INI
    details = relationship("GoodsReceiptD", back_populates="header")
    purchase_order = relationship("PurchaseOrderH", back_populates="goods_receipts")
    supplier = relationship("MasterSupplier")