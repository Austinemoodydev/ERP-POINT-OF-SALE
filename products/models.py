from django.db import models
from core.models import Branch
# Create your models here.


class Category(models.Model):

    name = models.CharField(
        max_length=191,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(
        max_length=191,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to='brands/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Unit(models.Model):

    name = models.CharField(
        max_length=50
    )

    abbreviation = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.abbreviation


class Product(models.Model):

    name = models.CharField(
        max_length=255
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    cost_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=16.00
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class ProductVariation(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    value = models.CharField(
        max_length=100
    )

    additional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.name} - {self.value}"


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='products/'
    )

    is_primary = models.BooleanField(
        default=False
    )


class ProductLocation(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    aisle = models.CharField(
        max_length=50,
        blank=True
    )

    shelf = models.CharField(
        max_length=50,
        blank=True
    )

    bin_number = models.CharField(
        max_length=50,
        blank=True
    )


class StockLevel(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    minimum_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    maximum_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    reorder_level = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )


tenant = models.ForeignKey(
    'saas.Tenant',
    on_delete=models.CASCADE
)
