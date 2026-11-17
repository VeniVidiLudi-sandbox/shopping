from django.shortcuts import render

from .middleware import HealthMiddleware
from .models import Heartbeat

# /health is answered by HealthMiddleware; this is only for the URL name.
health = HealthMiddleware(lambda request: None)


def home(request):
    return render(request, "app/home.html", {"last_heartbeat": Heartbeat.objects.first()})
