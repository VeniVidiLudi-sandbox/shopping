from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Links a Django user to the login service's user (the OIDC `sub`)."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oidc_sub = models.CharField(max_length=255, unique=True)


class Heartbeat(models.Model):
    """Written by the example job (platform.yaml `jobs.heartbeat`)."""
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-at"]
