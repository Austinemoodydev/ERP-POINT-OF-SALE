from celery import shared_task

from .models import ApprovalRequest


@shared_task
def escalations():
    approvals = ApprovalRequest.objects.filter(status='PENDING')

    for approval in approvals:
        pass

    return True
