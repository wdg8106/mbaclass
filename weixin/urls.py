from django.conf.urls import patterns, url

from .views import event
 
urlpatterns = patterns('',
    url(r'^event$', event, name="event"),
)