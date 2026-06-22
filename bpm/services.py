from .models import ApprovalRequest, Workflow


def workflow_stats():
    return {
        'pending': ApprovalRequest.objects.filter(status='PENDING').count(),
        'approved': ApprovalRequest.objects.filter(status='APPROVED').count(),
        'rejected': ApprovalRequest.objects.filter(status='REJECTED').count(),
    }
