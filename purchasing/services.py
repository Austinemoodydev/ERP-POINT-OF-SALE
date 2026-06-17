from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.services import process_stock_in
from accounting.services import post_journal_entry
from accounting.models import Account

from .models import GoodsReceivedItem


def receive_goods(grn_item, user):

    process_stock_in(

        warehouse=grn_item.grn.warehouse,

        product=grn_item.product,

        qty=grn_item.quantity,

        cost=grn_item.unit_cost,

        batch_number=grn_item.batch_number,

        user=user

    )


@receiver(          # ← moved outside receive_goods, now at top level
    post_save,
    sender=GoodsReceivedItem
)
def grn_inventory_update(
        sender,
        instance,
        created,
        **kwargs):

    if created:

        receive_goods(
            instance,
            instance.grn.received_by
        )


def post_purchase_invoice(
        supplier_invoice,
        user):

    inventory = Account.objects.get(
        code='1200'
    )

    payable = Account.objects.get(
        code='2000'
    )

    post_journal_entry(

        reference=supplier_invoice.invoice_number,

        description='Purchase Invoice',

        posting_date=supplier_invoice.invoice_date,

        user=user,

        lines=[

            {
                'account': inventory,
                'debit': supplier_invoice.total_amount,
                'credit': 0
            },

            {
                'account': payable,
                'debit': 0,
                'credit': supplier_invoice.total_amount
            }

        ]

    )
