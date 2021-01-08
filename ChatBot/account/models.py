from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import settings


class Profiles(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nickname = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.nickname


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='post')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.nickname


class Comment(models.Model):
    post = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='posts')
    posted = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {}' .format(self.post)


class Likes(models.Model):
    like_to = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='pasted_to')
    liked_from = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='pasted_from')
    liked = models.BooleanField(default=False)

    def __str__(self):
        return '{} Photo is liked by {}' .format(self.like_to, self.liked_from)
