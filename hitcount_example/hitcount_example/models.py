__author__ = 'philroche'
from django.db import models
from django.db.models.signals import post_save

from cached_hitcount.models import process_object_saved

class ExampleModel(models.Model):
    label = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return u'%s' % self.label


post_save.connect(process_object_saved, sender=ExampleModel)
