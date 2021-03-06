import os
import django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('djangoProject', broker='redis://redis:6379/0')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

