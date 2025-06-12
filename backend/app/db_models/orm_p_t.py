from sqlalchemy import Column, Integer, String, Text, DECIMAL, Float, Date, DateTime, Boolean, TIMESTAMP, CHAR, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Packinglistd(Base):
    __tablename__ = 'packinglistd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    GIDocNo = Column(String(15), primary_key=True, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['GIDocNo'], ['goodsissueh.DocNo'], name='fk_packinglistd_goodsissueh_0', use_alter=True),)

    # --- Relationships ---
    goodsissueh_ref = relationship("Goodsissueh", back_populates="packinglistd_collection", foreign_keys=[GIDocNo])

class Packinglisth(Base):
    __tablename__ = 'packinglisth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    ContainerNo = Column(String(30), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Plugind(Base):
    __tablename__ = 'plugind'

    Plugin = Column(String(20), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MenuName = Column(String(50), nullable=False)
    MenuText = Column(String(50), nullable=False)
    ParentMenu = Column(String(50), nullable=False)
    Form = Column(String(50), nullable=False)
    Query = Column(String(1024), nullable=False)
    PrefixReportFile = Column(String(50), nullable=False)

class Pluginh(Base):
    __tablename__ = 'pluginh'

    Plugin = Column(String(20), primary_key=True, nullable=False)
    Filename = Column(String(50), nullable=False)
    License = Column(String(50), nullable=False)

class Pointofsaled(Base):
    __tablename__ = 'pointofsaled'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    BaseQty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)
    PromoQty = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_pointofsaled_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="pointofsaled_collection", foreign_keys=[MaterialCode, Unit])

class Pointofsaleh(Base):
    __tablename__ = 'pointofsaleh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    SalesCode = Column(String(10), nullable=False)
    CustomerCode = Column(String(15), nullable=False)
    CustomerName = Column(String(45), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Mobile = Column(String(50), nullable=False)
    PONo = Column(String(50), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    Payment = Column(DECIMAL(18, 4), nullable=False)
    Change = Column(DECIMAL(18, 4), nullable=False)
    Rounding = Column(DECIMAL(18, 4), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['CustomerCode'], ['mastercustomer.Code'], name='fk_pointofsaleh_mastercustomer_0', use_alter=True), ForeignKeyConstraint(['SalesCode'], ['mastersales.Code'], name='fk_pointofsaleh_mastersales_1', use_alter=True),)

    # --- Relationships ---
    mastercustomer_ref = relationship("Mastercustomer", back_populates="pointofsaleh_collection", foreign_keys=[CustomerCode])
    mastersales_ref = relationship("Mastersales", back_populates="pointofsaleh_collection", foreign_keys=[SalesCode])

class Pointofsalett(Base):
    __tablename__ = 'pointofsalett'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TransactionType = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(255), primary_key=True, nullable=False)
    Payment = Column(DECIMAL(18, 4), nullable=False)

class Posstartbalanceh(Base):
    __tablename__ = 'posstartbalanceh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TransactionType = Column(String(20), nullable=False)
    User = Column(String(16), nullable=False)
    StartBalance = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
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

class Proformainvoiced(Base):
    __tablename__ = 'proformainvoiced'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(255), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Proformainvoiceh(Base):
    __tablename__ = 'proformainvoiceh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    ShipToCode = Column(String(10), nullable=False)
    PONo = Column(String(50), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Purchasecostd(Base):
    __tablename__ = 'purchasecostd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Description = Column(String(50), primary_key=True, nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

class Purchasecosth(Base):
    __tablename__ = 'purchasecosth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TransactionType = Column(String(20), nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    SupplierTaxTo = Column(String(10), nullable=False)
    SupplierInvNo = Column(String(20), nullable=False)
    TOP = Column(Integer, nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    InvoiceDocNo = Column(String(15), nullable=False)
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

    __table_args__ = (ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_purchasecosth_mastercurrency_0', use_alter=True), ForeignKeyConstraint(['SupplierCode'], ['mastersupplier.Code'], name='fk_purchasecosth_mastersupplier_1', use_alter=True),)

    # --- Relationships ---
    mastercurrency_ref = relationship("Mastercurrency", back_populates="purchasecosth_collection", foreign_keys=[Currency])
    mastersupplier_ref = relationship("Mastersupplier", back_populates="purchasecosth_collection", foreign_keys=[SupplierCode])

class Purchaseinvoicec(Base):
    __tablename__ = 'purchaseinvoicec'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    PCDocNo = Column(String(15), primary_key=True, nullable=False)

class Purchaseinvoiced(Base):
    __tablename__ = 'purchaseinvoiced'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_purchaseinvoiced_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="purchaseinvoiced_collection", foreign_keys=[MaterialCode, Unit])

class Purchaseinvoicedp(Base):
    __tablename__ = 'purchaseinvoicedp'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    DPDocNo = Column(String(16), primary_key=True, nullable=False)
    Usage = Column(DECIMAL(18, 4), nullable=False)

class Purchaseinvoicegr(Base):
    __tablename__ = 'purchaseinvoicegr'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    GRDocNo = Column(String(15), primary_key=True, nullable=False)

class Purchaseinvoiceh(Base):
    __tablename__ = 'purchaseinvoiceh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    PODocNo = Column(String(15), nullable=False)
    JODocNo = Column(String(15), nullable=False)
    Trip = Column(String(20), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    GRDocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    SupplierTaxTo = Column(String(10), nullable=False)
    SupplierInvNo = Column(String(20), nullable=False)
    TOP = Column(Integer, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    CostDistribution = Column(String(10), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    DownPayment = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    CutPPh = Column(Boolean, nullable=False)
    PPhPercent = Column(DECIMAL(18, 4), nullable=False)
    PPhValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(20), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_purchaseinvoiceh_mastercurrency_0', use_alter=True), ForeignKeyConstraint(['SupplierCode'], ['mastersupplier.Code'], name='fk_purchaseinvoiceh_mastersupplier_1', use_alter=True), ForeignKeyConstraint(['SupplierTaxTo'], ['mastersupplier.Code'], name='fk_purchaseinvoiceh_mastersupplier_2', use_alter=True),)

    # --- Relationships ---
    mastercurrency_ref = relationship("Mastercurrency", back_populates="purchaseinvoiceh_collection", foreign_keys=[Currency])
    mastersupplier_ref_via_SupplierCode = relationship("Mastersupplier", back_populates="purchaseinvoiceh_collection_via_SupplierCode", foreign_keys=[SupplierCode])
    mastersupplier_ref_via_SupplierTaxTo = relationship("Mastersupplier", back_populates="purchaseinvoiceh_collection_via_SupplierTaxTo", foreign_keys=[SupplierTaxTo])

class Purchaseorderd(Base):
    __tablename__ = 'purchaseorderd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(1024), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    QtyReceived = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_purchaseorderd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="purchaseorderd_collection", foreign_keys=[MaterialCode, Unit])

class Purchaseorderh(Base):
    __tablename__ = 'purchaseorderh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    DocDate = Column(Date, nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    DeliveryDate = Column(Date, nullable=False)
    TOP = Column(Integer, nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    JODocNo = Column(String(15), nullable=False)
    Trip = Column(String(20), nullable=False)
    SIDocNo = Column(String(15), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    CutPPh = Column(Boolean, nullable=False)
    PPhPercent = Column(DECIMAL(18, 4), nullable=False)
    PPhValue = Column(DECIMAL(18, 4), nullable=False)
    SendTo = Column(String(50), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16))
    ApprovedDate = Column(DateTime)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    IsSalesReturn = Column(Boolean, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Purchaseorderpr(Base):
    __tablename__ = 'purchaseorderpr'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    PRDocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    QtyPO = Column(DECIMAL(18, 4), nullable=False)

class Purchaserequestd(Base):
    __tablename__ = 'purchaserequestd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(1024), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    RequiredDate = Column(Date, nullable=False)
    QtyPO = Column(DECIMAL(18, 4), nullable=False)

class Purchaserequesth(Base):
    __tablename__ = 'purchaserequesth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    JODocNo = Column(String(15), nullable=False)
    Trip = Column(String(20), nullable=False)
    Department = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16))
    ApprovedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Purchasereturnd(Base):
    __tablename__ = 'purchasereturnd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_purchasereturnd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="purchasereturnd_collection", foreign_keys=[MaterialCode, Unit])

class Purchasereturnh(Base):
    __tablename__ = 'purchasereturnh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    GIDocNo = Column(String(15), nullable=False)
    SupplierCode = Column(String(10), nullable=False)
    SupplierTaxTo = Column(String(10), nullable=False)
    SupplierDocNo = Column(String(20), nullable=False)
    TaxNo = Column(String(20), nullable=False)
    TaxDate = Column(Date, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_purchasereturnh_mastercurrency_0', use_alter=True), ForeignKeyConstraint(['SupplierCode'], ['mastersupplier.Code'], name='fk_purchasereturnh_mastersupplier_1', use_alter=True), ForeignKeyConstraint(['SupplierTaxTo'], ['mastersupplier.Code'], name='fk_purchasereturnh_mastersupplier_2', use_alter=True),)

    # --- Relationships ---
    mastercurrency_ref = relationship("Mastercurrency", back_populates="purchasereturnh_collection", foreign_keys=[Currency])
    mastersupplier_ref_via_SupplierCode = relationship("Mastersupplier", back_populates="purchasereturnh_collection_via_SupplierCode", foreign_keys=[SupplierCode])
    mastersupplier_ref_via_SupplierTaxTo = relationship("Mastersupplier", back_populates="purchasereturnh_collection_via_SupplierTaxTo", foreign_keys=[SupplierTaxTo])

class Putawaylistd(Base):
    __tablename__ = 'putawaylistd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(15), nullable=False)
    TagNo = Column(String(10), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Putawaylisth(Base):
    __tablename__ = 'putawaylisth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Putawaylistr(Base):
    __tablename__ = 'putawaylistr'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Qualitycontrol(Base):
    __tablename__ = 'qualitycontrol'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    QCStatus = Column(String(10), nullable=False)
    QCInfo = Column(String(255), nullable=False)
    CheckedBy = Column(String(16), nullable=False)
    CheckedDate = Column(DateTime, nullable=False)
    QtyGood = Column(DECIMAL(18, 4), nullable=False)
    QtyBad = Column(DECIMAL(18, 4), nullable=False)
    SeriesGood = Column(String(3), nullable=False)
    SeriesBad = Column(String(3), nullable=False)
    TransferDateGood = Column(Date)
    TransferDateBad = Column(Date)
    LocationGood = Column(String(5), nullable=False)
    LocationBad = Column(String(5), nullable=False)
    TransferDocNoGood = Column(String(15), nullable=False)
    TransferDocNoBad = Column(String(15), nullable=False)

class Refreshcubelog(Base):
    __tablename__ = 'refreshcubelog'

    Periode = Column(Date, primary_key=True, nullable=False)
    Name = Column(String(50), primary_key=True, nullable=False)
    RefreshedBy = Column(String(16), nullable=False)
    RefreshedDate = Column(DateTime, nullable=False)
    TotalRow = Column(Integer, nullable=False)

class Reportfile(Base):
    __tablename__ = 'reportfile'

    Filename = Column(String(255), primary_key=True, nullable=False)

class Reportmanagement(Base):
    __tablename__ = 'reportmanagement'

    Role = Column(String(16), primary_key=True, nullable=False)
    MenuName = Column(String(50), primary_key=True, nullable=False)
    IsNoShowGrid = Column(Boolean, nullable=False)
    IsNoPrint = Column(Boolean, nullable=False)
    IsNoExport = Column(Boolean, nullable=False)
    DefaultReportFile = Column(String(100), nullable=False)
    HiddenReportFiles = Column(Text, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Reportrequest(Base):
    __tablename__ = 'reportrequest'

    ID = Column(String(50), primary_key=True, nullable=False)
    Api = Column(String(255), nullable=False)
    Parameters = Column(Text, nullable=False)
    FilterText = Column(String(512), nullable=False)
    Filename = Column(String(255), nullable=False)
    Token = Column(String(512), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    StartedDate = Column(DateTime)
    CompletedDate = Column(DateTime)
    Status = Column(String(20), nullable=False)
    ErrorMessage = Column(String(512), nullable=False)

class Resetprintcounterlog(Base):
    __tablename__ = 'resetprintcounterlog'

    ResetTime = Column(DateTime, primary_key=True, nullable=False)
    ResetBy = Column(String(16), primary_key=True, nullable=False)
    Document = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    Reason = Column(String(100), nullable=False)

class Role(Base):
    __tablename__ = 'role'

    Role = Column(String(16), primary_key=True, nullable=False)
    User = Column(String(16), primary_key=True, nullable=False)

class Salesinvoiced(Base):
    __tablename__ = 'salesinvoiced'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_salesinvoiced_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="salesinvoiced_collection", foreign_keys=[MaterialCode, Unit])

class Salesinvoicedp(Base):
    __tablename__ = 'salesinvoicedp'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    DPDocNo = Column(String(16), primary_key=True, nullable=False)
    Usage = Column(DECIMAL(18, 4), nullable=False)

class Salesinvoicegi(Base):
    __tablename__ = 'salesinvoicegi'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    GIDocNo = Column(String(15), primary_key=True, nullable=False)

class Salesinvoiceh(Base):
    __tablename__ = 'salesinvoiceh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    SODocNo = Column(String(15), nullable=False)
    GIDocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    PONo = Column(String(50), nullable=False)
    CustomerCode = Column(String(15), nullable=False)
    TaxToCode = Column(String(15), nullable=False)
    SalesCode = Column(String(10), nullable=False)
    TOP = Column(Integer, nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    DownPayment = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    PPhStatus = Column(String(10), nullable=False)
    CutPPh = Column(Boolean, nullable=False)
    PPhPercent = Column(DECIMAL(18, 4), nullable=False)
    PPhValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['CustomerCode'], ['mastercustomer.Code'], name='fk_salesinvoiceh_mastercustomer_0', use_alter=True), ForeignKeyConstraint(['TaxToCode'], ['mastercustomer.Code'], name='fk_salesinvoiceh_mastercustomer_1', use_alter=True), ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_salesinvoiceh_mastercurrency_2', use_alter=True), ForeignKeyConstraint(['SalesCode'], ['mastersales.Code'], name='fk_salesinvoiceh_mastersales_3', use_alter=True),)

    # --- Relationships ---
    mastercustomer_ref_via_CustomerCode = relationship("Mastercustomer", back_populates="salesinvoiceh_collection_via_CustomerCode", foreign_keys=[CustomerCode])
    mastercustomer_ref_via_TaxToCode = relationship("Mastercustomer", back_populates="salesinvoiceh_collection_via_TaxToCode", foreign_keys=[TaxToCode])
    mastercurrency_ref = relationship("Mastercurrency", back_populates="salesinvoiceh_collection", foreign_keys=[Currency])
    mastersales_ref = relationship("Mastersales", back_populates="salesinvoiceh_collection", foreign_keys=[SalesCode])

class Salesinvoicerd(Base):
    __tablename__ = 'salesinvoicerd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    RebateCode = Column(String(10), nullable=False)
    RebatePercent = Column(DECIMAL(18, 4), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    RebateValue = Column(DECIMAL(18, 4), nullable=False)

class Salesinvoicers(Base):
    __tablename__ = 'salesinvoicers'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)

class Salesorderd(Base):
    __tablename__ = 'salesorderd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    Info = Column(String(1024), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    QtyDelivered = Column(DECIMAL(18, 4), nullable=False)
    QtyWO = Column(DECIMAL(18, 4), nullable=False)
    QtyBooked = Column(DECIMAL(18, 4), nullable=False)
    PromoQty = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_salesorderd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="salesorderd_collection", foreign_keys=[MaterialCode, Unit])

class Salesorderh(Base):
    __tablename__ = 'salesorderh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    ShipToCode = Column(String(10), nullable=False)
    TaxToCode = Column(String(10), nullable=False)
    SalesCode = Column(String(10), nullable=False)
    DeliveryDate = Column(Date, nullable=False)
    PONo = Column(String(50), nullable=False)
    TOP = Column(Integer, nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    PPhStatus = Column(String(10), nullable=False)
    CutPPh = Column(Boolean, nullable=False)
    PPhPercent = Column(DECIMAL(18, 4), nullable=False)
    PPhValue = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    IsPurchaseReturn = Column(Boolean, nullable=False)
    IsApproved = Column(Boolean, nullable=False)
    ApprovedBy = Column(String(16))
    ApprovedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Currency'], ['mastercurrency.Code'], name='fk_salesorderh_mastercurrency_0', use_alter=True),)

    # --- Relationships ---
    mastercurrency_ref = relationship("Mastercurrency", back_populates="salesorderh_collection", foreign_keys=[Currency])

class Salesorderrd(Base):
    __tablename__ = 'salesorderrd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
    RebateCode = Column(String(10), nullable=False)
    RebatePercent = Column(DECIMAL(18, 4), nullable=False)
    DocValue = Column(DECIMAL(18, 4), nullable=False)
    RebateValue = Column(DECIMAL(18, 4), nullable=False)

class Salesorderrs(Base):
    __tablename__ = 'salesorderrs'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)

class Salesordersch(Base):
    __tablename__ = 'salesordersch'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    DeliveryDate = Column(Date, primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)

class Salesreturnd(Base):
    __tablename__ = 'salesreturnd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(1024), nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    OriginalTagNo = Column(String(10), nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Gross = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent2 = Column(DECIMAL(18, 4), nullable=False)
    DiscPercent3 = Column(DECIMAL(18, 4), nullable=False)
    DiscValue = Column(DECIMAL(18, 4), nullable=False)
    DiscNominal = Column(DECIMAL(18, 4), nullable=False)
    Netto = Column(DECIMAL(18, 4), nullable=False)
    Cost = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_salesreturnd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="salesreturnd_collection", foreign_keys=[MaterialCode, Unit])

class Salesreturnh(Base):
    __tablename__ = 'salesreturnh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    PODocNo = Column(String(15), nullable=False)
    GRDocNo = Column(String(15), nullable=False)
    SIDocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    CustomerTaxTo = Column(String(10), nullable=False)
    SalesCode = Column(String(10), nullable=False)
    Currency = Column(String(3), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    TaxStatus = Column(String(10), nullable=False)
    TaxPercent = Column(DECIMAL(18, 4), nullable=False)
    TaxPrefix = Column(String(3), nullable=False)
    TaxNo = Column(String(25), nullable=False)
    TaxDate = Column(Date, nullable=False)
    DiscPercent = Column(DECIMAL(18, 4), nullable=False)
    TotalGross = Column(DECIMAL(18, 4), nullable=False)
    TotalDisc = Column(DECIMAL(18, 4), nullable=False)
    TaxValue = Column(DECIMAL(18, 4), nullable=False)
    TaxValueInTaxCur = Column(DECIMAL(18, 4), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)
    TotalCost = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['CustomerCode'], ['mastercustomer.Code'], name='fk_salesreturnh_mastercustomer_0', use_alter=True), ForeignKeyConstraint(['CustomerTaxTo'], ['mastercustomer.Code'], name='fk_salesreturnh_mastercustomer_1', use_alter=True),)

    # --- Relationships ---
    mastercustomer_ref_via_CustomerCode = relationship("Mastercustomer", back_populates="salesreturnh_collection_via_CustomerCode", foreign_keys=[CustomerCode])
    mastercustomer_ref_via_CustomerTaxTo = relationship("Mastercustomer", back_populates="salesreturnh_collection_via_CustomerTaxTo", foreign_keys=[CustomerTaxTo])

class Scheduledjournald(Base):
    __tablename__ = 'scheduledjournald'

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

class Scheduledjournalh(Base):
    __tablename__ = 'scheduledjournalh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    StartDate = Column(Date, nullable=False)
    EndDate = Column(Date, nullable=False)
    IsEndOfMonth = Column(Boolean, nullable=False)
    DayOfMonth = Column(Integer, nullable=False)
    TotalDebet = Column(DECIMAL(18, 4), nullable=False)
    TotalCredit = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Shipmentd(Base):
    __tablename__ = 'shipmentd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    GIDocNo = Column(String(15), primary_key=True, nullable=False)

class Shipmenth(Base):
    __tablename__ = 'shipmenth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Location = Column(String(5), nullable=False)
    Zone = Column(String(10), nullable=False)
    VehicleNo = Column(String(10), nullable=False)
    TotalVolume = Column(DECIMAL(18, 4), nullable=False)
    TotalWeight = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Shortcut(Base):
    __tablename__ = 'shortcut'

    User = Column(String(16), primary_key=True, nullable=False)
    Menu = Column(String(50), primary_key=True, nullable=False)
    Ctrl = Column(Boolean, nullable=False)
    Alt = Column(Boolean, nullable=False)
    Key = Column(String(20), nullable=False)

class Smladjustment(Base):
    __tablename__ = 'smladjustment'

    DocDate = Column(Date, primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    PODocNo = Column(String(15), nullable=False)
    GRDocNo = Column(String(15), nullable=False)
    PIDocNo = Column(String(15), nullable=False)
    BaseQty = Column(DECIMAL(18, 4), nullable=False)

class Smlexcludeddocument(Base):
    __tablename__ = 'smlexcludeddocument'

    DocDate = Column(Date, primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    GIDocNo = Column(String(15), nullable=False)
    SODocNo = Column(String(15), nullable=False)
    TotalNetto = Column(DECIMAL(18, 4), nullable=False)

class Smlprocesslog(Base):
    __tablename__ = 'smlprocesslog'

    DocDate = Column(Date, primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    OriginalBaseQty = Column(DECIMAL(18, 4), nullable=False)
    NewBaseQty = Column(DECIMAL(18, 4), nullable=False)

class Specialjournald(Base):
    __tablename__ = 'specialjournald'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    AccountNo = Column(String(20), primary_key=True, nullable=False)
    Info = Column(String(255), primary_key=True, nullable=False)
    Currency = Column(String(3), nullable=False)
    Debet = Column(DECIMAL(18, 4), nullable=False)
    Credit = Column(DECIMAL(18, 4), nullable=False)
    ExchangeRate = Column(DECIMAL(18, 4), nullable=False)
    DebetLocal = Column(DECIMAL(18, 4), nullable=False)
    CreditLocal = Column(DECIMAL(18, 4), nullable=False)

class Specialjournalh(Base):
    __tablename__ = 'specialjournalh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    JournalType = Column(String(20), nullable=False)
    BusinessUnit = Column(String(20), nullable=False)
    TotalDebet = Column(DECIMAL(18, 4), nullable=False)
    TotalCredit = Column(DECIMAL(18, 4), nullable=False)
    PostedBy = Column(String(16), nullable=False)
    PostedDate = Column(DateTime, nullable=False)
    Information = Column(String(255), nullable=False)

class Stock(Base):
    __tablename__ = 'stock'

    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    DocNo = Column(String(15), primary_key=True, nullable=False)
    DocDate = Column(Date, primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Number = Column(Integer, primary_key=True, nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Location'], ['masterlocation.Code'], name='fk_stock_masterlocation_0', use_alter=True), ForeignKeyConstraint(['MaterialCode'], ['mastermaterial.Code'], name='fk_stock_mastermaterial_1', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref = relationship("Masterlocation", back_populates="stock_collection", foreign_keys=[Location])
    mastermaterial_ref = relationship("Mastermaterial", back_populates="stock_collection", foreign_keys=[MaterialCode])

class Stockbalance(Base):
    __tablename__ = 'stockbalance'

    Periode = Column(Date, primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Location = Column(String(5), primary_key=True, nullable=False)
    Zone = Column(String(10), primary_key=True, nullable=False)
    Bin = Column(String(10), primary_key=True, nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    QtyStart = Column(DECIMAL(18, 4), nullable=False)
    QtyIn = Column(DECIMAL(18, 4), nullable=False)
    QtyOut = Column(DECIMAL(18, 4), nullable=False)
    QtyEnd = Column(DECIMAL(18, 4), nullable=False)
    QtyBook = Column(DECIMAL(18, 4), nullable=False)

class Stockpriceadjustment(Base):
    __tablename__ = 'stockpriceadjustment'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    MaterialCode = Column(String(20), nullable=False)
    TotalAdjustment = Column(DECIMAL(18, 4), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Stocktransferd(Base):
    __tablename__ = 'stocktransferd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    BaseQty = Column(DECIMAL(18, 4), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['MaterialCode', 'Unit'], ['masterunitconversion.MaterialCode', 'masterunitconversion.Unit'], name='fk_stocktransferd_masterunitconversion_0', use_alter=True),)

    # --- Relationships ---
    masterunitconversion_ref = relationship("Masterunitconversion", back_populates="stocktransferd_collection", foreign_keys=[MaterialCode, Unit])

class Stocktransferh(Base):
    __tablename__ = 'stocktransferh'

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
    Znojob = Column(String(15))

    __table_args__ = (ForeignKeyConstraint(['FromLocation'], ['masterlocation.Code'], name='fk_stocktransferh_masterlocation_0', use_alter=True), ForeignKeyConstraint(['ToLocation'], ['masterlocation.Code'], name='fk_stocktransferh_masterlocation_1', use_alter=True),)

    # --- Relationships ---
    masterlocation_ref_via_FromLocation = relationship("Masterlocation", back_populates="stocktransferh_collection_via_FromLocation", foreign_keys=[FromLocation])
    masterlocation_ref_via_ToLocation = relationship("Masterlocation", back_populates="stocktransferh_collection_via_ToLocation", foreign_keys=[ToLocation])

class Stocktransferrequestd(Base):
    __tablename__ = 'stocktransferrequestd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    Qty = Column(DECIMAL(18, 4), nullable=False)
    QtyTransfer = Column(DECIMAL(18, 4), nullable=False)

class Stocktransferrequesth(Base):
    __tablename__ = 'stocktransferrequesth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    ToLocation = Column(String(5), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    Znojob = Column(String(15))

class Supplierbalance(Base):
    __tablename__ = 'supplierbalance'

    Periode = Column(Date, primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
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

class Supplierdpbalance(Base):
    __tablename__ = 'supplierdpbalance'

    Periode = Column(Date, primary_key=True, nullable=False)
    SupplierCode = Column(String(10), primary_key=True, nullable=False)
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

class Surveyresult(Base):
    __tablename__ = 'surveyresult'

    SurveyDate = Column(Date, primary_key=True, nullable=False)
    SurveyCode = Column(String(20), primary_key=True, nullable=False)
    CustomerCode = Column(String(10), primary_key=True, nullable=False)
    EmployeeNo = Column(String(10), primary_key=True, nullable=False)
    QuestionNo = Column(Integer, primary_key=True, nullable=False)
    AnswerNo = Column(Integer, primary_key=True, nullable=False)
    AnswerText = Column(String(255), nullable=False)

class Taxno(Base):
    __tablename__ = 'taxno'

    TaxNo = Column(String(25), primary_key=True, nullable=False)
    DocNo = Column(String(15), nullable=False)

class Transferorderd(Base):
    __tablename__ = 'transferorderd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    MaterialCode = Column(String(20), primary_key=True, nullable=False)
    TagNo = Column(String(10), primary_key=True, nullable=False)
    FromBin = Column(String(10), primary_key=True, nullable=False)
    ToBin = Column(String(10), primary_key=True, nullable=False)
    Unit = Column(String(5), nullable=False)
    AskQty = Column(DECIMAL(18, 4), nullable=False)
    ActualQty = Column(DECIMAL(18, 4), nullable=False)

class Transferorderh(Base):
    __tablename__ = 'transferorderh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    RefDocNo = Column(String(15), nullable=False)
    Location = Column(String(5), nullable=False)
    FromZone = Column(String(10), nullable=False)
    ToZone = Column(String(10), nullable=False)
    Equipment = Column(String(10), nullable=False)
    TotalVolume = Column(DECIMAL(18, 4), nullable=False)
    TotalWeight = Column(DECIMAL(18, 4), nullable=False)
    StartTime = Column(DateTime)
    EndTime = Column(DateTime)
    Duration = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16))
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime)

class Transportclaimd(Base):
    __tablename__ = 'transportclaimd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Coly = Column(Integer, primary_key=True, nullable=False)
    Claim = Column(DECIMAL(18, 4), nullable=False)

class Transportclaimh(Base):
    __tablename__ = 'transportclaimh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TSIDocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    CustomerName = Column(String(40), nullable=False)
    CustomerAddress = Column(String(80), nullable=False)
    CustomerCity = Column(String(20), nullable=False)
    CustomerPhone = Column(String(20), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    TotalClaim = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Transportcoly(Base):
    __tablename__ = 'transportcoly'

    TSIDocNo = Column(String(15), primary_key=True, nullable=False)
    Coly = Column(Integer, primary_key=True, nullable=False)
    RouteCode = Column(String(10), nullable=False)
    Content = Column(String(100), nullable=False)
    Weight = Column(DECIMAL(18, 4), nullable=False)
    Volume = Column(DECIMAL(18, 4), nullable=False)
    VehicleCode = Column(String(10), nullable=False)
    ShipmentDocNo = Column(String(15), nullable=False)
    UnloadBy = Column(String(16), nullable=False)
    UnloadDate = Column(DateTime)
    DODocNo = Column(String(15), nullable=False)
    LoadLocalBy = Column(String(16), nullable=False)
    LoadLocalDate = Column(DateTime)
    UnloadLocalBy = Column(String(16), nullable=False)
    UnloadLocalDate = Column(DateTime)
    ClaimDocNo = Column(String(15), nullable=False)

class Transportdeliveryorderd(Base):
    __tablename__ = 'transportdeliveryorderd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TSIDocNo = Column(String(15), primary_key=True, nullable=False)
    Coly = Column(Integer, primary_key=True, nullable=False)
    Returned = Column(Boolean, nullable=False)

class Transportdeliveryorderh(Base):
    __tablename__ = 'transportdeliveryorderh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Vehicle = Column(String(10), nullable=False)
    Driver = Column(String(10), nullable=False)
    Location = Column(String(5), nullable=False)
    TotalColy = Column(Integer, nullable=False)
    TotalVolume = Column(Integer, nullable=False)
    TotalWeight = Column(Integer, nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Transportpickupassignment(Base):
    __tablename__ = 'transportpickupassignment'

    SRDocNo = Column(String(15), primary_key=True, nullable=False)
    AssignedDriver = Column(String(10), nullable=False)
    AssignedBy = Column(String(16), nullable=False)
    AssignedDate = Column(DateTime)
    PickBy = Column(String(10), nullable=False)
    PickDate = Column(DateTime)

class Transportsalesorderd(Base):
    __tablename__ = 'transportsalesorderd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Coly = Column(Integer, primary_key=True, nullable=False)
    Content = Column(String(100), primary_key=True, nullable=False)
    Weight = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    Length = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    Width = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    Height = Column(DECIMAL(18, 4), primary_key=True, nullable=False)
    Volume = Column(DECIMAL(18, 4), nullable=False)
    Price = Column(DECIMAL(18, 4), nullable=False)
    Surcharge = Column(DECIMAL(18, 4), nullable=False)
    SurchargeInfo = Column(String(100), nullable=False)
    SubTotal = Column(DECIMAL(18, 4), nullable=False)

class Transportsalesorderh(Base):
    __tablename__ = 'transportsalesorderh'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    TSRDocNo = Column(String(15), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    CustomerName = Column(String(40), nullable=False)
    CustomerAddress = Column(String(80), nullable=False)
    CustomerCity = Column(String(20), nullable=False)
    CustomerPhone = Column(String(20), nullable=False)
    Recipient = Column(String(40), nullable=False)
    RecipientAddress = Column(String(80), nullable=False)
    RecipientCity = Column(String(20), nullable=False)
    RecipientArea = Column(String(60), nullable=False)
    RecipientPhone = Column(String(20), nullable=False)
    RecipientInformation = Column(String(255), nullable=False)
    Payment = Column(String(10), nullable=False)
    TOP = Column(Integer, nullable=False)
    ARReqListSeries = Column(String(3), nullable=False)
    ARReqListNo = Column(String(15), nullable=False)
    TSISeries = Column(String(3), nullable=False)
    TSIDocNo = Column(String(15), nullable=False)
    TransactionType = Column(String(20), nullable=False)
    PackageType = Column(String(10), nullable=False)
    ServiceType = Column(String(10), nullable=False)
    Route = Column(String(10), nullable=False)
    VehicleType = Column(String(10), nullable=False)
    IsRent = Column(Boolean, nullable=False)
    RentStartDate = Column(Date)
    RentEndDate = Column(Date)
    RentDays = Column(Integer, nullable=False)
    TotalColy = Column(Integer, nullable=False)
    PriceList = Column(DECIMAL(18, 4), nullable=False)
    Total = Column(DECIMAL(18, 4), nullable=False)
    IncomeTaxPercent = Column(DECIMAL(18, 4), nullable=False)
    IncomeTax = Column(DECIMAL(18, 4), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Transportsalesrequestd(Base):
    __tablename__ = 'transportsalesrequestd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Coly = Column(Integer, primary_key=True, nullable=False)
    Content = Column(String(100), primary_key=True, nullable=False)

class Transportsalesrequesth(Base):
    __tablename__ = 'transportsalesrequesth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Series = Column(String(3), nullable=False)
    DocDate = Column(Date, nullable=False)
    Payment = Column(String(10), nullable=False)
    CustomerCode = Column(String(10), nullable=False)
    CustomerName = Column(String(40), nullable=False)
    CustomerAddress = Column(String(80), nullable=False)
    CustomerCity = Column(String(20), nullable=False)
    CustomerPhone = Column(String(20), nullable=False)
    Pickup = Column(Boolean, nullable=False)
    PickupAddress = Column(String(80), nullable=False)
    PickupCity = Column(String(20), nullable=False)
    PickupPhone = Column(String(20), nullable=False)
    PickupPIC = Column(String(40), nullable=False)
    PickupInformation = Column(String(255), nullable=False)
    Recipient = Column(String(40), nullable=False)
    RecipientAddress = Column(String(80), nullable=False)
    RecipientCity = Column(String(20), nullable=False)
    RecipientArea = Column(String(60), nullable=False)
    RecipientPhone = Column(String(20), nullable=False)
    RecipientInformation = Column(String(255), nullable=False)
    PackageType = Column(String(10), nullable=False)
    ServiceType = Column(String(10), nullable=False)
    Route = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class Transportsalesrequestp(Base):
    __tablename__ = 'transportsalesrequestp'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    Coly = Column(Integer, primary_key=True, nullable=False)
    Content = Column(String(100), primary_key=True, nullable=False)

class Transportshipmentd(Base):
    __tablename__ = 'transportshipmentd'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    TSIDocNo = Column(String(15), primary_key=True, nullable=False)
    TotalColy = Column(Integer, nullable=False)
    Information = Column(String(255), nullable=False)

class Transportshipmenth(Base):
    __tablename__ = 'transportshipmenth'

    DocNo = Column(String(15), primary_key=True, nullable=False)
    DocDate = Column(Date, nullable=False)
    VehicleCode = Column(String(10), nullable=False)
    RouteCode = Column(String(10), nullable=False)
    DriverCode = Column(String(10), nullable=False)
    Information = Column(String(255), nullable=False)
    Status = Column(String(20), nullable=False)
    PrintCounter = Column(Integer, nullable=False)
    PrintedBy = Column(String(16), nullable=False)
    PrintedDate = Column(DateTime)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)