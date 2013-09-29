from django.core.management.base import BaseCommand
from django.conf import settings
from allmychanges.utils import graphite_send


class Command(BaseCommand):
    help = u"""Send release beats to graphite."""

    def handle(self, *args, **options):
        graphite_send(release=1)
