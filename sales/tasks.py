from celery import shared_task
from sales.models import SalesInvoice          # ← use SalesInvoice
from integrations.sms_services import send_sms
from django.utils import timezone


@shared_task
def debt_reminders():
    today = timezone.now().date()
    overdue_invoices = SalesInvoice.objects.filter(
        due_date__lt=today,     # due date has passed
        balance_due__gt=0       # still has outstanding balance
    )
    for invoice in overdue_invoices:
        send_sms(
            invoice.customer.phone,
            f"Reminder: Invoice #{invoice.id} of KES {invoice.balance_due} is overdue."
        )
