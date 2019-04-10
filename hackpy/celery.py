from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
import os
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackpy.settings')

app = Celery('hackpy')

app.config_from_object(settings.CELERY)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)