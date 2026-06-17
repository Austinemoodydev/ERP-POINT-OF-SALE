from django.db import models


class CustomerGroup(models.Model):

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name


class LoyaltyAccount(models.Model):

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE
    )

    customer = models.OneToOneField(
        'sales.Customer',
        on_delete=models.CASCADE
    )

    points = models.IntegerField(
        default=0
    )


class LoyaltyTransaction(models.Model):

    loyalty_account = models.ForeignKey(
        LoyaltyAccount,
        on_delete=models.CASCADE
    )

    points = models.IntegerField()

    transaction_type = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Reward(models.Model):          # ← moved out of LoyaltyTransaction

    name = models.CharField(
        max_length=255
    )

    points_required = models.IntegerField()

    description = models.TextField()

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Promotion(models.Model):

    name = models.CharField(
        max_length=255
    )

    start_date = models.DateField()

    end_date = models.DateField()

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    active = models.BooleanField(
        default=True
    )


class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    expiry_date = models.DateField()

    usage_limit = models.IntegerField(
        default=1
    )

    used_count = models.IntegerField(
        default=0
    )


class SMSCampaign(models.Model):

    name = models.CharField(
        max_length=255
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    sent = models.BooleanField(
        default=False
    )


class EmailCampaign(models.Model):

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    sent = models.BooleanField(
        default=False
    )


class WhatsAppMessage(models.Model):

    customer = models.ForeignKey(
        'sales.Customer',
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(
        max_length=50
    )

    message = models.TextField()

    status = models.CharField(
        max_length=50,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class CustomerFeedback(models.Model):

    customer = models.ForeignKey(
        'sales.Customer',
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comments = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class SupportTicket(models.Model):

    STATUS = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed')
    )

    customer = models.ForeignKey(
        'sales.Customer',
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE
    )

    subject = models.CharField(
        max_length=255
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='OPEN'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
