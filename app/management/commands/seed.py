"""Dev data (platform.yaml `commands.seed`; dev only)."""
from django.core.management.base import BaseCommand

from app.models import Heartbeat


class Command(BaseCommand):
    help = "Load dev data."

    def handle(self, *args, **options):
        if not Heartbeat.objects.exists():
            Heartbeat.objects.create()
        self.stdout.write("seeded")
