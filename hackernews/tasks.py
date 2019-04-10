from hackpy.celery import app
from celery import shared_task, task
from celery.schedules import crontab

from bs4 import BeautifulSoup
from urllib.parse import urlparse

@shared_task
def add(x,y):
	return x + y
