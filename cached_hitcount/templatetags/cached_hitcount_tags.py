from django import template
from django.core.urlresolvers import reverse

from cached_hitcount.utils import get_target_ctype_pk, get_hit_count as get_hit_count_utils
from cached_hitcount.settings import CACHED_HITCOUNT_CLIENT_CALLBACKS

register = template.Library()




@register.simple_tag(takes_context=True)
def get_hit_count(context, object, *args, **kwargs):
    '''
    Returns hit counts for an object.

    - Return total hits for an object: 
      {% get_hit_count [object] %}
    
    - Get total hits for an object over a certain time period:
      {% get_hit_count [object] within=["days=1"] %}

    The within arguments need to follow datetime.timedelta's limitations:
    Accepts days and weeks.
    '''
    kwargs['object'] = object
    return get_hit_count_utils(*args, **kwargs)



@register.inclusion_tag('hitcount_js.html', takes_context=True)
def get_hit_count_javascript_template(context, object, **kwargs):
    '''
    Return javascript for an object
    and requires jQuery.  NOTE: only works on a single object, not an object
    list.

    For example:

    {% get_hit_count_javascript_template [object] %}

    '''
    url = reverse('update_hit_count_ajax')
    ctype, object_pk = get_target_ctype_pk(object)
    csrf_token = unicode(context['csrf_token'])

    template_context = {
        'ctype_pk': ctype.pk,
        'object_pk': object_pk,
        'csrf_token': csrf_token,
        'url' : url,
    }

    if CACHED_HITCOUNT_CLIENT_CALLBACKS:
        template_context['client_callbacks'] = CACHED_HITCOUNT_CLIENT_CALLBACKS

    return template_context