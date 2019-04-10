from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .tasks import add


# Create your views here.

def index(request):
	add.delay(2,3)

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
		list_news_links = []
		
		for link in news_links:
			list_news_links.append(str(link.get('href')))
			list_news_links.append(str(link.text))
			host_name_url = urlparse(str(link.get('href')))
			list_news_links.append(str(host_name_url.netloc))

		print(list_news_links,'\n\n')	
		ctx = {
			# 'titles' : titles,
			'list_news_links' : list_news_links,
		}
	return render(request, 'hackernews/home.jinja', ctx)
