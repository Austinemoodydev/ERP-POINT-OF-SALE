from django.db import models

# Create your models here.
from django.conf import settings


class Department(models.Model):

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class Position(models.Model):

    title = models.CharField(
        max_length=255
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Employee(models.Model):

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    employee_number = models.CharField(
        max_length=50,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True
    )

    hire_date = models.DateField()

    basic_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    clock_in = models.DateTimeField(
        null=True,
        blank=True
    )

    clock_out = models.DateTimeField(
        null=True,
        blank=True
    )

    hours_worked = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )


class Shift(models.Model):

    name = models.CharField(
        max_length=100
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    def __str__(self):
        return self.name


class EmployeeShift(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()


class LeaveRequest(models.Model):

    STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    leave_type = models.CharField(
        max_length=100
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )


class Payroll(models.Model):

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    payroll_month = models.DateField()

    basic_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    allowances = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    deductions = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    gross_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    processed = models.BooleanField(
        default=False
    )


class PAYERecord(models.Model):

    payroll = models.ForeignKey(
        Payroll,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class NSSFRecord(models.Model):

    payroll = models.ForeignKey(
        Payroll,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class SHARecord(models.Model):

    payroll = models.ForeignKey(
        Payroll,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class Payslip(models.Model):

    payroll = models.OneToOneField(
        Payroll,
        on_delete=models.CASCADE
    )

    generated_at = models.DateTimeField(
        auto_now_add=True
    )

    pdf_file = models.FileField(
        upload_to='payslips/',
        blank=True
    )


class PayrollSettings(models.Model):

    paye_enabled = models.BooleanField(
        default=True
    )

    sha_enabled = models.BooleanField(
        default=True
    )

    nssf_enabled = models.BooleanField(
        default=True
    )

    sha_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0.0275
    )

    nssf_employee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2160
    )

    nssf_employer_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2160
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


class PAYETaxBand(models.Model):

    min_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    max_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    tenant = models.ForeignKey(
        'saas.Tenant',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.min_amount}-{self.max_amount}"
