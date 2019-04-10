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
#   return x + y

# @app.task
# def test(word):
#   return word

@celery.decorators.periodic_task(run_every=datetime.timedelta(hours=1))
def myfunc():
	req = requests.get("https://news.ycombinator.com/")
	soup = BeautifulSoup(req.text, 'html.parser')
	news_links = soup.find_all("a",{'class':'storylink'})
	print(type(news_links),'typeeeee')
	list_news_links = []
	
	for link in news_links[::-1]:
		list_news_links.append(str(link.get('href')))
		list_news_links.append(str(link.text))
		host_name_url = urlparse(str(link.get('href')))
		list_news_links.append(str(host_name_url.netloc))

	print('thissss is periodic_task')
	return 'periodic_task'