Django-Cached-HitCount
===============

Basic app that allows you to track the number of hits/views for a particular
object.

All hits are stored in memcache until persisted to database.

As the hits are stored in cache there are no DB queries/inserts/updates on each request.

Adding hits is done via an ajax call so that app can still be used on cached views.

You can persist the hits to DB using celery and the `persist_hits` periodic task or use the `persist_hits` management command.

    python manage.py persist_hits

hitcount_example app shows how to use app, by using `get_hit_count_javascript_template` and `get_hit_count` template tags.

Available settings are:

* HITCOUNT_CACHE -The CACHES setting dict key to use for caching hits (default is `cached_hitcount`)
* HITCOUNT_CACHE_TIMEOUT - How long in seconds should the hits be cached for before persisted  (default is `600`)
* HITCOUNT_IP_CACHE_TIMEOUT - How long in seconds should the black list ip addresses be cached for  (default is `86400` seconds = 1 day)
* HITCOUNT_PERSIST_SCHEDULE - How often should the hits be persisted  (default is `15` minutes)
* HITCOUNT_IP_CACHE - key name to use for caching the blacklist ip addresses  (default is `hitcount__blacklistip`)
* HITCOUNT_EXCLUDE_IP_ADDRESS - Whether or not you want to exclude some ip addresses  (default is True)
* HITCOUNT_EXCLUDE_BOTS - Whether or not you exclude bots (default is True)
* HITCOUNT_LOCK_KEY - key name to use for locking when persisting hits to DB

Also a gargoyle switch `cached_hitcount` to switch on/off all hit counting (default is True)

This app was very much inspired by <http://damontimm.com/code/django-hitcount/>


Installation:
-------------

Simplest way to formally install is to run:

    ./setup.py install

Or, you could do a PIP installation:

    pip install -e git://github.com/philroche/django-cached-hitcount.git#egg=django-cached-hitcount

Or using PyPi

    pip install django-cached-hitcount

Copyright:
-------------

This package is © 2014 Philip Roche, released under the terms of the GNU GPL v3 (or at your option a later version).