from django.contrib import admin

from .models import Heartbeat, Profile

admin.site.register(Profile)
admin.site.register(Heartbeat)
