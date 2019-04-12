from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime

# from .tasks import test, return_5, myfunc
from .tasks import myfunc
from .models import NewsLinks, ProfileUser


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
			#get-hn-id - completed
			soup_hnnews_id = BeautifulSoup(str(element),'html.parser')
			hnnews_id = soup_hnnews_id.find("tr",{'class':'athing'})
			hnnews_id = hnnews_id.get('id')
			print(hnnews_id)
			
			#ADD USERS ONLY IF NOT ALREADY EXISTS
			#ADD Newslinks and all related data if not already exists
			news_items = NewsLinks.objects.filter(hackernews_post_id=int(hnnews_id)).exists()
			if news_items == False:
				print('news does not exists..')
				news_add,_ = NewsLinks.objects.get_or_create(hackernews_post_id=int(hnnews_id))

				add_news_fields = NewsLinks.objects.get(hackernews_post_id=int(hnnews_id))
				#top-line - completed
				soup_top_line = BeautifulSoup(str(element),'html.parser')
				news_link = soup_top_line.find("a", {'class':'storylink'})
				# print(news_link.text)
				add_news_fields.title = news_link.text #storing title
				# print(news_link.get('href'))
				add_news_fields.title_link = news_link.get('href') #storing title link
				# print(urlparse(news_link.get('href')).netloc)
				# print('\n')


				#bottom-line - completed
				next_row = element.findNext('tr') #Getting the soup element of bottom row
				soup_bottom_link = BeautifulSoup(str(next_row),'html.parser')

				karma_point = soup_bottom_link.find("span",{'class':'score'})
				post_by = soup_bottom_link.find("a",{'class':'hnuser'})
				time_of_upload = soup_bottom_link.find("span",{'class':'age'})

				#check if the user is  displayed on page and accordingly register his/her profile
				users = soup_bottom_link.find("a",{'class':'hnuser'})
				if users is not None:
					#check and register if displayed user already exists
					profile_user = ProfileUser.objects.filter(username=post_by.text).exists()
					if profile_user == False:
						print('user does not exist..')
						new_hnuser,_ = ProfileUser.objects.get_or_create(username=post_by.text)
						print('user registered')
					else:
						print('user exists')
						pass
				else:
					print('User is not displayed on the home page and therefore no link present')
				#Check and add comment only if it is diplayed on the page
				comments = soup_bottom_link.find_all('a',{'href':'item?id='+hnnews_id})
				if len(comments) == 2:
					if "discuss" in comments[1].text:
						print('0') # 0 comments in case of "discuss" 
					else:
						print(comments[1].text.split('\xa0')[0]) #number of comments
						#Getting onto the comments page
						comments_link = comments[0].get('href')
						comments_page_req = requests.get("https://news.ycombinator.com/"+comments_link)
						print(comments_page_req) #to check if comments page is loading or not

						comments_soup = BeautifulSoup(comments_page_req.text,'html.parser')


				else:
					print(None) #number of comments stored as None when unavailable 

				#storing time
				if "hour" in time_of_upload.text:
					posted_time = datetime.datetime.now() - datetime.timedelta(hours=int(time_of_upload.text.split(' ')[0]))
				if "minute" in time_of_upload.text:
					posted_time = datetime.datetime.now() - datetime.timedelta(minutes=int(time_of_upload.text.split(' ')[0]))

				
				# print(soup_bottom_link)

				karma_points_check = soup_bottom_link.find('span',{'class':'score'})
				if karma_points_check is not None:
					#check and add data in karma_points if displayed user's karma points already exists
					# print(karma_point.text)
					add_news_fields.karma_points = karma_point.text #storing karma points
				
				print(post_by.text)
				print(time_of_upload.text)
				add_news_fields.time_posted = posted_time #storing time of post as calculated above
				print('\n')

				add_news_fields.save()
				


	
	ctx = {}
	return render(request, 'hackernews/home.jinja', ctx)
