import uuid
from django.db import models

# Create your models here.


class APIKey(models.Model):

    name = models.CharField(
        max_length=255
    )

    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Webhook(models.Model):

    EVENTS = (

        ('SALE_CREATED', 'Sale Created'),
        ('PURCHASE_CREATED', 'Purchase Created'),
        ('PAYMENT_RECEIVED', 'Payment Received'),
        ('CUSTOMER_CREATED', 'Customer Created'),

    )

    event = models.CharField(
        max_length=50,
        choices=EVENTS
    )

    endpoint_url = models.URLField()

    active = models.BooleanField(
        default=True
    )


class ERPIntegration(models.Model):

    name = models.CharField(
        max_length=255
    )

    base_url = models.URLField()

    api_key = models.TextField()

    active = models.BooleanField(
        default=True
    )
