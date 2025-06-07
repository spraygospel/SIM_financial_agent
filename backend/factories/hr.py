# backend/factories/hr.py
from .base import BaseModuleFactory
from backend.app import db_models
import datetime
from decimal import Decimal

class HrFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("HrChangeShiftH", self._build_hr_change_shift_h)
        self.main_factory.register_builder("HrChangeShiftD", self._build_hr_change_shift_d)
        self.main_factory.register_builder("HrOvertimeH", self._build_hr_overtime_h)
        self.main_factory.register_builder("HrOvertimeD", self._build_hr_overtime_d)

    def _build_hr_change_shift_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.HrChangeShiftH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("CSH", 15)),
            Series='CSH', DocDate=now.date(), Information='Test Change Shift', Status='OPEN',
            IsApproved=True, PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_hr_change_shift_d(self, params):
        header = params.get('hrchangeshifth') or self.main_factory.create('HrChangeShiftH')
        employee = params.get('masteremployeeh') or self.main_factory.create('MasterEmployeeH')

        return db_models.HrChangeShiftD(
            DocNo=header.DocNo,
            EmployeeNo=employee.EmployeeNo,
            NewShift='PAGI'
        )
    
    def _build_hr_overtime_h(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        return db_models.HrOvertimeH(
            DocNo=params.get('DocNo', self.main_factory.get_unique_value("OT", 15)),
            Series='OT', DocDate=now.date(), Reason='URGENT', Information='Test Overtime',
            Status='OPEN', IsApproved=True, PrintCounter=0,
            CreatedBy='test', CreatedDate=now, ChangedBy='test', ChangedDate=now
        )

    def _build_hr_overtime_d(self, params):
        header = params.get('hrovertimeh') or self.main_factory.create('HrOvertimeH')
        employee = params.get('masteremployeeh') or self.main_factory.create('MasterEmployeeH')

        return db_models.HrOvertimeD(
            DocNo=header.DocNo,
            EmployeeNo=employee.EmployeeNo,
            StartTime=datetime.time(17, 0),
            EndTime=datetime.time(18, 0),
            Duration=Decimal('1.0')
        )