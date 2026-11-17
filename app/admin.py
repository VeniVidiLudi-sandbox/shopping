from django.contrib import admin

from .models import Heartbeat, Item, Profile

admin.site.register(Profile)
admin.site.register(Heartbeat)
admin.site.register(Item)
