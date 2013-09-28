# -*- coding: utf-8 -*-

import os

from django.db import models
from crawler import search_changelog, _parse_changelog_text
from allmychanges.utils import cd, get_package_metadata, download_repo


class Repo(models.Model):
    PROCESSING_STATE_CHOICES = (
        ('in_progress', 'In progress'),
        ('error', 'Error'),
        ('finished', 'Finished'),
    )

    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)

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

    def is_need_processing(self):
        # todo: me
        return True

    def start_changelog_processing(self):
        path = download_repo(self.url)
        
        if path:
            with cd(path):
                changelog_filename = search_changelog()
                if changelog_filename:
                    fullfilename = os.path.normpath(
                        os.path.join(os.getcwd(), changelog_filename))

                    with open(fullfilename) as f:
                        changes = _parse_changelog_text(f.read())

                        if changes:
                            self.title = get_package_metadata('.', 'Name')
                            self.versions.all().delete()

                            for change in changes:
                                version = self.versions.create(name=change['version'])
                                for section in change['sections']:
                                    item = version.items.create(text=section['notes'])
                                    for section_item in section['items']:
                                        item.changes.create(type='new', text=section_item)
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


class RepoVersionItemChange(models.Model):
    REPO_VERSION_ITEM_CHANGE_TYPE_CHOICES = (
        ('new', 'new'),
        ('fix', 'fix'),
    )

    version_item = models.ForeignKey(RepoVersionItem, related_name='changes')
    type = models.CharField(max_length=10, choices=REPO_VERSION_ITEM_CHANGE_TYPE_CHOICES)
    text = models.TextField()
