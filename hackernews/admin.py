from django.contrib import admin

from .models import ProfileUser, NewsLinks, Comments, UpvotesNewslink, UpvotesComment

# Register your models here.

admin.site.register(ProfileUser)
admin.site.register(NewsLinks)
admin.site.register(Comments)
admin.site.register(UpvotesNewslink)
admin.site.register(UpvotesComment)
