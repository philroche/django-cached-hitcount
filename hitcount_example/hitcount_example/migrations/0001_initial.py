# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExampleModel'
        db.create_table(u'hitcount_example_examplemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal(u'hitcount_example', ['ExampleModel'])


    def backwards(self, orm):
        # Deleting model 'ExampleModel'
        db.delete_table(u'hitcount_example_examplemodel')


    models = {
        u'hitcount_example.examplemodel': {
            'Meta': {'object_name': 'ExampleModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['hitcount_example']