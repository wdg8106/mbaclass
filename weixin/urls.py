from django.conf.urls import patterns, url

from .views import callback
 
urlpatterns = patterns('',
    url(r'^cb$', callback, name="wx_callback"),
)