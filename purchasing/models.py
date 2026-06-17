from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


# Create your models here.


class Supplier(models.Model):

    name = models.CharField(
        max_length=255
    )

    supplier_code = models.CharField(
        max_length=50,
        unique=True
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        blank=True
    )

    kra_pin = models.CharField(
        max_length=50,
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

    payment_terms = models.IntegerField(
        default=30
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class PurchaseRequisition(models.Model):

    STATUS = [

        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')

    ]

    requisition_no = models.CharField(
        max_length=50,
        unique=True
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='DRAFT'
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class PurchaseRequisitionItem(models.Model):

    requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class PurchaseOrder(models.Model):

    STATUS = [

        ('DRAFT', 'Draft'),
        ('APPROVED', 'Approved'),
        ('PARTIAL', 'Partial'),
        ('RECEIVED', 'Received'),
        ('CLOSED', 'Closed')

    ]

    po_number = models.CharField(
        max_length=50,
        unique=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT
    )

    requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='DRAFT'
    )

    order_date = models.DateField()

    expected_date = models.DateField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class PurchaseOrderItem(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    unit_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    received_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )


class PurchaseApproval(models.Model):

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    approved_at = models.DateTimeField(
        auto_now_add=True
    )

    comments = models.TextField(
        blank=True
    )


class GoodsReceivedNote(models.Model):

    grn_number = models.CharField(
        max_length=50,
        unique=True
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.PROTECT
    )

    warehouse = models.ForeignKey(
        'inventory.Warehouse',
        on_delete=models.PROTECT
    )

    received_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    received_date = models.DateTimeField(
        auto_now_add=True
    )


class GoodsReceivedItem(models.Model):

    grn = models.ForeignKey(
        GoodsReceivedNote,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    batch_number = models.CharField(
        max_length=100
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    unit_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class SupplierInvoice(models.Model):

    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.PROTECT
    )

    invoice_date = models.DateField()

    due_date = models.DateField()

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    is_paid = models.BooleanField(
        default=False
    )


class SupplierLedger(models.Model):

    supplier = models.ForeignKey(
        Supplier,
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

    tenant = models.ForeignKey(
        'saas.Tenant',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
