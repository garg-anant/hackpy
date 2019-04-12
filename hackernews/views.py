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
from .models import NewsLinks, ProfileUser, Comments


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
			news_rows = NewsLinks.objects.filter(hackernews_post_id=int(hnnews_id)).exists()
			if news_rows == False:
				news_add,_ = NewsLinks.objects.get_or_create(hackernews_post_id=int(hnnews_id))

				add_news_fields = NewsLinks.objects.get(hackernews_post_id=int(hnnews_id))
				#top-line - completed
				soup_top_line = BeautifulSoup(str(element),'html.parser')
				news_link = soup_top_line.find("a", {'class':'storylink'})
				add_news_fields.title = news_link.text #storing title
				add_news_fields.title_link = news_link.get('href') #storing title link
				# print(urlparse(news_link.get('href')).netloc) #getting the base_url


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
						new_hnuser,_ = ProfileUser.objects.get_or_create(username=post_by.text)
					
					profile_user_instance = ProfileUser.objects.filter(username=post_by.text).last()
					add_news_fields.posted_by = profile_user_instance #storing the foreign key of ProfileUser in NewsLink table	
				else:
					print('User is not displayed on the home page and therefore no link present')
				
				#Check and add comment only if it is diplayed on the page
				comments = soup_bottom_link.find_all('a',{'href':'item?id='+hnnews_id})
				if len(comments) == 2:
					if "discuss" in comments[1].text:
						print('0') # 0 comments in case of "discuss" 
					else:
						add_news_fields.num_comments = int(comments[1].text.split('\xa0')[0]) #storing number of comments
						
						#Getting onto the comments page
						comments_link = comments[0].get('href')
						comments_page_req = requests.get("https://news.ycombinator.com/"+comments_link)
						comments_soup = BeautifulSoup(comments_page_req.text,'html.parser')
						
						#Storing NewsLink id
						newslink_id = comments_soup.find("tr",{'class':'athing'})
						newslink_id = newslink_id.get('id')

						#Rest of the Comment information
						comment_elements = comments_soup.find_all("tr",{'class':'athing comtr'})
						
						#add here comment data from individual comments
						for comment_element in comment_elements:

							#Storing NewsLink id
							soup_comment = BeautifulSoup(str(comment_element),'html.parser')
							comment_hnnews_id = soup_comment.find("tr",{'class':'athing comtr'})
							comment_hnnews_id = comment_hnnews_id.get('id') #getting hnnews id for comment table
							comment_text = soup_comment.find("div",{'class':'comment'})
							comment_rows = Comments.objects.filter(hnnews_id=int(comment_hnnews_id)).exists()
							if comment_rows == False:

								print(newslink_id)
								newslink_obj = NewsLinks.objects.get(hackernews_post_id=newslink_id)

								post_by = soup_comment.find("a",{'class':'hnuser'})
								profile_user = ProfileUser.objects.filter(username=post_by.text).exists()
								if profile_user == False:
									new_hnuser,_ = ProfileUser.objects.get_or_create(username=post_by.text)
								else:
									pass

								profile_user_instance = ProfileUser.objects.filter(username=post_by.text).last()
								comments_add,_ = Comments.objects.get_or_create(hnnews_id=int(comment_hnnews_id),newslink=newslink_obj, posted_by=profile_user_instance)

								add_comments_fields = Comments.objects.filter(hnnews_id=int(comment_hnnews_id)).last()
								#check and register if displayed user already exists
								
								
								#storing time(comment added_on) in Comments table
								comment_added_on = soup_comment.find("a",{'href':'item?id='+comment_hnnews_id})
								if "hour" in comment_added_on.text:
									comment_posted_on = datetime.datetime.now() - datetime.timedelta(hours=int(time_of_upload.text.split(' ')[0]))
								if "minute" in comment_added_on.text:
									comment_posted_on = datetime.datetime.now() - datetime.timedelta(minutes=int(time_of_upload.text.split(' ')[0]))
								
								
								add_comments_fields.hnnews_id = int(comment_hnnews_id)

								if comment_text.text is not None:
									add_comments_fields.content = comment_text.span.text
								else:
									add_comments_fields.content = None
								
								add_comments_fields.added_on = comment_posted_on
								
								add_comments_fields.save()


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

				add_news_fields.time_posted = posted_time #storing time of post as calculated above

				add_news_fields.save()
				

	
	ctx = {}
	return render(request, 'hackernews/home.jinja', ctx)
