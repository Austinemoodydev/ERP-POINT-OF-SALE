from celery import shared_task
from hr.models import Employee, Payslip
from hr.services import calculate_payroll


@shared_task
def process_payroll():
    employees = Employee.objects.filter(active=True)
    for emp in employees:
        calculate_payroll(emp)
