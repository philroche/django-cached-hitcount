Django-Cached-HitCount
===============

Basic app that allows you to track the number of hits/views for a particular
object.

All hits are stored in memcache

Available settings are:

HITCOUNT_CACHE -The CACHES settings dict key to use for caching hits (default is 'cached_hitcount')
HITCOUNT_CACHE_TIMEOUT - How long in seconds should the hits be cached for before persisted  (default is '600')
HITCOUNT_IP_CACHE_TIMEOUT - How long in seconds should the black list ip addresses be cached for  (default is '86400' seconds = 1 day)
HITCOUNT_PERSIST_SCHEDULE - How often should the hits be persisted  (default is '15' minutes)
HITCOUNT_IP_CACHE - key name to use for caching the blacklist ip addresses  (default is 'hitcount__blacklistip')
HITCOUNT_EXCLUDE_IP_ADDRESS - Wheter or not you want to exclude some ip addresses  (default is True)

Also a gargoyle switch 'cached_hitcount' to switch on/off all hit counting (default is True)

This app was very much inspired by <http://damontimm.com/code/django-hitcount/>


Installation:
-------------

Simplest way to formally install is to run:

    ./setup.py install

Or, you could do a PIP installation:

    pip install -e git://github.com/philroche/django-cached-hitcount.git#egg=django-cached-hitcount




