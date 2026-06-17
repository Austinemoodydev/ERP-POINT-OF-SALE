from decimal import Decimal
from .models import VATRate


def calculate_vat(amount):

    vat_rate = VATRate.objects.filter(
        active=True
    ).first()

    if not vat_rate:
        return Decimal('0')

    return (
        amount *
        vat_rate.percentage
    ) / Decimal('100')
