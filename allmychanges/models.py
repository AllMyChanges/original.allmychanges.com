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
    version = models.CharField(max_length=255)

    def __unicode__(self):
        return self.version


class RepoVersionItem(models.Model):
    REPO_VERSION_ITEM_TYPE_CHOICES = (
        ('new', 'new'),
        ('fix', 'fix'),
    )

    version = models.ForeignKey(RepoVersion, related_name='items')
    type = models.CharField(max_length=10, choices=REPO_VERSION_ITEM_TYPE_CHOICES)
    text = models.TextField()