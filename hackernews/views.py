from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# from .tasks import test, return_5, myfunc
from .tasks import myfunc
from .models import NewsLinks


# Create your views here.

def index(request):
	# myfunc.delay()
	# test.delay('hello world!')
	# return_5.delay()

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('home'))

	return render(request, 'hackernews/login.jinja' ,{})

def home(request):
	if not request.user.is_authenticated:
		return render(request, 'hackernews/login.jinja', {})
	else:
		req = requests.get("https://news.ycombinator.com/")
		soup = BeautifulSoup(req.text, 'html.parser')
		
		news_links = soup.find_all("a",{'class':'storylink'})
		karma_points = soup.find_all("span",{'class':'score'})
		# print(karma_points)
		posts_by = soup.find_all("a",{'class':'hnuser'})
		# print(posts_by)
		time_of_uploads = soup.find_all("span",{'class':'age'})
		# print(time_of_uploads)
		num_comments = soup.find_all("a")
		num_comments_list = []
		for comment in num_comments:
			if "comment" in comment.text:
				num_comments_list.append(comment.text.split("\xa0")[0])
			if "discuss" in comment.text:
				num_comments_list.append(0)
		num_comments_list.pop(0)
		
		for i in num_comments_list:
			print(type(i))		
		print(num_comments_list)
		print(len(num_comments_list))		

		list_news_links = []
		
		for link in news_links[::-1]:
			list_news_links.append(str(link.get('href')))
			list_news_links.append(str(link.text))
			host_name_url = urlparse(str(link.get('href')))
			list_news_links.append(str(host_name_url.netloc))

		for karma_point in karma_points[::-1]:
			# print(str(karma_point.text))
			print('\n')

		for post_by in posts_by[::-1]:
			print(str(post_by.text))

		for time_of_upload in time_of_uploads[::-1]:
			print(str(time_of_upload.text))





		ctx = {
			# 'titles' : titles,
			'list_news_links' : list_news_links,
		}
	return render(request, 'hackernews/home.jinja', ctx)
