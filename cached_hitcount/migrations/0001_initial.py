# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hit'
        db.create_table(u'cached_hitcount_hit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_hit', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'cached_hitcount', ['Hit'])

        # Adding model 'BlacklistIP'
        db.create_table(u'cached_hitcount_blacklistip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal(u'cached_hitcount', ['BlacklistIP'])


    def backwards(self, orm):
        # Deleting model 'Hit'
        db.delete_table(u'cached_hitcount_hit')

        # Deleting model 'BlacklistIP'
        db.delete_table(u'cached_hitcount_blacklistip')


    models = {
        u'cached_hitcount.blacklistip': {
            'Meta': {'object_name': 'BlacklistIP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'cached_hitcount.hit': {
            'Meta': {'ordering': "('-hits',)", 'object_name': 'Hit'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_hit'", 'to': u"orm['contenttypes.ContentType']"}),
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cached_hitcount']