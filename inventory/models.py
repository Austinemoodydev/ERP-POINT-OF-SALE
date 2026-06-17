from django.db import models
from products.models import Product
from accounts.models import User


class Warehouse(models.Model):

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    code = models.CharField(
        max_length=50,
        unique=True
    )

    address = models.TextField()

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class InventoryLedger(models.Model):

    TRANSACTION_TYPES = [

        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('TRANSFER', 'Transfer'),
        ('ADJUSTMENT', 'Adjustment'),
        ('DAMAGED', 'Damaged'),
        ('RETURN', 'Return'),
        ('EXPIRED', 'Expired')

    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    balance_after = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reference_number = models.CharField(
        max_length=100
    )

    remarks = models.TextField(
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class WarehouseStock(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    class Meta:

        unique_together = (
            'warehouse',
            'product'
        )


class StockIn(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    reference_number = models.CharField(
        max_length=100,
        unique=True
    )

    supplier_name = models.CharField(
        max_length=255
    )

    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    received_date = models.DateTimeField(
        auto_now_add=True
    )


class StockInItem(models.Model):

    stock_in = models.ForeignKey(
        StockIn,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    cost_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class StockOut(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    reference_number = models.CharField(
        max_length=100,
        unique=True
    )

    issued_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    issued_date = models.DateTimeField(
        auto_now_add=True
    )


class StockOutItem(models.Model):

    stock_out = models.ForeignKey(
        StockOut,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class StockAdjustment(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    old_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    new_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reason = models.TextField()

    adjusted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    adjusted_at = models.DateTimeField(
        auto_now_add=True
    )


class StockTransfer(models.Model):

    transfer_number = models.CharField(
        max_length=100,
        unique=True
    )

    from_warehouse = models.ForeignKey(
        Warehouse,
        related_name='source_warehouse',
        on_delete=models.CASCADE
    )

    to_warehouse = models.ForeignKey(
        Warehouse,
        related_name='destination_warehouse',
        on_delete=models.CASCADE
    )

    transferred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    transfer_date = models.DateTimeField(
        auto_now_add=True
    )


class StockTransferItem(models.Model):

    transfer = models.ForeignKey(
        StockTransfer,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class DamagedStock(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reason = models.TextField()

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    reported_at = models.DateTimeField(
        auto_now_add=True
    )


class ReturnedStock(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reason = models.TextField()

    returned_at = models.DateTimeField(
        auto_now_add=True
    )


class ExpiredStock(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    batch_number = models.CharField(
        max_length=100
    )

    expiry_date = models.DateField()

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    disposed = models.BooleanField(
        default=False
    )


class StockTake(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    conducted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    conducted_at = models.DateTimeField(
        auto_now_add=True
    )


class StockTakeItem(models.Model):

    stock_take = models.ForeignKey(
        StockTake,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    system_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    counted_quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    variance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class CycleCount(models.Model):

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    last_count_date = models.DateField()

    next_count_date = models.DateField()

    frequency_days = models.IntegerField()

    def __str__(self):
        return f"{self.product} - {self.warehouse}"


class ProductBatch(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    batch_number = models.CharField(
        max_length=100
    )

    quantity_received = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    quantity_remaining = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    unit_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    manufacture_date = models.DateField(
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    received_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['received_date']

    def __str__(self):
        return f"{self.product} - {self.batch_number}"


class ProductSerial(models.Model):

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE
    )

    serial_number = models.CharField(
        max_length=191,
        unique=True
    )

    imei_number = models.CharField(
        max_length=191,
        blank=True
    )

    batch = models.ForeignKey(
        ProductBatch,
        on_delete=models.CASCADE,
        null=True
    )

    is_sold = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class InventoryAudit(models.Model):        # ← moved out of ProductSerial

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(
        max_length=255
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
