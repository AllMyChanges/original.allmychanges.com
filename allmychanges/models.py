# -*- coding: utf-8 -*-
from django.db import models


class Repo(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{url}. {title}'.format(url=self.url, title=self.title)


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