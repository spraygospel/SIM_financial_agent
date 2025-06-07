# backend/factories/master_data.py
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal

class MasterDataFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("MasterCountry", self._build_master_country)
        self.main_factory.register_builder("MasterCurrency", self._build_master_currency)
        self.main_factory.register_builder("MasterSupplier", self._build_master_supplier)
        self.main_factory.register_builder("MasterCity", self._build_master_city)
        self.main_factory.register_builder("MasterAccountGroup", self._build_master_account_group)
        self.main_factory.register_builder("MasterDepartment", self._build_master_department)
        self.main_factory.register_builder("MasterTransactionType", self._build_master_transaction_type)
        self.main_factory.register_builder("MasterAccount", self._build_master_account)
        self.main_factory.register_builder("MasterProvince", self._build_master_province)
        ## TAMBAHKAN BUILDER BARU UNTUK MASTER DATA
        self.main_factory.register_builder("MasterCustomerGroup", self._build_master_customer_group)
        self.main_factory.register_builder("MasterPriceListType", self._build_master_price_list_type)
        self.main_factory.register_builder("MasterSalesArea1", self._build_master_sales_area1)
        self.main_factory.register_builder("MasterSalesArea2", self._build_master_sales_area2)
        self.main_factory.register_builder("MasterSalesArea3", self._build_master_sales_area3)
        self.main_factory.register_builder("MasterCustomer", self._build_master_customer)
        self.main_factory.register_builder("MasterUnit", self._build_master_unit)
        self.main_factory.register_builder("MasterMaterialGroup1", self._build_master_material_group1)
        self.main_factory.register_builder("MasterMaterialGroup2", self._build_master_material_group2)
        self.main_factory.register_builder("MasterMaterialGroup3", self._build_master_material_group3)
        self.main_factory.register_builder("MasterMaterialType", self._build_master_material_type)
        self.main_factory.register_builder("MasterMaterial", self._build_master_material)
        self.main_factory.register_builder("MasterLocation", self._build_master_location)
        self.main_factory.register_builder("MasterBank", self._build_master_bank)
        self.main_factory.register_builder("MasterCollector", self._build_master_collector)
        self.main_factory.register_builder("MasterCustomerPartner", self._build_master_customer_partner)
        self.main_factory.register_builder("MasterUnitConversion", self._build_master_unit_conversion)
        #sales builders
        self.main_factory.register_builder("MasterEmployeeH", self._build_master_employee_h)
        self.main_factory.register_builder("MasterSales", self._build_master_sales)

    def _build_master_country(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterCountry(
            Code=params.get("Code", self.main_factory.get_unique_value("C", 2)),
            Name=params.get("Name", "Country " + self.main_factory.get_unique_value("N")),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    def _build_master_province(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        country = params.get('mastercountry') # Dependensi otomatis
        return db_models.MasterProvince(
            Country=country.Code,
            Code=params.get("Code", self.main_factory.get_unique_value("P", 20)),
            Name=params.get("Name", "Province " + self.main_factory.get_unique_value("N")),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    def _build_master_city(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        province = params.get('masterprovince') 
        
        # Tambahkan pengecekan untuk keamanan
        if not province:
            raise ValueError("Gagal membuat MasterCity: dependensi MasterProvince tidak ditemukan/dibuat.")

        return db_models.MasterCity(
            Country=province.Country, # Ambil country dari province
            Province=province.Code,
            City=params.get("City", self.main_factory.get_unique_value("C", 20)),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_currency(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterCurrency(
            Code=params.get("Code", self.main_factory.get_unique_value("C", 3)),
            Name=params.get("Name", "Currency " + self.main_factory.get_unique_value("N")),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    # TAMBAHKAN FUNGSI-FUNGSI BUILDER BARU
    def _build_master_account_group(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterAccountGroup(
            # PERBAIKAN: Gunakan get_unique_value dengan prefix 2 huruf dan panjang 5
            Code=params.get("Code", self.main_factory.get_unique_value("AG", 3)),
            Name=params.get("Name", "Account Group " + self.main_factory.get_unique_value("N")),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_department(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterDepartment(
            Code=params.get("Code", self.main_factory.get_unique_value("D", 10)),
            Name=params.get("Name", "Department " + self.main_factory.get_unique_value("N")),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_account(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        account_group = params.get('masteraccountgroup')
        department = params.get('masterdepartment')
        currency = params.get('mastercurrency')
        
        return db_models.MasterAccount(
            AccountNo=params.get("AccountNo", self.main_factory.get_unique_value("ACC", 20)),
            Name=params.get("Name", "Account " + self.main_factory.get_unique_value("N")),
            Level=params.get("Level", 1),
            AccountGroup=account_group.Code,
            Department=department.Code,
            Currency=currency.Code,
            IsJournal=params.get("IsJournal", True),
            IsCashier=params.get("IsCashier", False),
            Users=params.get("Users", ""),
            ParentNo=params.get("ParentNo", None),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    
    def _build_master_transaction_type(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        # Kita tidak membuat MasterAccount di sini, kita berasumsi ia sudah dibuat
        # atau kita harus membuatnya. Untuk sekarang, mari kita buat default jika tidak ada.
        account = params.get('masteraccount')
        
        return db_models.MasterTransactionType(
            Type=params.get("Type", self.main_factory.get_unique_value("T", 20)),
            Description=params.get("Description", "Trans " + self.main_factory.get_unique_value("D")),
            AccountNo=account.AccountNo,
            Purpose=params.get("Purpose", ""),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    
    def _build_master_supplier(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        country = params.get('mastercountry')
        currency = params.get('mastercurrency')
        city = params.get('mastercity') 
        trans_type1 = params.get('mastertransactiontype')

        # PERBAIKAN: Buat instance kedua untuk TransactionType2 jika tidak disediakan
        # Kita bisa membuat instance baru atau me-reuse yang sudah ada.
        # Untuk kesederhanaan, kita buat yang baru dengan `override` berbeda.
        trans_type2 = self.main_factory.create(
            "MasterTransactionType",
            Type=self.main_factory.get_unique_value("T2", 20),
            Description="Secondary Transaction"
        )

        return db_models.MasterSupplier(
            Code=params.get('Code', self.main_factory.get_unique_value("S", 10)),
            Name=params.get('Name', "Supplier " + self.main_factory.get_unique_value("N")),
            Country=country.Code,
            Currency=currency.Code,
            City=city.City,
            Province=city.Province,
            TransactionType=trans_type1.Type, 
            TransactionType2=trans_type2.Type, # Gunakan .Type dari instance yang valid
            Address=params.get('Address', 'Default Address'),
            Address2=params.get('Address2', ''),
            Phone=params.get('Phone', ''),
            Fax=params.get('Fax', ''),
            Email=params.get('Email', ''),
            Contact=params.get('Contact', ''),
            Mobile=params.get('Mobile', ''),
            TaxNumber=params.get('TaxNumber', ''),
            TOP=params.get('TOP', 0),
            Limit=params.get('Limit', Decimal('0.0')),
            CutPPh=params.get('CutPPh', False),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    def _build_master_customer_group(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterCustomerGroup(Code=params.get('Code', self.main_factory.get_unique_value('CG', 5)), Name=params.get('Name', 'Group'), CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_price_list_type(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterPriceListType(Code=params.get('Code', self.main_factory.get_unique_value('PL', 5)), Name=params.get('Name', 'Price List'), CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_sales_area1(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterSalesArea1(Code=params.get('Code', self.main_factory.get_unique_value('SA1', 10)), Name=params.get('Name', 'Area 1'), CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_sales_area2(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        area1 = params.get('mastersalesarea1')
        return db_models.MasterSalesArea2(Area1=area1.Code, Code=params.get('Code', self.main_factory.get_unique_value('SA2', 10)), Name=params.get('Name', 'Area 2'), CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_sales_area3(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        area2 = params.get('mastersalesarea2')
        return db_models.MasterSalesArea3(Area1=area2.Area1, Area2=area2.Code, Code=params.get('Code', self.main_factory.get_unique_value('SA3', 10)), Name=params.get('Name', 'Area 3'), CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_customer(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        country = params.get('mastercountry') or self.main_factory.create('MasterCountry')
        currency = params.get('mastercurrency') or self.main_factory.create('MasterCurrency')
        group = params.get('mastercustomergroup') or self.main_factory.create('MasterCustomerGroup')
        price_list = params.get('masterpricelisttype') or self.main_factory.create('MasterPriceListType')
        
        # PERBAIKAN UTAMA: Gunakan flush bertahap untuk hirarki SalesArea
        sales_area1 = self.main_factory.create("MasterSalesArea1")
        self.session.flush() # Simpan SalesArea1

        sales_area2 = self.main_factory.create("MasterSalesArea2", mastersalesarea1=sales_area1)
        self.session.flush() # Simpan SalesArea2

        sales_area3 = self.main_factory.create("MasterSalesArea3", mastersalesarea2=sales_area2)
        self.session.flush() # Simpan SalesArea3
        
        trans_type1 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))
        trans_type2 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))

        return db_models.MasterCustomer(
            Code=params.get('Code', self.main_factory.get_unique_value('C', 10)),
            Name='Customer', Country=country.Code, CustomerGroup=group.Code,
            PriceListType=price_list.Code, 
            SalesArea1=sales_area3.Area1, 
            SalesArea2=sales_area3.Area2,
            SalesArea3=sales_area3.Code, 
            Currency=currency.Code, TransactionType=trans_type1.Type,
            TransactionType2=trans_type2.Type, Address='', Address2='', City='', Phone='', Fax='', Email='',
            Contact='', Mobile='', WhatsAppSession='', WhatsAppNo='', TaxNumber='', TOP=0,
            Limit=Decimal('0.0'), CutPPh=False, IsBlacklisted=False, IsDeleted=False,
            Latitude=Decimal('0.0'), Longitude=Decimal('0.0'), Information='',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_unit(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterUnit(Code=params.get('Code', self.main_factory.get_unique_value('U', 5)), Name='Unit', CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_material_group1(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterMaterialGroup1(Code=params.get('Code', self.main_factory.get_unique_value('MG1', 10)), Name='Group 1', CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now)

    def _build_master_material_group2(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        group1 = params.get('mastermaterialgroup1')
        return db_models.MasterMaterialGroup2(
            Group1=group1.Code,
            Code=params.get('Code', self.main_factory.get_unique_value('MG2', 10)),
            Name='Group 2',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_material_group3(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        group2 = params.get('mastermaterialgroup2')
        return db_models.MasterMaterialGroup3(
            Group1=group2.Group1,
            Group2=group2.Code,
            Code=params.get('Code', self.main_factory.get_unique_value('MG3', 10)),
            Name='Group 3',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    def _build_master_material(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # Buat dependensi secara eksplisit
        smallest_unit = params.get('mastersmallestunit') or self.main_factory.create("MasterUnit")
        sold_unit = params.get('mastersoldunit') or self.main_factory.create("MasterUnit")
        sku_unit = params.get('masterskuunit') or self.main_factory.create("MasterUnit")
        
        # PERBAIKAN UTAMA: Gunakan flush bertahap
        group1 = self.main_factory.create("MasterMaterialGroup1")
        self.session.flush() # Simpan group1 ke DB

        group2 = self.main_factory.create("MasterMaterialGroup2", mastermaterialgroup1=group1)
        self.session.flush() # Simpan group2 ke DB

        group3 = self.main_factory.create("MasterMaterialGroup3", mastermaterialgroup2=group2)
        self.session.flush() # Simpan group3 ke DB
        
        m_type = params.get('mastermaterialtype') or self.main_factory.create('MasterMaterialType')
        currency = params.get('mastercurrency') or self.main_factory.create('MasterCurrency')
        tt1 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))
        tt2 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))
        tt3 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))
        tt4 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))
        tt5 = self.main_factory.create("MasterTransactionType", Type=self.main_factory.get_unique_value("T", 20))

        return db_models.MasterMaterial(
            Code=params.get('Code', self.main_factory.get_unique_value('M', 20)), Name='Material', 
            SmallestUnit=smallest_unit.Code, SoldUnit=sold_unit.Code, SKUUnit=sku_unit.Code,
            Group1=group3.Group1, 
            Group2=group3.Group2, 
            Group3=group3.Code,
            Type=m_type.Code, Currency=currency.Code, 
            TransactionType1=tt1.Type, TransactionType2=tt2.Type, TransactionType3=tt3.Type,
            TransactionType4=tt4.Type, TransactionType5=tt5.Type, NameInPO='', IsBatch=True, IsService=False, IsAsset=False, IsPPh=False,
            HS='', Barcode='', MinStock=0, MaxStock=0, DefaultPrice=0, Info='',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )
    
    def _build_master_material_type(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterMaterialType(
            Code=params.get('Code', self.main_factory.get_unique_value('MT', 5)),
            Name=params.get('Name', 'Material Type'),
            IsWaste=params.get('IsWaste', False),
            CreatedBy='test',
            CreatedDate=now,
            ChangedBy='test',
            ChangedDate=now
        )
    def _build_master_location(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        country = params.get('mastercountry') or self.main_factory.create('MasterCountry')
        
        return db_models.MasterLocation(
            Code=params.get('Code', self.main_factory.get_unique_value('L', 5)),
            Name=params.get('Name', 'Location ' + self.main_factory.get_unique_value('N')),
            Country=country.Code,
            IsWarehouseManagement=params.get('IsWarehouseManagement', False),
            IsQualityControl=params.get('IsQualityControl', False),
            VolumeCapacity=params.get('VolumeCapacity', Decimal('0')),
            Address=params.get('Address', ''),
            Address2=params.get('Address2', ''),
            City=params.get('City', ''),
            Latitude=params.get('Latitude', Decimal('0.0')),
            Longitude=params.get('Longitude', Decimal('0.0')),
            CreatedBy='test',
            CreatedDate=now,
            ChangedBy='test',
            ChangedDate=now
        )
    def _build_master_employee_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterEmployeeH(
            EmployeeNo=params.get('EmployeeNo', self.main_factory.get_unique_value('E', 10)),
            Name=params.get('Name', 'Employee ' + self.main_factory.get_unique_value('N')),
            Gender='M',
            BirthDate=now.date() - datetime.timedelta(days=365*25), # Umur 25 tahun
            Religion='Other',
            IsActive=True,
            JoinDate=now.date(),
            ResignReason='',
            Information='',
            CreatedBy='test',
            CreatedDate=now,
            ChangedBy='test',
            ChangedDate=now
        )
    def _build_master_sales(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        employee = params.get('masteremployeeh') or self.main_factory.create('MasterEmployeeH')
        
        return db_models.MasterSales(
            Code=employee.EmployeeNo, # Gunakan EmployeeNo sebagai Code
            Name=params.get('Name', employee.Name), # Ambil nama dari employee
            Address=params.get('Address', ''),
            City=params.get('City', ''),
            Phone=params.get('Phone', ''),
            Mobile=params.get('Mobile', ''),
            CreatedBy='test',
            CreatedDate=now,
            ChangedBy='test',
            ChangedDate=now
        )
    def _build_master_bank(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterBank(
            Code=params.get('Code', self.main_factory.get_unique_value('B', 5)),
            Name=params.get('Name', 'Bank Default'),
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_collector(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.MasterCollector(
            Code=params.get('Code', self.main_factory.get_unique_value('COL', 10)),
            Name=params.get('Name', 'Collector Default'),
            Address='', City='', Phone='', Mobile='',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_master_customer_partner(self, params):
        customer = params.get('main_customer') or self.main_factory.create('MasterCustomer')
        partner = params.get('partner_customer') or self.main_factory.create('MasterCustomer')
        return db_models.MasterCustomerPartner(
            CustomerCode=customer.Code,
            PartnerCode=partner.Code,
            PartnerFunc=params.get('PartnerFunc', 'SHIP_TO')
        )

    def _build_master_unit_conversion(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit')
        return db_models.MasterUnitConversion(
            MaterialCode=material.Code,
            Unit=unit.Code,
            Content=Decimal('1.0'), Weight=0, Volume=0, IsInactive=False,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )