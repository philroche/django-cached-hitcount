import datetime

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.dispatch import Signal

from cached_hitcount.settings import CACHED_HITCOUNT_IP_CACHE_TIMEOUT, CACHED_HITCOUNT_IP_CACHE
from cached_hitcount.utils import get_hitcount_cache
# SIGNALS #
#TODO model to create an initial entry in DB for object and also set initial value (0) in memcache

# MODELS #
class Hit(models.Model):
    '''
    Model that stores the hit totals for any content object.

    '''

    hits = models.PositiveIntegerField(default=0)
    added        = models.DateField(default=datetime.datetime.utcnow().date(), db_index=True)
    content_type    = models.ForeignKey(ContentType,
                        verbose_name="content type",
                        related_name="content_type_set_for_%(class)s", db_index=True)
    object_pk       = models.PositiveIntegerField('object ID', db_index=True)
    content_object  = generic.GenericForeignKey('content_type', 'object_pk')

    class Meta:
        ordering = ( '-hits', )
        #unique_together = (("content_type", "object_pk"),)
        get_latest_by = "added"

    def __unicode__(self):
        return u'%s' % self.content_object

    def get_content_object_url(self):
        '''
        Django has this in its contrib.comments.model file -- seems worth
        implementing though it may take a couple steps.
        '''
        pass

#MANAGER
class BlacklistIPManager(models.Manager):
    def set_cache(self):
        hitcount_cache = get_hitcount_cache()
        blacklist_ips = list(self.get_query_set().values_list('ip',flat=True))
        hitcount_cache.set(CACHED_HITCOUNT_IP_CACHE, blacklist_ips, CACHED_HITCOUNT_IP_CACHE_TIMEOUT)
        return blacklist_ips

    def get_cache(self):
        hitcount_cache = get_hitcount_cache()
        blacklist_ips = hitcount_cache.get(CACHED_HITCOUNT_IP_CACHE)
        if not blacklist_ips and not isinstance(blacklist_ips, list):
            blacklist_ips = self.set_cache()
        return blacklist_ips


class BlacklistIP(models.Model):

    objects = BlacklistIPManager()

    ip = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return u'%s' % self.ip

    def save(self,*args, **kwargs):
        super(BlacklistIP, self).save(*args, **kwargs)
        BlacklistIP.objects.set_cache()
