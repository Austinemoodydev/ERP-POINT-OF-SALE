from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StockInItem


@receiver(
    post_save,
    sender=StockInItem
)
def stock_received(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        print(
            "Stock Received"
        )
