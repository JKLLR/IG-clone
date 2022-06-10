from django.contrib import admin

# Register your models here.

from .models import Profile, Post, Like, Subscribers, Comment, Follow

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Subscribers)
admin.site.register(Comment)
admin.site.register(Follow)