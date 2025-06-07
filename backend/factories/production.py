# backend/factories/production.py
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal

class ProductionFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("JobOrder", self._build_job_order)
        self.main_factory.register_builder("MaterialUsageH", self._build_material_usage_h)
        self.main_factory.register_builder("MaterialUsageD", self._build_material_usage_d)
        self.main_factory.register_builder("JobResultH", self._build_job_result_h)
        self.main_factory.register_builder("JobResultD", self._build_job_result_d)

    def _build_job_order(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')
        # PERBAIKAN: Minta MasterUnit secara langsung dari factory
        unit = params.get('masterunit') or self.main_factory.create('MasterUnit', Code=material.SmallestUnit)
        location = params.get('masterlocation') or self.main_factory.create('MasterLocation')
        sales_order = params.get('salesorderh') or self.main_factory.create('SalesOrderH')
        
        return db_models.JobOrder(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("JO", 15)),
            Series='JO', PlannedStartDate=now.date(), PlannedFinishDate=now.date(),
            ActualStartDate=now.date(), ActualStartTime=now.time(), ActualFinishDate=now.date(),
            ActualFinishTime=now.time(), RequiredDate=now.date(), SODocNo=sales_order.DocNo,
            IODocNo='', WODocNo='', ParentJODocNo='', Level=1, Priority=1, Location=location.Code,
            Department='', ExcludeCostDistribution=False, Formula='', MaterialCode=material.Code,
            Unit=unit.Code, QtyTarget=Decimal('1.0'), QtyOutput=Decimal('0.0'), CheckQtyOutput=False,
            TotalCost=Decimal('0.0'), Status='OPEN', Information='Test Job Order',
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_material_usage_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        job_order = params.get('joborder') or self.main_factory.create('JobOrder')
        location = job_order.location_ref
        
        return db_models.MaterialUsageH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("MU", 15)),
            Series='MU', DocDate=now.date(), DocTime=now.time(), JODocNo=job_order.DocNo,
            Location=location.Code, Machine='', Information='Test Material Usage', Status='OPEN',
            TotalCost=Decimal('0.0'), PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_material_usage_d(self, params):
        header = params.get('materialusageh') or self.main_factory.create('MaterialUsageH')
        material = params.get('mastermaterial') or self.main_factory.create('MasterMaterial')

        return db_models.MaterialUsageD(
            DocNo=header.DocNo,
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=material.SmallestUnit,
            Qty=Decimal('1.0'), BaseQty=Decimal('1.0'), Cost=Decimal('0.0')
        )

    def _build_job_result_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        job_order = params.get('joborder') or self.main_factory.create('JobOrder')
        location = job_order.location_ref

        return db_models.JobResultH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("JR", 15)),
            Series='JR', DocDate=now.date(), DocTime=now.time(), JODocNo=job_order.DocNo,
            Location=location.Code, Machine='', Information='Test Job Result', Status='OPEN',
            PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_job_result_d(self, params):
        header = params.get('jobresulth') or self.main_factory.create('JobResultH')
        
        # PERBAIKAN: Ambil material dari JobOrder yang ada di header, bukan dari relasi langsung
        if not header.job_order_ref:
             # Jika relasi belum terbentuk, query dari DB menggunakan JODocNo
             job_order = self.session.query(db_models.JobOrder).filter_by(DocNo=header.JODocNo).one()
        else:
             job_order = header.job_order_ref

        material = job_order.material_ref
        unit = material.smallest_unit_ref

        return db_models.JobResultD(
            DocNo=header.DocNo,
            MaterialCode=material.Code,
            TagNo=params.get('TagNo', self.main_factory.get_unique_value('T', 10)),
            Unit=unit.Code,
            Info='', BatchNo='', BatchInfo='', Qty=Decimal('1.0'),
            COGM=Decimal('0.0'), Cost=Decimal('0.0')
        )