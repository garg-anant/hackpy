from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Index, Text

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models
from elasticsearch_dsl import *

from .utils import NewsLinksIndex

connections.create_connection()

# newslink = Index('newslinksindex')

# newslink.settings(number_of_shards=1, number_of_replicas=0)
'''
# @newslink.doc_type
class NewsLinkIndex(DocType):
	title = Text()
	# model = NewsLinks
	
	class Meta:
		index = 'newslinksindex'
		model = NewsLinks
		# fields = ['title']

def bulk_indexing():
	NewsLinkIndex.init()
	es = Elasticsearch()
	bulk(client=es, actions=(b.indexing() for b in NewsLinks.objects.all().iterator()))
'''

def bulk_indexing():
	NewsLinksIndex.init()
	es = Elasticsearch()
	bulk(client=es, actions=(b.indexing() for b in models.NewsLinks.objects.all().iterator()))