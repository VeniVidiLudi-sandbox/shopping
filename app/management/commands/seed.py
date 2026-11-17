"""Dev data (platform.yaml `commands.seed`; dev only)."""
from django.core.management.base import BaseCommand

from app.models import Heartbeat, Item


class Command(BaseCommand):
    help = "Load dev data."

    def handle(self, *args, **options):
        if not Heartbeat.objects.exists():
            Heartbeat.objects.create()
        if not Item.objects.exists():
            for t in ["Milk x2", "Bread", "Bananas", "Washing-up liquid", "Cheese"]:
                Item.objects.create(text=t)
        self.stdout.write("seeded")
