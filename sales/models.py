from django.db import models
from accounts.models import User
# Create your models here.


class Customer(models.Model):

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE
    )

    customer_code = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    credit_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Quotation(models.Model):

    STATUS = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
    ]

    quotation_no = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    quotation_date = models.DateField()

    valid_until = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='DRAFT'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )


class QuotationItem(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class SalesOrder(models.Model):

    STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('INVOICED', 'Invoiced'),
        ('CLOSED', 'Closed')
    ]

    order_number = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    order_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )


class SalesOrderItem(models.Model):

    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class POSSale(models.Model):

    sale_number = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.PROTECT
    )

    cashier = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    sale_date = models.DateTimeField(
        auto_now_add=True
    )


class POSSaleItem(models.Model):

    sale = models.ForeignKey(
        POSSale,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class SalesInvoice(models.Model):

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.SET_NULL,
        null=True
    )

    invoice_date = models.DateField()

    due_date = models.DateField()

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    balance_due = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    is_paid = models.BooleanField(
        default=False
    )


class CustomerLedger(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    reference = models.CharField(
        max_length=100
    )

    debit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class CustomerPayment(models.Model):

    PAYMENT_METHODS = [

        ('CASH', 'Cash'),
        ('MPESA', 'M-Pesa'),
        ('BANK', 'Bank Transfer'),
        ('CARD', 'Card'),
        ('CHEQUE', 'Cheque')

    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT
    )

    invoice = models.ForeignKey(
        SalesInvoice,
        on_delete=models.PROTECT
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )


class SalesAccountingEntry(models.Model):

    reference = models.CharField(
        max_length=100
    )

    account_name = models.CharField(
        max_length=255
    )

    debit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


tenant = models.ForeignKey(
    'saas.Tenant',
    on_delete=models.CASCADE
)
