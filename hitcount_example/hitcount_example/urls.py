from django.conf.urls import patterns, include, url
from django.contrib import admin

from cached_hitcount import urls as hitcount_ruls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hits/', include(hitcount_ruls)),
    url(r'^$', 'hitcount_example.views.index', name='hitcount_example_index'),
)
