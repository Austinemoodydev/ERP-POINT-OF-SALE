from celery import shared_task  # ← ADD THIS
from integrations.email_services import send_email    # ← ADD THIS
from integrations.sms_services import send_sms        # ← ADD THIS
from integrations.whatsapp import send_whatsapp    # ← ADD THIS


@shared_task
def queue_email(subject, message, recipient):
    send_email(subject, message, recipient)


@shared_task
def queue_sms(phone, message):
    send_sms(phone, message)


@shared_task
def queue_whatsapp(phone, message):
    send_whatsapp(phone, message)
