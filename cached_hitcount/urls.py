from django.conf.urls import patterns, url
from .views import update_hit_count_ajax



urlpatterns = patterns('',
    url(r'$', update_hit_count_ajax, name='update_hit_count_ajax'),
)