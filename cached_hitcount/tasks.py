from datetime import datetime, timedelta
from celery.task import periodic_task
from memcached_stats import MemcachedStats
import logging


from django.core.cache import parse_backend_conf
from django.contrib.contenttypes.models import ContentType

try:
    from django.db.transaction import atomic as transaction_atomic
except ImportError:
    from django.db.transaction import commit_on_success as transaction_atomic

from cached_hitcount.utils import get_hitcount_cache, is_cached_hitcount_enabled, release_lock
from cached_hitcount.settings import CACHED_HITCOUNT_CACHE, CACHED_HITCOUNT_CACHE_TIMEOUT, CACHED_HITCOUNT_IP_CACHE, CACHED_HITCOUNT_LOCK_KEY
from cached_hitcount.models import Hit

logger = logging.getLogger(__name__)

@periodic_task(run_every=timedelta(minutes=5))
def persist_hits():
    if is_cached_hitcount_enabled:

        backend, location, params = parse_backend_conf(CACHED_HITCOUNT_CACHE)
        host, port = location.split(':')
        hitcount_cache = get_hitcount_cache()
        lock = hitcount_cache.get(CACHED_HITCOUNT_LOCK_KEY)
        #print  'persist_hits - check %s lock = %s' % (CACHED_HITCOUNT_LOCK_KEY, lock)
        if lock is None or lock != 1:
            try:
                #acquire a lock so no updates will occur while we are persisting the hits to DB
                hitcount_cache.set(CACHED_HITCOUNT_LOCK_KEY, 1, CACHED_HITCOUNT_CACHE_TIMEOUT)
                #print  'acquire %s lock = %s ' % (CACHED_HITCOUNT_LOCK_KEY, hitcount_cache.get(CACHED_HITCOUNT_LOCK_KEY))
                mem = MemcachedStats(host, port)
                keys = mem.keys()

                content_types = {}#used for keeping track of the content types so DB doesn't have to be queried each time
                for cache_key in keys:
                    if "hitcount__" in cache_key and not CACHED_HITCOUNT_IP_CACHE in cache_key:
                        cache_key = cache_key.split(':')[-1]#the key is a combination of key_prefix, version and key all separated by : - all we need is the key
                        count = hitcount_cache.get(cache_key)
                        if count:#only update the hit count if the is not None
                            hitcount, ctype_pk, object_pk  = cache_key.split('__')
                            if ctype_pk in content_types.keys():
                                content_type = content_types[ctype_pk]
                            else:
                                content_type = ContentType.objects.get(id=ctype_pk)
                                content_types[ctype_pk] = content_type

                            with transaction_atomic():
                                #save a new hit or increment this hits on an existing hit
                                hit, created = Hit.objects.select_for_update().get_or_create(added=datetime.utcnow().date(), object_pk=object_pk, content_type=content_type)
                                if hit and created:
                                    hit.hits = long(count)
                                    hit.save()
                                elif hit:
                                    hit.hits = hit.hits + long(count)
                                    hit.save()

                        #reset the hitcount for this object to 0 - even if it was previously None
                        hitcount_cache.set(cache_key, 0, CACHED_HITCOUNT_CACHE_TIMEOUT)
                        #print  'reset key %s to zero = %s ' % (cache_key, hitcount_cache.get(cache_key))
            except Exception, ex:
                logger.error('Unable to persist hits')
                logger.error(ex)

                raise ex
            finally:
                release_lock()
        else:
            logger.error('Unable to persist hits due to persist task already in progress (%s is locked)' % CACHED_HITCOUNT_LOCK_KEY)





