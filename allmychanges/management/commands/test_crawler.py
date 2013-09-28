import os
import requests
import re
import envoy

from django.core.management.base import BaseCommand
from django.conf import settings
from crawler import search_changelog, _parse_changelog_text
from allmychanges.utils import cd, load_data, transform_url, download_repo


def fetch_with_crawler_this(url):
    try:
        if False:
            result = requests.get(url)
            if result.status_code != 200:
                raise RuntimeError('Bad status code: {0}'.format(result.status_code))

        path = download_repo(url, pull_if_exists=False)

        if path and os.path.exists(path):
            with cd(path):
                changelog_filename = search_changelog()
                if changelog_filename:
                    fullfilename = os.path.normpath(
                        os.path.join(os.getcwd(), changelog_filename))
                    was_parsed = False
                    num_versions = num_items = 0
                    try:
                        with open(fullfilename) as f:
                            changes = _parse_changelog_text(f.read())
                            num_versions = len(changes)
                            num_items = sum(len(section['items'])
                                            for version in changes
                                            for section in version['sections'])

                            if num_versions > 0 and num_items > 0:
                                was_parsed = True
                    except Exception:
                        pass
                    return fullfilename, was_parsed, num_versions, num_items, False
    finally:
        pass

    return None, False, 0, 0, path is None

        

class Command(BaseCommand):
    help = u"""Tests crawler on selected projects."""

    def handle(self, *args, **options):
        root = settings.REPO_ROOT
        reps = load_data(os.path.join(root, 'reps.csv'))

        changelogs_found = 0
        changelogs_parsed = 0
        changelogs_versions = 0
        changelogs_items = 0
        reps_not_found = 0

        for name, url in reps:
            try:
                changelog_filename, was_parsed, num_versions, num_items, not_found = fetch_with_crawler_this(url)
                if not_found:
                    reps_not_found += 1
                    
                if changelog_filename:
                    changelogs_found += 1
                    if was_parsed:
                        changelogs_parsed += 1
                        changelogs_versions += num_versions
                        changelogs_items += num_items

                else:
                    # changelog not found in repository
                    print url

            except RuntimeError:
                pass

        stats = {}
        stats['crawler.changelogs-found'] = changelogs_found
        stats['crawler.changelogs-parsed'] = changelogs_parsed
        stats['crawler.changelog-versions-parsed'] = changelogs_versions
        stats['crawler.changelog-items-parsed'] = changelogs_items
        stats['crawler.reps-not-found'] = reps_not_found

        with open(os.path.join(settings.PROJECT_ROOT, '.stats'), 'w') as f:
            for key, value in stats.items():
                f.write('{key} {value}\n'.format(key=key, value=value))
