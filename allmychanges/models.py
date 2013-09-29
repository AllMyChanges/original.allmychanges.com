# -*- coding: utf-8 -*-
import os
import datetime

from django.db import models
from django.utils.timezone import now

from crawler import search_changelog, _parse_changelog_text
from crawler.git_crawler import aggregate_git_log
from allmychanges.utils import (
    cd,
    get_package_metadata,
    download_repo,
    get_commit_type,
    get_markup_type,
    get_clean_text_from_markup_text,
)
from allmychanges.tasks import update_repo


MARKUP_CHOICES = (
    ('markdown', 'markdown'),
    ('rest', 'rest'),
)


class Repo(models.Model):
    PROCESSING_STATE_CHOICES = (
        ('in_progress', 'In progress'),
        ('error', 'Error'),
        ('finished', 'Finished'),
    )

    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    changelog_markup = models.CharField(max_length=20, choices=MARKUP_CHOICES, blank=True, null=True)

    # processing fields
    processing_state = models.CharField(max_length=20, choices=PROCESSING_STATE_CHOICES, null=True)
    processing_status_message = models.CharField(max_length=255, blank=True, null=True)
    processing_progress = models.PositiveIntegerField(default=0)
    processing_date_started = models.DateTimeField(blank=True, null=True)
    processing_date_finished = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'{url}. {title}'.format(url=self.url, title=self.title)

    @classmethod
    def start_changelog_processing_for_url(cls, url):
        repo, is_created = Repo.objects.get_or_create(url=url)
        repo.start_processing_if_needed()
        return repo

    def start_processing_if_needed(self):
        if self.is_need_processing:
            self.start_changelog_processing()
            return True
        else:
            return False

    @property
    def is_need_processing(self):
        if not self.processing_date_started:
            return True
        elif self.is_processing_started_more_than_minutes_ago(30):
            return True
        elif self.is_processing_started_more_than_minutes_ago(5) and self.processing_state == 'finished':
            return True
        elif self.is_processing_started_more_than_minutes_ago(1) and self.processing_state == 'error':
            return True
        else:
            return False

    def is_processing_started_more_than_minutes_ago(self, minutes):
        return now() > self.processing_date_started + datetime.timedelta(minutes=minutes)

    def start_changelog_processing(self):
        update_repo.delay(self.id)

    def _update(self):
        """Updates changelog (usually in background)."""
        self.processing_state = 'in_progress'
        self.processing_status_message = 'Downloading code'
        self.processing_progress = 50
        self.processing_date_started = now()
        self.save()

        try:
            path = download_repo(self.url)

            if path:
                with cd(path):
                    self.processing_status_message = 'Searching changes'
                    self.processing_progress = 55
                    self.save()
                    changelog_filename = search_changelog()
                    if changelog_filename:
                        full_filename = os.path.normpath(
                            os.path.join(os.getcwd(), changelog_filename))

                        self._update_from_filename(full_filename)
                    else:
                        self._update_from_git_log(path)

        except Exception as e:
            self.processing_state = 'error'
            self.processing_status_message = str(e)[:255]
            self.processing_progress = 100
            self.processing_date_finished = now()
            self.save()
            raise

    def _update_from_git_log(self, path):
        changes = aggregate_git_log(path)
        if changes:
            self._update_from_changes(changes)

    def _update_from_filename(self, filename):
        with open(filename) as f:
            self.changelog_markup = get_markup_type(filename)
            self.processing_status_message = 'Parsing changelog'
            self.processing_progress = 60
            self.save()
            changes = _parse_changelog_text(f.read())
            self._update_from_changes(changes)

    def _update_from_changes(self, changes):
        """Update changelog in database, taking data from python-structured changelog."""
        self.title = get_package_metadata('.', 'Name')
        if self.title is None:
            self.title = self.url.rsplit('/', 1)[-1]

        if changes:
            self.versions.all().delete()
            self.processing_status_message = 'Updating database'
            self.processing_progress = 70
            self.save()

            for change in changes:
                version = self.versions.create(name=change['version'])
                for section in change['sections']:

                    item = version.items.create(text=section['notes'])
                    for section_item in section['items']:
                        item.changes.create(type=get_commit_type(section_item), text=section_item)

                        self.processing_state = 'finished'
                        self.processing_status_message = 'Done'
                        self.processing_progress = 100
                        self.processing_date_finished = now()
        else:
            self.processing_state = 'error'
            self.processing_status_message = 'Changelog not found'
            self.processing_progress = 100
            self.processing_date_finished = now()

        self.save()


class RepoVersion(models.Model):
    repo = models.ForeignKey(Repo, related_name='versions')
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class RepoVersionItem(models.Model):
    version = models.ForeignKey(RepoVersion, related_name='items')
    text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'Version item of {version_unicode}'.format(version_unicode=self.version.__unicode__())

    @property
    def clean_text(self):
        return get_clean_text_from_markup_text(self.text, markup_type=self.version.repo.changelog_markup)


class RepoVersionItemChange(models.Model):
    REPO_VERSION_ITEM_CHANGE_TYPE_CHOICES = (
        ('new', 'new'),
        ('fix', 'fix'),
    )

    version_item = models.ForeignKey(RepoVersionItem, related_name='changes')
    type = models.CharField(max_length=10, choices=REPO_VERSION_ITEM_CHANGE_TYPE_CHOICES)
    text = models.TextField()

    @property
    def text_clean(self):
        return get_clean_text_from_markup_text(self.text, markup_type=self.version_item.version.repo.changelog_markup)