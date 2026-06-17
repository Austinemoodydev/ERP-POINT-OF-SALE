from django.db import models
from django.conf import settings


class ETIMSSettings(models.Model):
    company_pin = models.CharField(max_length=50)
    device_serial = models.CharField(max_length=100)
    api_url = models.URLField()
    api_key = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_pin


class ElectronicInvoice(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUBMITTED', 'Submitted'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )

    invoice_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    invoice_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    etims_invoice_number = models.CharField(
        max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number


class VATRate(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class VATTransaction(models.Model):
    reference = models.CharField(max_length=100)
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateField()
    branch = models.ForeignKey(
        'core.Branch', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.reference


class WithholdingTax(models.Model):
    reference = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=255)
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateField()

    def __str__(self):
        return self.reference


class TaxLedger(models.Model):
    TAX_TYPES = (
        ('VAT', 'VAT'),
        ('WHT', 'Withholding Tax'),
        ('PAYE', 'PAYE'),
        ('SHA', 'SHA'),
        ('NSSF', 'NSSF'),
    )

    tax_type = models.CharField(max_length=20, choices=TAX_TYPES)
    reference = models.CharField(max_length=100)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transaction_date = models.DateField()
    branch = models.ForeignKey(
        'core.Branch', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.tax_type} - {self.reference}"


class TaxReturn(models.Model):
    RETURN_TYPES = (
        ('VAT', 'VAT'),
        ('PAYE', 'PAYE'),
        ('WHT', 'WHT'),
    )

    return_type = models.CharField(max_length=20, choices=RETURN_TYPES)
    filing_period = models.CharField(max_length=20)
    total_tax = models.DecimalField(max_digits=15, decimal_places=2)
    filed = models.BooleanField(default=False)
    filed_at = models.DateTimeField(null=True, blank=True)


class AuditTrail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    record_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)


class DataChangeLog(models.Model):
    model_name = models.CharField(max_length=255)
    record_id = models.CharField(max_length=100)
    field_name = models.CharField(max_length=255)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class SecurityLog(models.Model):
    EVENT_TYPES = (
        ('LOGIN', 'Login'),
        ('FAILED_LOGIN', 'Failed Login'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('LOCKOUT', 'Account Lockout'),
        ('PERMISSION_CHANGE', 'Permission Change'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
