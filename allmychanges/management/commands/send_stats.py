import os

from django.core.management.base import BaseCommand
from django.conf import settings
from allmychanges.utils import graphite_send


def get_stats():
    with open(os.path.join(settings.PROJECT_ROOT, '.stats')) as f:
        lines = f.readlines()
        stats = [line.split(None, 1) for line in lines]
        stats = {name: float(value) for name, value in stats}
        return stats


class Command(BaseCommand):
    help = u"""Send stats to graphite Graphite."""

    def handle(self, *args, **options):
        stats = get_stats()
        graphite_send(**stats)
