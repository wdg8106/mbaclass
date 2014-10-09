from django.conf.urls import patterns, include, url

import xadmin

urlpatterns = patterns('',
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^wx/',include('weixin.urls' )),
    url(r'^', include(xadmin.site.urls)),
)
