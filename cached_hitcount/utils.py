from datetime import datetime, timedelta
import re
from gargoyle import gargoyle

from django.core.cache import cache, get_cache
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from cached_hitcount.settings import CACHED_HITCOUNT_CACHE, CACHED_HITCOUNT_ENABLED


# this is not intended to be an all-knowing IP address regex
IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def is_cached_hitcount_enabled():
    return gargoyle.is_active('cached_hitcount', default=True) and CACHED_HITCOUNT_ENABLED

def get_target_ctype_pk(obj):
    return ContentType.objects.get_for_model(obj), obj.pk


def return_period_from_string(arg):
    '''
    Takes a string such as "days=1,seconds=30" and strips the quotes
    and returns a dictionary with the key/value pairs
    '''
    period = {}

    if arg[0] == '"' and arg[-1] == '"':
        opt = arg[1:-1] #remove quotes
    else:
        opt = arg

    for o in opt.split(","):
        key, value = o.split("=")
        period[str(key)] = int(value)

    return period


def get_hit_count(*args, **kwargs):
    from cached_hitcount.models import Hit#avoid circular import


    hits =  Hit.objects.all()

    if "within" in kwargs:
        within = kwargs["within"]
        if not isinstance(within, timedelta):
            timedelta_dict = return_period_from_string(within)
            within = timedelta(**timedelta_dict)

        period = datetime.utcnow() - within
        hits = hits.filter(added__gte=period)

    if "object_ids" in kwargs and "object" in kwargs:
        object = kwargs["object"]#need object to get the content type
        object_ids = kwargs["object_ids"]
        content_type, object_pk = get_target_ctype_pk(object)
        hits =  hits.filter(object_pk__in=object_ids, content_type=content_type)
    elif "object" in kwargs:
        object = kwargs["object"]
        content_type, object_pk = get_target_ctype_pk(object)
        hits =  hits.filter(object_pk=object_pk, content_type=content_type)

    total_hits = 0

    try:
        total_hits = hits.aggregate(Sum('hits'))['hits__sum']
    except Hit.DoesNotExist:
        #create a Hit for this object as it doesn't exist yet
        Hit.objects.select_for_update().get_or_create(added=datetime.utcnow().date(), object_pk=object_pk, content_type=content_type)

    return str(total_hits)

def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.

    **NOTE** This function was taken from django-tracking (MIT LICENSE)
             http://code.google.com/p/django-tracking/
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                # no IP, probably from some dirty proxy or other device
                # throw in some bogus IP
                ip_address = '10.0.0.1'
        except IndexError:
            pass

    return ip_address

hitcount_cache = None
def get_hitcount_cache():
    global hitcount_cache
    if hitcount_cache is None:
        try:
            hitcount_cache = get_cache(CACHED_HITCOUNT_CACHE)
        except:
            # Use the default cache
            hitcount_cache = cache
    return hitcount_cache
