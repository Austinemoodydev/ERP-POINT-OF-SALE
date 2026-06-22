from django.db.models.signals import post_save

from django.dispatch import receiver

from .models import Product

from .services.barcode_service import generate_barcode


@receiver(post_save, sender=Product)
def save_barcode(sender, instance, created, **kwargs):

    if created:

        image = generate_barcode(instance)

        instance.barcode_image.save(



            image.name,

            image,

            save=False

        )

        instance.save()
