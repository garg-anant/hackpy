from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class ProfileUser(AbstractUser):
	email = models.CharField(max_length=100, unique=True)

	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.email

class NewsLinks(models.Model):
	title = models.CharField(max_length=300)
	posted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
	title_link = models.URLField(max_length=400)
	num_comments = models.PositiveIntegerField(default=0)
	hackernews_post_id = models.PositiveIntegerField(unique=True)
	upvotes = models.PositiveSmallIntegerField(default=0)
	downvotes = models.PositiveSmallIntegerField(default=0)
	karma_points = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.title

class comments(models.Model):
	newslink = models.ForeignKey(NewsLinks, on_delete=models.CASCADE)
	content = models.CharField(max_length=1000)
	posted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)		
	added_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.id