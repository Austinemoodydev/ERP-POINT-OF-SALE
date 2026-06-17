import requests
from .models import Webhook


def trigger_webhook(
        event,
        payload):

    hooks = Webhook.objects.filter(
        event=event,
        active=True
    )

    for hook in hooks:

        try:

            requests.post(
                hook.endpoint_url,
                json=payload,
                timeout=10
            )

        except Exception:
            pass
