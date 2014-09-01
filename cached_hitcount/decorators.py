from django.views.decorators.csrf import csrf_exempt, csrf_protect
from cached_hitcount.settings import CACHED_HITCOUNT_CSRF_EXEMPT

def conditional_csrf_exempt(func):
    if CACHED_HITCOUNT_CSRF_EXEMPT:
        return csrf_exempt(func)
    else:
        return csrf_protect(func)