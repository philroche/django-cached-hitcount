__author__ = 'philroche'
from django.db import models

class ExampleModel(models.Model):
    label = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return u'%s' % self.label

#TODo - add save signal