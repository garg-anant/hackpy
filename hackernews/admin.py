from django.contrib import admin

from .models import ProfileUser, NewsLinks, Comments 

# Register your models here.

admin.site.register(ProfileUser)
admin.site.register(NewsLinks)
admin.site.register(Comments)
