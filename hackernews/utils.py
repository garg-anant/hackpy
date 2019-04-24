from elasticsearch_dsl import DocType, Text

class NewsLinksIndex(DocType):
	title = Text()

	class Meta:
		index = 'news-links-index'