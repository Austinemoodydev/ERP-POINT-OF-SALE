from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Company(TimeStampedModel):

    name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=30
    )

    email = models.EmailField()

    address = models.TextField()

    kra_pin = models.CharField(
        max_length=50,
        blank=True
    )

    logo = models.ImageField(
        upload_to='company/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Branch(TimeStampedModel):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    manager_name = models.CharField(
        max_length=255,
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Notification(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class BranchUser(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE
    )

    is_default = models.BooleanField(
        default=False
    )


class BranchRole(models.Model):

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:
        unique_together = (
            'branch',
            'name'
        )

    def __str__(self):
        return f"{self.branch} - {self.name}"


class BranchTransfer(models.Model):

    STATUS = (
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('RECEIVED', 'Received')
    )

    transfer_number = models.CharField(
        max_length=50,
        unique=True
    )

    from_branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='outgoing'
    )

    to_branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name='incoming'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )

    transfer_date = models.DateField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.transfer_number


class BranchTransferItem(models.Model):

    transfer = models.ForeignKey(
        BranchTransfer,
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
