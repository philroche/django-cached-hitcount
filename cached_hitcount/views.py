import json

from django.http import Http404, HttpResponse
from django.views.decorators.cache import never_cache

from cached_hitcount.utils import get_ip, get_hitcount_cache, is_cached_hitcount_enabled, is_bot_request, using_memcache
from cached_hitcount.models import BlacklistIP
from cached_hitcount.settings import CACHED_HITCOUNT_CACHE_TIMEOUT, CACHED_HITCOUNT_EXCLUDE_IP_ADDRESS, \
    CACHED_HITCOUNT_EXCLUDE_BOTS, CACHED_HITCOUNT_LOCK_KEY, \
    CACHED_HITCOUNT_SERVER_CALLBACKS

from cached_hitcount.decorators import conditional_csrf_exempt

def _update_hit_count(request, object_pk, ctype_pk):
    '''
    Evaluates a request's Hit and corresponding HitCount object and,
    after a bit of clever logic, either ignores the request or registers
    a new Hit.

    This is NOT a view!  But should be used within a view ...

    Returns True if the request was considered a Hit; returns False if not.
    '''
    if request:#we might be calling this form a signal
        ip = get_ip(request)

        # first, check our request against the blacklists before continuing
        if CACHED_HITCOUNT_EXCLUDE_IP_ADDRESS and ip in BlacklistIP.objects.get_cache():
            return False

        #are we excluding bots and is this a bot
        if CACHED_HITCOUNT_EXCLUDE_BOTS and is_bot_request(request):
            return False

    #save to memcache
    hitcount_cache = get_hitcount_cache()

    cache_key = "hitcount__%s__%s" % (ctype_pk, object_pk)

    #if the lock is set then do nothing (this means the hits are being persisted to DB)
    lock = hitcount_cache.get(CACHED_HITCOUNT_LOCK_KEY)
    #print  'check %s lock = %s' % (CACHED_HITCOUNT_LOCK_KEY, lock)
    if lock is None or lock != 1:
        try:
            hitcount_cache.incr(cache_key)
            return True
        except ValueError:#cache might have timed out
            count = 1
            hitcount_cache.set(cache_key, count, CACHED_HITCOUNT_CACHE_TIMEOUT)
            return True

    return False

def json_error_response(error_message):
    return HttpResponse(json.dumps(dict(success=False,
                                              error_message=error_message)))

def call_custom_callbacks():
    results = {}
    #AttributeError
    #ImportError
    for custom_callback_key, custom_callback_module_method in CACHED_HITCOUNT_SERVER_CALLBACKS.iteritems():
        custom_callback_module, custom_callback_method = custom_callback_module_method
        try:
            m = __import__(custom_callback_module, globals(), locals(), [custom_callback_method], -1)
            func = getattr(m,custom_callback_method)
            results[custom_callback_key] = func()
        except AttributeError, ae:
            results.setdefault('errors', []).append('%s has no method %s' % (custom_callback_module, custom_callback_method))
        except ImportError, ie:
            results.setdefault('errors', []).append('Unable to import %s' % custom_callback_module)

    return results

@never_cache
@conditional_csrf_exempt
def update_hit_count_ajax(request):
    '''
    Ajax call that can be used to update a hit count.

    Ajax is not the only way to do this, but probably will cut down on 
    bots and spiders.

    See template tags for how to implement.
    '''

    # make sure this is an ajax request
    if not is_cached_hitcount_enabled() or not using_memcache() or not request.is_ajax():
        raise Http404()

    if request.method == "GET":
        return json_error_response("Hits counted via POST only.")

    object_pk = request.POST.get('object_pk', None)
    ctype_pk = request.POST.get('ctype_pk', None)
    
    status = "no hit recorded"
    if object_pk and ctype_pk:
        result = _update_hit_count(request, object_pk, ctype_pk)

        if result:
            status = "success"

    result_dict = {'status': status}
    if CACHED_HITCOUNT_SERVER_CALLBACKS:
        result_dict.update(call_custom_callbacks())

    return HttpResponse(json.dumps(result_dict),mimetype="application/json")
