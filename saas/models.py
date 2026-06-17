from django.db import models

# Create your models here.


class Tenant(models.Model):

    name = models.CharField(
        max_length=255
    )

    company_pin = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):

    name = models.CharField(
        max_length=100
    )

    monthly_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    max_users = models.IntegerField()

    max_branches = models.IntegerField()

    max_products = models.IntegerField()

    max_storage_gb = models.IntegerField()

    def __str__(self):
        return self.name


class TenantSubscription(models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT
    )

    start_date = models.DateField()

    end_date = models.DateField()

    active = models.BooleanField(
        default=True
    )


class TrialAccount(models.Model):

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()

    end_date = models.DateField()

    converted = models.BooleanField(
        default=False
    )


class Invoice(models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    due_date = models.DateField()

    paid = models.BooleanField(
        default=False
    )


class SubscriptionPayment(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_date = models.DateField()

    transaction_reference = models.CharField(
        max_length=100
    )


class UsageTracking(models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    current_users = models.IntegerField(
        default=0
    )

    current_products = models.IntegerField(
        default=0
    )

    current_branches = models.IntegerField(
        default=0
    )

    storage_used_gb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


class TenantDomain(models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE
    )

    domain = models.CharField(
        max_length=191,
        unique=True
    )

    active = models.BooleanField(
        default=True
    )
