from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class TweeterUser(models.Model):
    name = models.TextField(max_length=30, default='no name provided')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)


class Tweet(models.Model):
    body = models.TextField(max_length=140)
    author = models.ForeignKey(TweeterUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now, editable=False)


class Notification(models.Model):
    notified = models.ForeignKey(TweeterUser, on_delete=models.DO_NOTHING)
    not_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
