from django.conf import settings

CACHED_HITCOUNT_CACHE = getattr(settings, 'HITCOUNT_CACHE', 'default')#The CACHES settings dict key to use for caching hits # hitcount_cache

CACHED_HITCOUNT_ENABLED = hasattr(settings, 'CACHES') and CACHED_HITCOUNT_CACHE in getattr(settings, 'CACHES', {})

CACHED_HITCOUNT_CACHE_TIMEOUT = getattr(settings, 'HITCOUNT_CACHE_TIMEOUT', 600 )#600 = 10 mins,  3600 = 1 hour# How long in seconds should the hits be cached for before persisted
CACHED_HITCOUNT_IP_CACHE_TIMEOUT = getattr(settings, 'HITCOUNT_IP_CACHE_TIMEOUT', 86400 )#600 = 10 mins,  3600 = 1 hour, 86400=1 day# How long in seconds should the black list ip addresses be cached for
CACHED_HITCOUNT_PERSIST_SCHEDULE = getattr(settings, 'HITCOUNT_PERSIST_SCHEDULE', 15 )#minutes # How often should the hits be persisted
CACHED_HITCOUNT_IP_CACHE = getattr(settings, 'HITCOUNT_IP_CACHE', 'hitcount__blacklistip')#key name to use for caching the blacklist ip addresses
CACHED_HITCOUNT_EXCLUDE_IP_ADDRESS = getattr(settings, 'HITCOUNT_EXCLUDE_IP_ADDRESS', True)#Wheter or not you want to exclude some ip addresses
CACHED_HITCOUNT_EXCLUDE_BOTS = getattr(settings, 'HITCOUNT_EXCLUDE_BOTS', True)#Whether or not you exclude bots
