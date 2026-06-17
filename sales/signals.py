from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import POSSaleItem
from .services import process_sale_item


@receiver(
    post_save,
    sender=POSSaleItem
)
def reduce_inventory(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        process_sale_item(instance)
