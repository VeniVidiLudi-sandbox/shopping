"""The example job (platform.yaml `jobs.heartbeat`): hourly in prod, on
command in dev (`platform job run heartbeat`)."""
from django.core.management.base import BaseCommand

from app.models import Heartbeat


class Command(BaseCommand):
    help = "Record a heartbeat."

    def handle(self, *args, **options):
        Heartbeat.objects.create()
        Heartbeat.objects.filter(pk__in=Heartbeat.objects.values_list("pk", flat=True)[1000:]).delete()
        self.stdout.write("ok")
