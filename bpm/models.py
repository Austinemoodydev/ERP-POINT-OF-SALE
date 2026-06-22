from django.db import models
from django.conf import settings


class Workflow(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE
    )
    step_number = models.IntegerField()
    name = models.CharField(max_length=255)
    approver_role = models.ForeignKey(
        'accounts.Role',
        on_delete=models.CASCADE
    )
    escalation_hours = models.IntegerField(default=24)

    def __str__(self):
        return self.name


class ApprovalRequest(models.Model):
    STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    current_step = models.IntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ApprovalHistory(models.Model):
    approval = models.ForeignKey(
        ApprovalRequest,
        on_delete=models.CASCADE
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    action = models.CharField(max_length=50)
    comments = models.TextField()
    approved_at = models.DateTimeField(auto_now_add=True)


class WorkflowNode(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE
    )
    node_name = models.CharField(max_length=255)
    position_x = models.IntegerField()
    position_y = models.IntegerField()


class Task(models.Model):
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class DocumentVersion(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE
    )
    version = models.IntegerField()
    file = models.FileField(upload_to='versions/')


class ElectronicSignature(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    signature = models.ImageField(upload_to='signatures/')
    signed_at = models.DateTimeField(auto_now_add=True)


class SignedDocument(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE
    )
    signature = models.ForeignKey(
        ElectronicSignature,
        on_delete=models.CASCADE
    )
    signed_at = models.DateTimeField(auto_now_add=True)


class SLA(models.Model):
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE
    )
    max_hours = models.IntegerField()
    warning_hours = models.IntegerField()
