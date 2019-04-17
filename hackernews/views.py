from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime

# from .tasks import test, return_5, myfunc
from .tasks import myfunc
from .models import NewsLinks, ProfileUser, Comments, UpvotesNewslink, UpvotesComment
from .forms import CommentForm, RegisterUser


# Create your views here.

def index(request):
	myfunc.delay()
	form = RegisterUser()
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('home'))

	return render(request, 'hackernews/login.jinja' ,{'form':form})

def comments(request, newslink_id):
	form = CommentForm()
	comments = Comments.objects.filter(newslink=newslink_id)
	newslink = NewsLinks.objects.filter(id=newslink_id).last()
	user_posted_by = ProfileUser.objects.filter(username=request.user.username).last()

	comment_votes = UpvotesComment

	if request.method=='POST':
		form = CommentForm(request.POST)
		print('entered here')
		if form.is_valid():
			form_save = form.save(commit=False)
			form_save.newslink = newslink
			form_save.posted_by = user_posted_by
			form_save.save()
			return redirect('comments', newslink_id=newslink.id)
		else:
			print(form.errors)

	ctx = {
			'comments': comments,
			'newslink': newslink,
			'form': form,
			'comment_votes': comment_votes
	}
	
	return render(request, 'hackernews/comments.jinja', ctx)

def search(request):
	text = request.GET.get('q')
	filtered_links = NewsLinks.objects.filter(title__icontains=text)
	
	ctx = {
		'filtered_links':filtered_links,
	}
	return render(request,'hackernews/search.jinja',ctx)

def create_account(request):
	form = RegisterUser(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			form_save = form.save(commit=False)
			form_save.set_password(request.POST.get('password'))
			form_save.save()
			
			return HttpResponseRedirect(reverse('index'))
			

		return render(request, 'hackernews/home.jinja', {'form':form})
	return render(request, 'hackernews/login.jinja', {'form':form})

def logout_func(request):
	logout(request)
	return HttpResponseRedirect(reverse('views'))

def vote_newslink(request):
	newslink_id = request.GET.get('newslink_id')
	newslink = NewsLinks.objects.get(id=newslink_id)
	user = request.GET.get('username')
	user = ProfileUser.objects.filter(username=user).last()
	vote_newslink,_ = UpvotesNewslink.objects.get_or_create(newslink_voted=True, voted_by=user, newslink=newslink)

	newslink.upvotes += 1
	newslink.save()

	return HttpResponse('SUCCESS')

def vote_comment(request):
	comment_id = request.GET.get('comment_id')
	comment = Comments.objects.get(id=comment_id)
	user = request.GET.get('username')
	user = ProfileUser.objects.filter(username=user).last()
	vote_comment,_ = UpvotesComment.objects.get_or_create(comment_voted=True, voted_by=user, comment=comment)

	comment.upvotes += 1
	comment.save()

	return HttpResponse('SUCCESS')	

def reply(request,comment_id):
	comment = Comments.objects.filter(id=comment_id).last()
	user_posted_by = ProfileUser.objects.filter(username=request.user.username).last()
	form = CommentForm()

	if request.method=='POST':
		form=CommentForm(request.POST)
		if form.is_valid():
			form_save = form.save(commit=False)
			form_save.newslink = comment.newslink
			form_save.posted_by = user_posted_by
			form_save.comment = comment
			form_save.save()
			return redirect('comments', newslink_id=comment.newslink.id)
		else:
			print(form.errors)

	ctx = {
		'comment':comment,
		'form': form
	}
	
	return render(request, 'hackernews/reply.jinja', ctx)

# @login_required(login_url=redirect('views'))
def home(request):
	
	ctx = {}
	
	if not request.user.is_authenticated:
		return render(request, 'hackernews/login.jinja',{})
	else:
		newslinks = NewsLinks.objects.all()
		paginator = Paginator(newslinks, 30)	
		page = request.GET.get('page')
		newslinks = paginator.get_page(page)

		newslink_votes = UpvotesNewslink

	ctx = {
	'newslinks': newslinks,
	'newslink_votes': newslink_votes,
	}
	
	return render(request, 'hackernews/home.jinja', ctx)
