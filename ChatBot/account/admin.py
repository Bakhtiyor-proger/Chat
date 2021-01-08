from django.contrib import admin

from . models import Profiles, Message, Comment, Likes


@admin.register(Profiles)
class AdminProfile(admin.ModelAdmin):
    list_display = ['owner', 'nickname']


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['post', 'posted', 'created']


"""
@admin.register(Likes)
class AdminLike(admin.ModelAdmin):
    list_display = ['like_to', 'liked_from', 'liked']
"""



