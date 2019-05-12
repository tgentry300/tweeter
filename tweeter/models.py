from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class TweeterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Tweet(models.Model):
    body = models.TextField(max_length=140)
    username = models.OneToOneField(TweeterUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now, editable=False)


# class Notification(models.Model):
#     notified_user = models.OneToOneField(TweeterUser, on_delete=models.DO_NOTHING)
    # notifying_user = models.ForeignKey(TweeterUser, on_delete=models.DO_NOTHING)
