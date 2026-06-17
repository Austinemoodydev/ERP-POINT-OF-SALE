from inventory.services import process_stock_out
from accounting.services import post_journal_entry
from accounting.models import Account


def process_sale_item(item):          # ← closes here, no nesting

    process_stock_out(

        warehouse=item.sale.warehouse,

        product=item.product,

        qty=item.quantity,

        reference=item.sale.sale_number,

        user=item.sale.cashier

    )


def post_sales_invoice(               # ← now at top level, not inside process_sale_item
        invoice,
        user):

    receivable = Account.objects.get(  # ← fixed indentation (was one space, now 4)
        code='1100'
    )

    revenue = Account.objects.get(
        code='4000'
    )

    post_journal_entry(

        reference=invoice.invoice_number,

        description='Sales Invoice',

        posting_date=invoice.invoice_date,

        user=user,

        lines=[

            {
                'account': receivable,
                'debit': invoice.total_amount,
                'credit': 0
            },

            {
                'account': revenue,
                'debit': 0,
                'credit': invoice.total_amount
            }

        ]

    )
