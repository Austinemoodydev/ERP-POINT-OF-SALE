import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'poserp.settings')  # ← was config.settings

app = Celery('poserp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
