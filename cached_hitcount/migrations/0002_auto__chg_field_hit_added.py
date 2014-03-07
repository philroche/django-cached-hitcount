# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Hit.added'
        db.alter_column(u'cached_hitcount_hit', 'added', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Hit.added'
        db.alter_column(u'cached_hitcount_hit', 'added', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'cached_hitcount.blacklistip': {
            'Meta': {'object_name': 'BlacklistIP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'cached_hitcount.hit': {
            'Meta': {'ordering': "('-hits',)", 'object_name': 'Hit'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 28, 0, 0)'}),
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