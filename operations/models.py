from django.db import models

# Create your models here.
from django.conf import settings


class Conversation(models.Model):

    title = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_messages'
    )

    body = models.TextField()

    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    read = models.BooleanField(
        default=False
    )


class Notification(models.Model):

    TYPES = (
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Success')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_notifications'
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=TYPES
    )

    read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class WorkTask(models.Model):

    title = models.CharField(
        max_length=255
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_tasks'
    )

    due_date = models.DateField()

    completed = models.BooleanField(
        default=False
    )


class CalendarEvent(models.Model):

    title = models.CharField(
        max_length=255
    )

    start = models.DateTimeField()

    end = models.DateTimeField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_calendar_events'
    )


class Meeting(models.Model):

    subject = models.CharField(
        max_length=255
    )

    scheduled_for = models.DateTimeField()

    location = models.CharField(
        max_length=255
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='operations_meetings'
    )

# --- append to operations/models.py ---


class FeatureFlag(models.Model):

    name = models.CharField(
        max_length=255
    )

    enabled = models.BooleanField(
        default=True
    )


class ErrorLog(models.Model):

    message = models.TextField()

    stack_trace = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class BackgroundJob(models.Model):

    task_name = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=50
    )

    started = models.DateTimeField()

    finished = models.DateTimeField(
        null=True
    )


class Metric(models.Model):

    name = models.CharField(
        max_length=255
    )

    value = models.FloatField()

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )


class ArchivedRecord(models.Model):

    model_name = models.CharField(
        max_length=255
    )

    record_id = models.IntegerField()

    archived_at = models.DateTimeField(
        auto_now_add=True
    )


class RetentionPolicy(models.Model):

    model_name = models.CharField(
        max_length=255
    )

    days = models.IntegerField()
