# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Repo.processing_state'
        db.add_column(u'allmychanges_repo', 'processing_state',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)

        # Adding field 'Repo.processing_status_message'
        db.add_column(u'allmychanges_repo', 'processing_status_message',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Repo.processing_progress'
        db.add_column(u'allmychanges_repo', 'processing_progress',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Repo.processing_date_started'
        db.add_column(u'allmychanges_repo', 'processing_date_started',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Repo.processing_date_finished'
        db.add_column(u'allmychanges_repo', 'processing_date_finished',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Repo', fields ['url']
        db.create_unique(u'allmychanges_repo', ['url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repo', fields ['url']
        db.delete_unique(u'allmychanges_repo', ['url'])

        # Deleting field 'Repo.processing_state'
        db.delete_column(u'allmychanges_repo', 'processing_state')

        # Deleting field 'Repo.processing_status_message'
        db.delete_column(u'allmychanges_repo', 'processing_status_message')

        # Deleting field 'Repo.processing_progress'
        db.delete_column(u'allmychanges_repo', 'processing_progress')

        # Deleting field 'Repo.processing_date_started'
        db.delete_column(u'allmychanges_repo', 'processing_date_started')

        # Deleting field 'Repo.processing_date_finished'
        db.delete_column(u'allmychanges_repo', 'processing_date_finished')


    models = {
        u'allmychanges.repo': {
            'Meta': {'object_name': 'Repo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processing_date_finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'processing_date_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'processing_progress': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'processing_state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'processing_status_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'allmychanges.repoversion': {
            'Meta': {'object_name': 'RepoVersion'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': u"orm['allmychanges.Repo']"})
        },
        u'allmychanges.repoversionitem': {
            'Meta': {'object_name': 'RepoVersionItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['allmychanges.RepoVersion']"})
        },
        u'allmychanges.repoversionitemchange': {
            'Meta': {'object_name': 'RepoVersionItemChange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'version_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': u"orm['allmychanges.RepoVersionItem']"})
        }
    }

    complete_apps = ['allmychanges']