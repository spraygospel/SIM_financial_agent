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
        self.main_factory.register_builder("HrAttendance", self._build_hr_attendance)
        self.main_factory.register_builder("HrPayroll", self._build_hr_payroll)

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
    def _build_hr_attendance(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        employee = params.get('masteremployeeh') or self.main_factory.create('MasterEmployeeH')
        return db_models.HrAttendance(
            AttendanceDate=now.date(),
            EmployeeNo=employee.EmployeeNo,
            Shift='PAGI', WorkingDuration=8, Break1Duration=1, Break2Duration=0,
            NettoWorkingDuration=7, StartEarlyMinute=0, StartLateMinute=0,
            EndEarlyMinute=0, EndLateMinute=0, Overtime=0, IsValid=True,
            DocNo='', Problem='', CreatedBy='test', CreatedDate=now
        )

    def _build_hr_payroll(self, params):
        now = datetime.datetime.now(datetime.timezone.utc)
        employee = params.get('masteremployeeh') or self.main_factory.create('MasterEmployeeH')
        return db_models.HrPayroll(
            PayrollDate=now.date().replace(day=1),
            RootComponent='GAJI',
            EmployeeNo=employee.EmployeeNo,
            Component='GAJI_POKOK',
            IsFinal=True,
            Value=Decimal('5000000'),
            CreatedBy='test',
            CreatedDate=now
        )