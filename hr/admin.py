from django.contrib import admin
from .models import (
    Department,
    Position,
    Employee,
    Attendance,
    Shift,
    EmployeeShift,
    LeaveRequest,
    Payroll,
    PAYERecord,
    NSSFRecord,
    SHARecord,
    Payslip,
    PayrollSettings,
    PAYETaxBand,
)

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Shift)
admin.site.register(EmployeeShift)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
admin.site.register(PAYERecord)
admin.site.register(NSSFRecord)
admin.site.register(SHARecord)
admin.site.register(Payslip)
admin.site.register(PayrollSettings)
admin.site.register(PAYETaxBand)
