# coding=utf-8
import xadmin
from xadmin.layout import *

from .models import Event, EventMember

class EventAdmin(object):
    list_display = ('slug', 'public_time', 'start_time', 'end_time', 'author', 'is_active')
    list_filter = ('public_time', 'start_time', 'end_time', 'author', 'is_active')

    search_fields = ('slug',)

    model_icon = 'fa fa-bullhorn'

    user_fields = ('author',)

xadmin.site.register(Event, EventAdmin)