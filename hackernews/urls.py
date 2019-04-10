from django.urls import path, include
from . import views

urlpatterns=[
	path('', views.index, name='views'),
	path('home', views.home, name='home'),
]	
