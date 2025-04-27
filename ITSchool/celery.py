import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITSchool.settings')

app = Celery('ITSchool')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()