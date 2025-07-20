import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuration.settings")
app = Celery("configuration", broker=settings.CELERY_BROKER_URL)
# app = Celery("configuration")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
