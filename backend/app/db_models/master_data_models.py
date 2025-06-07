# backend/app/db_models/master_data_models.py
from sqlalchemy import (Column, String, Date, Integer, Numeric, ForeignKey,
                        DateTime, Time, BigInteger, and_, ForeignKeyConstraint)
from sqlalchemy.dialects.mysql import BIT, TINYINT
from sqlalchemy.orm import relationship
from .base import Base

# ==============================================================================
# Model-Model Dasar Tanpa Dependensi atau dengan Dependensi Sederhana
# ==============================================================================

class MasterCountry(Base):
    __tablename__ = 'mastercountry'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    provinces = relationship("MasterProvince", back_populates="country_ref")
    customers = relationship("MasterCustomer", back_populates="country_ref")
    suppliers = relationship("MasterSupplier", foreign_keys="[MasterSupplier.Country]", back_populates="country_ref")
    locations = relationship("MasterLocation", back_populates="country_ref")

class MasterUnit(Base):
    __tablename__ = 'masterunit'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    unit_conversions = relationship("MasterUnitConversion", back_populates="unit_ref")
    materials_smallest_unit = relationship("MasterMaterial", foreign_keys="[MasterMaterial.SmallestUnit]", back_populates="smallest_unit_ref")
    materials_sold_unit = relationship("MasterMaterial", foreign_keys="[MasterMaterial.SoldUnit]", back_populates="sold_unit_ref")
    materials_sku_unit = relationship("MasterMaterial", foreign_keys="[MasterMaterial.SKUUnit]", back_populates="sku_unit_ref")

class MasterCurrency(Base):
    __tablename__ = 'mastercurrency'
    Code = Column(String(3), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    customers = relationship("MasterCustomer", back_populates="currency_ref")
    suppliers = relationship("MasterSupplier", back_populates="currency_ref")
    materials = relationship("MasterMaterial", back_populates="currency_ref")
    accounts = relationship("MasterAccount", back_populates="currency_ref")

class MasterCustomerGroup(Base):
    __tablename__ = 'mastercustomergroup'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    customers = relationship("MasterCustomer", back_populates="customer_group_ref")

class MasterPriceListType(Base):
    __tablename__ = 'masterpricelisttype'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    customers = relationship("MasterCustomer", back_populates="price_list_type_ref")

class MasterAccountGroup(Base):
    __tablename__ = 'masteraccountgroup'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    accounts = relationship("MasterAccount", back_populates="account_group_ref")

class MasterDepartment(Base):
    __tablename__ = 'masterdepartment'
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    accounts = relationship("MasterAccount", back_populates="department_ref")

class MasterMaterialType(Base):
    __tablename__ = 'mastermaterialtype'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    IsWaste = Column(BIT, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    materials = relationship("MasterMaterial", back_populates="type_ref")

class MasterEmployeeH(Base):
    __tablename__ = 'masteremployeeh'
    EmployeeNo = Column(String(10), primary_key=True)
    Name = Column(String(50), nullable=False)
    Gender = Column(String(1), nullable=False)
    BirthDate = Column(Date, nullable=False)
    Religion = Column(String(20), nullable=False)
    IsActive = Column(BIT, nullable=False)
    JoinDate = Column(Date, nullable=False)
    ResignDate = Column(Date, nullable=True)
    ResignReason = Column(String(50), nullable=False)
    Information = Column(String(1024), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    sales_rep_data = relationship("MasterSales", back_populates="employee_data_ref", uselist=False)

class MasterBank(Base):
    __tablename__ = 'masterbank'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

class MasterCollector(Base):
    __tablename__ = 'mastercollector'
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    Address = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Phone = Column(String(20), nullable=False)
    Mobile = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

# ==============================================================================
# Model-Model dengan Dependensi Hirarkis (Area, Akun, Grup Material)
# ==============================================================================

class MasterProvince(Base):
    __tablename__ = 'masterprovince'
    Country = Column(String(5), ForeignKey('mastercountry.Code'), primary_key=True)
    Code = Column(String(20), primary_key=True)
    Name = Column(String(50), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    country_ref = relationship("MasterCountry", back_populates="provinces")
    cities = relationship("MasterCity", back_populates="province_ref")

class MasterCity(Base):
    __tablename__ = 'mastercity'
    Country = Column(String(5), primary_key=True)
    Province = Column(String(20), primary_key=True)
    City = Column(String(50), primary_key=True)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['Country', 'Province'], ['masterprovince.Country', 'masterprovince.Code']),
    )

    province_ref = relationship("MasterProvince", back_populates="cities")
    suppliers_in_city = relationship("MasterSupplier", back_populates="city_ref", overlaps="country_ref,suppliers")

class MasterAccount(Base):
    __tablename__ = 'masteraccount'
    AccountNo = Column(String(20), primary_key=True)
    Name = Column(String(50), nullable=False)
    Level = Column(TINYINT, nullable=False)
    AccountGroup = Column(String(5), ForeignKey('masteraccountgroup.Code'), nullable=False)
    ParentNo = Column(String(20), ForeignKey('masteraccount.AccountNo'), nullable=True)
    IsJournal = Column(BIT, nullable=False)
    IsCashier = Column(BIT, nullable=False)
    Users = Column(String(512), nullable=False)
    Department = Column(String(10), ForeignKey('masterdepartment.Code'), nullable=False)
    Currency = Column(String(3), ForeignKey('mastercurrency.Code'), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    account_group_ref = relationship("MasterAccountGroup", back_populates="accounts")
    currency_ref = relationship("MasterCurrency", back_populates="accounts")
    department_ref = relationship("MasterDepartment", back_populates="accounts")
    
    parent_account = relationship("MasterAccount", remote_side=[AccountNo], back_populates="child_accounts")
    child_accounts = relationship("MasterAccount", back_populates="parent_account")
    transaction_types = relationship("MasterTransactionType", back_populates="master_account_ref")

class MasterMaterialGroup1(Base):
    __tablename__ = 'mastermaterialgroup1'
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    materials = relationship("MasterMaterial", back_populates="group1_ref")
    material_group2_children = relationship("MasterMaterialGroup2", back_populates="group1_as_parent")

class MasterMaterialGroup2(Base):
    __tablename__ = 'mastermaterialgroup2'
    Group1 = Column(String(10), ForeignKey('mastermaterialgroup1.Code'), primary_key=True)
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    group1_as_parent = relationship("MasterMaterialGroup1", back_populates="material_group2_children")
    material_group3_children = relationship("MasterMaterialGroup3", back_populates="group2_parent_ref")

class MasterMaterialGroup3(Base):
    __tablename__ = 'mastermaterialgroup3'
    Group1 = Column(String(10), primary_key=True)
    Group2 = Column(String(10), primary_key=True)
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Group1', 'Group2'], ['mastermaterialgroup2.Group1', 'mastermaterialgroup2.Code']),)
    
    group2_parent_ref = relationship("MasterMaterialGroup2", back_populates="material_group3_children")

class MasterSalesArea1(Base):
    __tablename__ = 'mastersalesarea1'
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    customers = relationship("MasterCustomer", back_populates="sales_area1_ref")
    sales_area2_children = relationship("MasterSalesArea2", back_populates="area1_parent_ref")

class MasterSalesArea2(Base):
    __tablename__ = 'mastersalesarea2'
    Area1 = Column(String(10), ForeignKey('mastersalesarea1.Code'), primary_key=True)
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    area1_parent_ref = relationship("MasterSalesArea1", back_populates="sales_area2_children")
    sales_area3_children = relationship("MasterSalesArea3", back_populates="area2_ref")

class MasterSalesArea3(Base):
    __tablename__ = 'mastersalesarea3'
    Area1 = Column(String(10), primary_key=True)
    Area2 = Column(String(10), primary_key=True)
    Code = Column(String(10), primary_key=True)
    Name = Column(String(40), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['Area1', 'Area2'], ['mastersalesarea2.Area1', 'mastersalesarea2.Code']),)
    
    area2_ref = relationship("MasterSalesArea2", back_populates="sales_area3_children")
    customers = relationship("MasterCustomer", back_populates="sales_area3_ref", viewonly=True, overlaps="area2_ref")

# ==============================================================================
# Model-Model Kompleks dengan Banyak Dependensi
# ==============================================================================

class MasterTransactionType(Base):
    __tablename__ = 'mastertransactiontype'
    Type = Column(String(20), primary_key=True)
    Description = Column(String(40), nullable=False)
    AccountNo = Column(String(20), ForeignKey('masteraccount.AccountNo'), nullable=False)
    Purpose = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    master_account_ref = relationship("MasterAccount", back_populates="transaction_types")

class MasterLocation(Base):
    __tablename__ = 'masterlocation'
    Code = Column(String(5), primary_key=True)
    Name = Column(String(40), nullable=False)
    IsWarehouseManagement = Column(BIT, nullable=False)
    IsQualityControl = Column(BIT, nullable=False)
    VolumeCapacity = Column(Numeric(18, 0), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(80), nullable=False)
    Country = Column(String(5), ForeignKey('mastercountry.Code'), nullable=False)
    Latitude = Column(Numeric(18, 7), nullable=False)
    Longitude = Column(Numeric(18, 7), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    country_ref = relationship("MasterCountry", back_populates="locations")
    # Relasi ke SalesInvoiceH dan model transaksi lain akan ditambahkan di model masing-masing

class MasterSales(Base):
    __tablename__ = 'mastersales'
    Code = Column(String(10), ForeignKey('masteremployeeh.EmployeeNo'), primary_key=True)
    Name = Column(String(40), nullable=False)
    Address = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Phone = Column(String(20), nullable=False)
    Mobile = Column(String(20), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    employee_data_ref = relationship("MasterEmployeeH", back_populates="sales_rep_data")
    sales_orders = relationship("SalesOrderH", back_populates="sales_person_ref")
    sales_invoices = relationship("SalesInvoiceH", back_populates="sales_person_ref")

class MasterSupplier(Base):
    __tablename__ = 'mastersupplier'
    Code = Column(String(10), primary_key=True)
    Name = Column(String(120), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(50), nullable=False)
    Country = Column(String(5), ForeignKey('mastercountry.Code'), primary_key=True) 
    Phone = Column(String(50), nullable=False)
    Province = Column(String(20), nullable=False)
    Fax = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)
    Contact = Column(String(40), nullable=False)
    Mobile = Column(String(50), nullable=False)
    TaxNumber = Column(String(21), nullable=False)
    TOP = Column(Integer, nullable=False)
    Currency = Column(String(3), ForeignKey('mastercurrency.Code'), nullable=False)
    Limit = Column(Numeric(18, 4), nullable=False)
    TransactionType = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    TransactionType2 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    CutPPh = Column(BIT, nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    
    __table_args__ = (
        ForeignKeyConstraint(['Country', 'Province', 'City'], ['mastercity.Country', 'mastercity.Province', 'mastercity.City']),
    )

    # Definisikan relasi dengan lebih eksplisit
    country_ref = relationship("MasterCountry", foreign_keys=[Country], back_populates="suppliers")
    city_ref = relationship("MasterCity", back_populates="suppliers_in_city", overlaps="country_ref,suppliers")
    currency_ref = relationship("MasterCurrency")
    transaction_type1_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType])
    transaction_type2_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType2])

class MasterCustomer(Base):
    __tablename__ = 'mastercustomer'
    Code = Column(String(10), primary_key=True)
    Name = Column(String(120), nullable=False)
    Address = Column(String(80), nullable=False)
    Address2 = Column(String(80), nullable=False)
    City = Column(String(20), nullable=False)
    Country = Column(String(5), ForeignKey('mastercountry.Code'), nullable=False)
    Phone = Column(String(50), nullable=False)
    Fax = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False)
    Contact = Column(String(40), nullable=False)
    Mobile = Column(String(50), nullable=False)
    WhatsAppSession = Column(String(20), nullable=False)
    WhatsAppNo = Column(String(20), nullable=False)
    TaxNumber = Column(String(21), nullable=False)
    CustomerGroup = Column(String(10), ForeignKey('mastercustomergroup.Code'), nullable=False)
    PriceListType = Column(String(5), ForeignKey('masterpricelisttype.Code'), nullable=False)
    SalesArea1 = Column(String(10), ForeignKey('mastersalesarea1.Code'), primary_key=True)
    SalesArea2 = Column(String(10), primary_key=True)
    SalesArea3 = Column(String(10), primary_key=True)
    TOP = Column(Integer, nullable=False)
    Currency = Column(String(3), ForeignKey('mastercurrency.Code'), nullable=False)
    Limit = Column(Numeric(18, 4), nullable=False)
    TransactionType = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    TransactionType2 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    CutPPh = Column(BIT, nullable=False)
    IsBlacklisted = Column(BIT, nullable=False)
    IsDeleted = Column(BIT, nullable=False)
    Latitude = Column(Numeric(18, 7), nullable=False)
    Longitude = Column(Numeric(18, 7), nullable=False)
    Information = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)
    Znowa = Column(String(1), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(['SalesArea1', 'SalesArea2', 'SalesArea3'], ['mastersalesarea3.Area1', 'mastersalesarea3.Area2', 'mastersalesarea3.Code']),
    )

    country_ref = relationship("MasterCountry", back_populates="customers")
    currency_ref = relationship("MasterCurrency", back_populates="customers")
    customer_group_ref = relationship("MasterCustomerGroup", back_populates="customers")
    price_list_type_ref = relationship("MasterPriceListType", back_populates="customers")
    sales_area1_ref = relationship("MasterSalesArea1", back_populates="customers")
    sales_area3_ref = relationship("MasterSalesArea3", back_populates="customers", viewonly=True, overlaps="sales_area1_ref")
    transaction_type1_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType])
    transaction_type2_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType2])
    partners_as_main = relationship("MasterCustomerPartner", foreign_keys="[MasterCustomerPartner.CustomerCode]", back_populates="main_customer")
    partners_as_partner = relationship("MasterCustomerPartner", foreign_keys="[MasterCustomerPartner.PartnerCode]", back_populates="partner_customer")
    # sales
    sales_orders = relationship("SalesOrderH", foreign_keys="[SalesOrderH.CustomerCode]", back_populates="customer")
    tax_to_sales_orders = relationship("SalesOrderH", foreign_keys="[SalesOrderH.TaxToCode]", back_populates="tax_to_customer_ref")
    sales_invoices = relationship("SalesInvoiceH", foreign_keys="[SalesInvoiceH.CustomerCode]", back_populates="customer")
    tax_to_sales_invoices = relationship("SalesInvoiceH", foreign_keys="[SalesInvoiceH.TaxToCode]", back_populates="tax_to_customer_ref")

class MasterMaterial(Base):
    __tablename__ = 'mastermaterial'
    Code = Column(String(20), primary_key=True)
    Name = Column(String(80), nullable=False)
    NameInPO = Column(String(80), nullable=False)
    Substitute = Column(String(20), ForeignKey('mastermaterial.Code'), nullable=True)
    SmallestUnit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    SoldUnit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    SKUUnit = Column(String(5), ForeignKey('masterunit.Code'), nullable=False)
    Group1 = Column(String(10), ForeignKey('mastermaterialgroup1.Code'), nullable=False)
    Group2 = Column(String(10), nullable=False)
    Group3 = Column(String(10), nullable=False)
    Type = Column(String(5), ForeignKey('mastermaterialtype.Code'), nullable=False)
    IsBatch = Column(BIT, nullable=False)
    IsService = Column(BIT, nullable=False)
    IsAsset = Column(BIT, nullable=False)
    IsPPh = Column(BIT, nullable=False)
    HS = Column(String(20), nullable=False)
    Barcode = Column(String(20), nullable=False)
    MinStock = Column(Numeric(18, 0), nullable=False)
    MaxStock = Column(Numeric(18, 0), nullable=False)
    Currency = Column(String(3), ForeignKey('mastercurrency.Code'), nullable=False)
    DefaultPrice = Column(Numeric(18, 4), nullable=False)
    TransactionType1 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    TransactionType2 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    TransactionType3 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    TransactionType4 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    TransactionType5 = Column(String(20), ForeignKey('mastertransactiontype.Type'), nullable=False)
    Info = Column(String(255), nullable=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['Group1', 'Group2'], ['mastermaterialgroup2.Group1', 'mastermaterialgroup2.Code']),
        ForeignKeyConstraint(['Group1', 'Group2', 'Group3'], ['mastermaterialgroup3.Group1', 'mastermaterialgroup3.Group2', 'mastermaterialgroup3.Code']),
    )

    currency_ref = relationship("MasterCurrency", back_populates="materials")
    group1_ref = relationship("MasterMaterialGroup1", back_populates="materials")
    type_ref = relationship("MasterMaterialType", back_populates="materials")
    
    smallest_unit_ref = relationship("MasterUnit", foreign_keys=[SmallestUnit], back_populates="materials_smallest_unit")
    sold_unit_ref = relationship("MasterUnit", foreign_keys=[SoldUnit], back_populates="materials_sold_unit")
    sku_unit_ref = relationship("MasterUnit", foreign_keys=[SKUUnit], back_populates="materials_sku_unit")
    
    substitute_material = relationship("MasterMaterial", remote_side=[Code], uselist=False)
    unit_conversions = relationship("MasterUnitConversion", back_populates="material")
    
    transaction_type1_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType1])
    transaction_type2_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType2])
    transaction_type3_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType3])
    transaction_type4_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType4])
    transaction_type5_ref = relationship("MasterTransactionType", foreign_keys=[TransactionType5])

class MasterUnitConversion(Base):
    __tablename__ = 'masterunitconversion'
    MaterialCode = Column(String(20), ForeignKey('mastermaterial.Code'), primary_key=True)
    Unit = Column(String(5), ForeignKey('masterunit.Code'), primary_key=True)
    Content = Column(Numeric(18, 4), nullable=False)
    Weight = Column(Numeric(18, 4), nullable=False)
    Volume = Column(Numeric(18, 4), nullable=False)
    IsInactive = Column(BIT, nullable=False, default=False)
    CreatedBy = Column(String(16), nullable=False)
    CreatedDate = Column(DateTime, nullable=False)
    ChangedBy = Column(String(16), nullable=False)
    ChangedDate = Column(DateTime, nullable=False)

    material = relationship("MasterMaterial", back_populates="unit_conversions")
    unit_ref = relationship("MasterUnit", back_populates="unit_conversions")

class MasterCustomerPartner(Base):
    __tablename__ = 'mastercustomerpartner'
    CustomerCode = Column(String(10), primary_key=True)
    PartnerCode = Column(String(10), primary_key=True)
    PartnerFunc = Column(String(10), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(['CustomerCode'], ['mastercustomer.Code']),
        ForeignKeyConstraint(['PartnerCode'], ['mastercustomer.Code']),
    )
    
    main_customer = relationship("MasterCustomer", foreign_keys=[CustomerCode], back_populates="partners_as_main")
    partner_customer = relationship("MasterCustomer", foreign_keys=[PartnerCode], back_populates="partners_as_partner")