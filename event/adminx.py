# coding=utf-8
import xadmin
import json

#from xadmin.layout import *
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from .models import Event, EventMember, EventField
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied


from dynamic_forms.admin import AdminFormFieldInlineForm

class FormFieldInlineAdmin(object):
    model = EventField
    extra = 1
    style = 'accordion'
    form = AdminFormFieldInlineForm
    list_display = ('field_type', 'name', 'label')

class EventMemberInline(object):
    model = EventMember
    style = 'table'
    readonly_fields = ('is_response', 'status', 'value', 'is_send_wx', 'is_send_sms')
    extra = 1

class EventAdmin(object):

    def show_page(self, event):
        return '<a href="%s"/><i class="fa fa-eye"></i></a>' % self.get_admin_url('event_show', event.id)
    show_page.short_description = "查看"
    show_page.allow_tags = True

    list_display = ('title', 'event_type', 'public_time', 'start_time', 'end_time', 'author', 'is_active', 'show_page')
    list_filter = ('public_time', 'event_type', 'public_time', 'start_time', 'end_time', 'author', 'is_active')

    search_fields = ('slug',)

    model_icon = 'fa fa-bullhorn'

    user_fields = ('author',)

    inlines = (EventMemberInline, FormFieldInlineAdmin, )

    formfield_overrides = {UEditorField: {'widget': UEditorWidget({'width':'100%', 'height':300, 'toolbars':"full", 'imagePath':"event/img/", 'filePath':"event/file/"})}}

xadmin.site.register(Event, EventAdmin)

class EventMemberAdmin(object):
    list_display = ('event', 'member', 'status', 'is_response', 'is_send_wx', 'is_send_sms', 'pretty_value')
    list_filter = ('is_response', 'status', 'member__classnum')
    readonly_fields = ('is_response', 'status', 'value', 'is_send_wx', 'is_send_sms')

    model_icon = 'fa fa-bullhorn'

    user_can_access_owned_objects_only = True
    user_owned_objects_field = 'member'
xadmin.site.register(EventMember, EventMemberAdmin)


from xadmin.views.form import FormAdminView
from dynamic_forms.forms import FormModelForm

class EventFormView(FormAdminView):
    form = FormModelForm
    form_template = 'event/show.html'
    title = '活动通知'

    def init_request(self, event_id, *args, **kwargs):
        event = Event.objects.get(id=event_id)

        try:
            event_data = EventMember.objects.get(event=event, member=self.user)
            if event_data.status > 3:
                raise PermissionDenied
        except EventMember.DoesNotExist:
            raise PermissionDenied

        self.form_model = event
        self.event_data = event_data

        self.prepare_form()

    def get_context(self):
        context = super(EventFormView, self).get_context()
        context.update({
            'event': self.form_model
        })
        return context

    def get_form_datas(self):
        data = super(EventFormView, self).get_form_datas()
        data['model'] = self.form_model
        return data

    def save_forms(self):
        mapped_data = self.form_obj.get_mapped_data()
        self.event_data.value = json.dumps(mapped_data, cls=DjangoJSONEncoder)
        self.event_data.status = 3
        self.event_data.is_response = True
        self.event_data.save()

    def post_response(self):
        msg = '您的信息已经成功提交，感谢您的支持，祝您不挂科。'
        self.message_user(msg, 'success')

        return self.get_redirect_url()

xadmin.site.register_view(r'^event/show/(\d+)$', EventFormView, name='event_show')

class GlobalSetting(object):

    def get_context(self):
        context = super(GlobalSetting, self).get_context()
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'com.tencent.mm':
            context['base_template'] = 'base_wx.html'
            context['in_wx'] = True
        return context

xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
