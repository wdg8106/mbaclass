from django.conf.urls import patterns, include, url

import xadmin

urlpatterns = patterns('',
    url(r'^', include(xadmin.site.urls))
)
