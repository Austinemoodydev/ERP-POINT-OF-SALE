
from django.contrib import admin
from .models import (
    Workflow,
    WorkflowStep,
    ApprovalRequest,
    ApprovalHistory,
    Task,
    Document,
    DocumentVersion,
    ElectronicSignature,
    SignedDocument,
    WorkflowNode,
    SLA,
)

admin.site.register(Workflow)
admin.site.register(WorkflowStep)
admin.site.register(ApprovalRequest)
admin.site.register(ApprovalHistory)
admin.site.register(Task)
admin.site.register(Document)
admin.site.register(DocumentVersion)
admin.site.register(ElectronicSignature)
admin.site.register(SignedDocument)
admin.site.register(WorkflowNode)
admin.site.register(SLA)
