# crm/services.py
# Award loyalty points automatically after a sale.

from .models import (
    LoyaltyAccount,
    LoyaltyTransaction
)


def award_points(customer, amount):

    points = int(amount / 100)

    account, _ = LoyaltyAccount.objects.get_or_create(
        customer=customer
    )

    account.points += points
    account.save()

    LoyaltyTransaction.objects.create(
        loyalty_account=account,
        points=points,
        transaction_type='EARN'
    )
