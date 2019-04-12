from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class ProfileUser(AbstractUser):
	username = models.CharField(max_length=100, unique=True)

	# REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.email

class NewsLinks(models.Model):
	title = models.CharField(max_length=300)
	posted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, null=True, blank=True)
	title_link = models.URLField(max_length=400)
	num_comments = models.PositiveIntegerField(default=0, null=True, blank=True)
	hackernews_post_id = models.PositiveIntegerField(unique=True)
	# karma_points = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	karma_points = models.CharField(max_length=10, null=True, blank=True)
	time_posted = models.DateTimeField(null=True, blank=True)

	upvotes = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	downvotes = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return self.title

class comments(models.Model):
	newslink = models.ForeignKey(NewsLinks, on_delete=models.CASCADE)
	content = models.CharField(max_length=1000)
	posted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)		
	added_on = models.DateTimeField(auto_now_add=True)
	comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
	hnnews_id = models.PositiveIntegerField(blank=True, null=True)

	def __str__(self):
		return self.id