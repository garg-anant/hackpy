from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .utils import NewsLinksIndex

import django.db.models.options as options
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
	'es_index_name', 'es_type_name', 'es_mapping'
)

# Create your models here.


class ProfileUser(AbstractUser):
	username = models.CharField(max_length=100, unique=True)

	# REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username

class NewsLinks(models.Model):
	title = models.CharField(max_length=300, null=True, blank=True)
	posted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, null=True, blank=True)
	title_link = models.URLField(max_length=400, null=True, blank=True)
	base_url = models.URLField(max_length=100, null=True, blank=True)
	num_comments = models.PositiveIntegerField(default=0, null=True, blank=True)
	hackernews_post_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
	# karma_points = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	karma_points = models.CharField(max_length=15, null=True, blank=True)
	time_posted = models.DateTimeField(null=True, blank=True)

	upvotes = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	downvotes = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return '%s - %s' % (self.id, self.hackernews_post_id)

	'''
	def indexing(self):
		obj = NewsLinksIndex(meta={'id': self.id}, title=self.title)
		return obj.to_dict()
	'''
	class Meta:
		es_index_name = 'django'
		es_type_name = 'newslink'
		es_mapping = {
				'properties': {
					'newslinkindex': {
						'type': 'object',
						'properties': {
							'title': {'type': 'string', 'index': 'not_analyzed'},
						}
					},
					
				}
			}

	def es_repr(self):
		data = {}
		mapping = self._meta.es_mapping
		data['_id'] = self.pk
		'''
		for field_name in mapping['properties'].keys():
			data[field_name] = self.field_es_repr(field_name)
		'''
		data['title'] = self.title	
		return data
	'''
	def field_es_repr(self, field_name):
		config = self._meta.es_mapping['properties'][field_name]
		if hasattr(self, 'get_es_%s' % field_name):
			field_es_value = getattr(self, 'get_es_%s' % field_name)()
		else:
			if config['type'] == 'object':
				related_object = getattr(self, field_name)
				field_es_value = {}
				field_es_value['_id'] = related_object.pk
				for prop in config['properties'].keys():
					field_es_value[prop] = getattr(related_object, prop)
			else:
				field_es_value = getattr(self, field_name)
		return field_es_value
	'''


class Comments(models.Model):
	newslink = models.ForeignKey(NewsLinks, on_delete=models.CASCADE)
	content = models.CharField(max_length=10000)
	posted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)        
	added_on = models.DateTimeField(auto_now_add=True)
	comment = models.ForeignKey('Comments', null=True, blank=True, on_delete=models.CASCADE)
	hnnews_id = models.PositiveIntegerField(blank=True, null=True)
	upvotes = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return '%s' % (self.id)

class UpvotesNewslink(models.Model):
	newslink_voted = models.BooleanField(default=False)
	voted_by = models.ForeignKey(ProfileUser,on_delete=models.CASCADE)
	newslink = models.ForeignKey(NewsLinks, on_delete=models.CASCADE)

class UpvotesComment(models.Model):
	comment_voted = models.BooleanField(default=False)
	voted_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comments, on_delete=models.CASCADE) 