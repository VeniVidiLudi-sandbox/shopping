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


class Item(models.Model):
    """One post-it on the shared list."""
    COLOURS = ["yellow", "pink", "blue", "green", "orange"]
    text = models.CharField(max_length=120)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                 related_name="items_added")
    added_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="items_ordered")
    ordered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["ordered", "-added_at", "-id"]

    def __str__(self):
        return self.text

    @property
    def colour(self):
        return self.COLOURS[self.pk % len(self.COLOURS)]

    @property
    def tilt(self):
        return (-2.5, 1.5, -1, 2.5, 0.5, -1.8)[self.pk % 6]

    @property
    def adder_name(self):
        u = self.added_by
        return (u.first_name or u.username) if u else "someone"
