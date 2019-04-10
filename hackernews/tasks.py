from hackpy.celery import app
import celery
from celery import shared_task, task, Celery
from celery.schedules import crontab
from celery.decorators import periodic_task
from celery import task


from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import datetime

# @periodic_task(run_every=(crontab(minute="*")))
# def return_5():
#     print('hello world return func')
#     return 5

# @shared_task
# def add(x,y):
# 	return x + y

# @app.task
# def test(word):
# 	return word

@celery.decorators.periodic_task(run_every=datetime.timedelta(hours=1))
def myfunc():
    print('thissss is periodic_task')
    return 'periodic_task'