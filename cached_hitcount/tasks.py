from datetime import datetime, timedelta
from gargoyle import gargoyle
from celery.task import periodic_task
from memcached_stats import MemcachedStats

from django.core.cache import parse_backend_conf
from django.contrib.contenttypes.models import ContentType

from cached_hitcount.utils import get_hitcount_cache
from cached_hitcount.settings import CACHED_HITCOUNT_ENABLED, CACHED_HITCOUNT_CACHE, CACHED_HITCOUNT_CACHE_TIMEOUT, CACHED_HITCOUNT_IP_CACHE
from cached_hitcount.models import Hit
@periodic_task(run_every=timedelta(minutes=5))
def persist_hits():
    if CACHED_HITCOUNT_ENABLED:
        #TODO - add a try except around this n case it can't connect
        backend, location, params = parse_backend_conf(CACHED_HITCOUNT_CACHE)
        host, port = location.split(':')
        mem = MemcachedStats(host, port)
        keys = mem.keys()
        hitcount_cache = get_hitcount_cache()
        content_types = {}#used for keeping track of the content types so DB doesn't have to be queried each time
        for cache_key in keys:
            if "hitcount__" in cache_key and not CACHED_HITCOUNT_IP_CACHE in cache_key:
                cache_key = cache_key.split(':')[-1]#TODO why do we have to do this?
                count = hitcount_cache.get(cache_key)
                hitcount, ctype_pk, object_pk  = cache_key.split('__')

                if ctype_pk in content_types.keys():
                    content_type = content_types[ctype_pk]
                else:
                    content_type = ContentType.objects.get(id=ctype_pk)
                    content_types[ctype_pk] = content_type

                #save a new hit or increment this hits on an existing hit
                hit, created = Hit.objects.select_for_update().get_or_create(added=datetime.utcnow().date(), object_pk=object_pk, content_type=content_type)
                if hit and created:
                    hit.hits = count
                    hit.save()
                elif hit:
                    hit.hits = hit.hits + count
                    hit.save()

                #reset the hitcount for this object to 0
                hitcount_cache.set(cache_key, 0, CACHED_HITCOUNT_CACHE_TIMEOUT)





