from .models import ApprovalHistory


def approve(request, user):

    ApprovalHistory.objects.create(


        approval=request,


        approved_by=user,


        action='APPROVED'

    )

    request.status = 'APPROVED'

    request.save()
