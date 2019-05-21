from django.contrib import admin
from .models import TweeterUser, Tweet

admin.site.register(TweeterUser)
admin.site.register(Tweet)
