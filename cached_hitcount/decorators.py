from django.views.decorators.csrf import csrf_exempt
from cached_hitcount.settings import CACHED_HITCOUNT_CSRF_EXEMPT

def conditional_csrf_exempt(func):
    if not CACHED_HITCOUNT_CSRF_EXEMPT:
        return csrf_exempt(func)
    else:
        return func