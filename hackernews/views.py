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

		news_element = soup.find_all("tr", {'class':'athing'})

		for element in news_element:
			# print(element,'\n\n')

			#get-hn-id - completed
			
			soup_hnnews_id = BeautifulSoup(str(element),'html.parser')
			hnnews_id = soup_hnnews_id.find("tr",{'class':'athing'})
			hnnews_id = hnnews_id.get('id')
			print(hnnews_id)
			
			#top-line - completed
			'''			
			soup_top_line = BeautifulSoup(str(element),'html.parser')
			news_link = soup_top_line.find("a", {'class':'storylink'})
			print(news_link.text)
			print(news_link.get('href'))
			print(urlparse(news_link.get('href')).netloc)
			print('\n')
			'''
			#bottom-line
			next_row = element.findNext('tr')
			soup_bottom_link = BeautifulSoup(str(next_row),'html.parser')

			karma_point = soup_bottom_link.find("span",{'class':'score'})
			post_by = soup_bottom_link.find("a",{'class':'hnuser'})
			time_of_upload = soup_bottom_link.find("span",{'class':'age'})

			comments = soup_bottom_link.find_all('a',{'href':'item?id='+hnnews_id})
			if len(comments) == 2:
				if "discuss" in comments[1].text:
					print('0') # 0 comments in case of "discuss" 
				else:
					print(comments[1].text.split('\xa0')[0]) #number of comments
			else:
				print(None) #number of comments stored as None when unavailable 
			# print(comments)

			

			'''
			print(soup_bottom_link)
			print(karma_point.text)
			print(post_by.text)
			print(time_of_upload.text)
			print('\n')
			'''
		'''
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

		# print(num_comments_list)
		# print(len(num_comments_list))		

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




		'''
		ctx = {
			# 'titles' : titles,
			# 'list_news_links' : list_news_links,
		}
	return render(request, 'hackernews/home.jinja', ctx)
