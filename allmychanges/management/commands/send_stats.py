import graphitesend
import os


from django.core.management.base import BaseCommand
from django.conf import settings


def get_stats():
    with open(os.path.join(settings.PROJECT_ROOT, '.stats')) as f:
        lines = f.readlines()
        stats = [line.split(None, 1) for line in lines]
        stats = {name: float(value) for name, value in stats}
        return stats


class Command(BaseCommand):
    help = u"""Send stats to graphite Graphite."""

    def handle(self, *args, **options):
        prefix = 'allmychanges.'
        stats = get_stats()
        g = graphitesend.init(prefix=prefix,
                              graphite_server=settings.GRAPHITE_HOST)
        g.send_dict(stats)
