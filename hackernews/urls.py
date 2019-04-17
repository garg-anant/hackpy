from django.urls import path, include
from . import views

urlpatterns=[
	path('', views.index, name='views'),
	path('create_account', views.create_account, name='create_account'),
	path('home', views.home, name='home'),
	path('comments/<int:newslink_id>', views.comments, name='comments'),
	path('logout', views.logout_func, name='logout'),
	path('reply/<int:comment_id>', views.reply, name='reply'),
	path('search', views.search, name='search'),

	#Ajax Vote Newslink 
	path('vote_newslink', views.vote_newslink, name='vote_newslink'),
	#Ajax Vote Comment
	path('vote_comment', views.vote_comment, name='vote_comment'),
]	
