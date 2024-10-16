import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("wb_app")
# Используйте Redis в качестве брокера сообщений
app.conf.broker_url = 'redis://localhost:6379/0'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)