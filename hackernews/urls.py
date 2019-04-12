from django.urls import path, include
from . import views

urlpatterns=[
	path('', views.index, name='views'),
	path('home', views.home, name='home'),
	path('reply/<int:newslink_id>', views.reply, name='reply')
]	
