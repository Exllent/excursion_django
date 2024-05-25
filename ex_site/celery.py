import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ex_site.settings")
app = Celery("ex_site")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
