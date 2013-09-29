from django.core.management.base import BaseCommand

from allmychanges.models import Repo

        
class Command(BaseCommand):
    help = u"""Deletes all repositories and related information."""

    def handle(self, *args, **options):
        Repo.objects.all().delete()
