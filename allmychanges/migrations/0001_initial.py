# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repo'
        db.create_table(u'allmychanges_repo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'allmychanges', ['Repo'])

        # Adding model 'RepoVersion'
        db.create_table(u'allmychanges_repoversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['allmychanges.Repo'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'allmychanges', ['RepoVersion'])

        # Adding model 'RepoVersionItem'
        db.create_table(u'allmychanges_repoversionitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['allmychanges.RepoVersion'])),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'allmychanges', ['RepoVersionItem'])

        # Adding model 'RepoVersionItemChange'
        db.create_table(u'allmychanges_repoversionitemchange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['allmychanges.RepoVersionItem'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'allmychanges', ['RepoVersionItemChange'])


    def backwards(self, orm):
        # Deleting model 'Repo'
        db.delete_table(u'allmychanges_repo')

        # Deleting model 'RepoVersion'
        db.delete_table(u'allmychanges_repoversion')

        # Deleting model 'RepoVersionItem'
        db.delete_table(u'allmychanges_repoversionitem')

        # Deleting model 'RepoVersionItemChange'
        db.delete_table(u'allmychanges_repoversionitemchange')


    models = {
        u'allmychanges.repo': {
            'Meta': {'object_name': 'Repo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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