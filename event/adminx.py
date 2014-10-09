# coding=utf-8
import xadmin
from xadmin.layout import *
from xadmin.plugins.inline import Inline
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from .models import Event, EventMember, EventForm, EventField
from django.forms import Media


from dynamic_forms.admin import AdminFormFieldInlineForm

class FormFieldInlineAdmin(object):
    model = EventField
    extra = 1
    style = 'accordion'
    form = AdminFormFieldInlineForm
    list_display = ('field_type', 'name', 'label')

class EventMemberInline(object):
    model = EventMember
    readonly_fields = ('is_response', )
    extra = 1

class EventAdmin(object):

    def show_page(self, event):
        return '<a href="%s"/><i class="fa fa-eye"></i></a>' % self.get_admin_url('event_show', event.id)
    show_page.short_description = "查看"
    show_page.allow_tags = True

    list_display = ('slug', 'public_time', 'start_time', 'end_time', 'author', 'is_active', 'show_page')
    list_filter = ('public_time', 'start_time', 'end_time', 'author', 'is_active')

    search_fields = ('slug',)

    model_icon = 'fa fa-bullhorn'

    user_fields = ('author',)

    inlines = (EventMemberInline, FormFieldInlineAdmin, )

    formfield_overrides = {UEditorField: {'widget': UEditorWidget({'width':'100%', 'height':300, 'toolbars':"full", 'imagePath':"event/img/", 'filePath':"event/file/"})}}

xadmin.site.register(Event, EventAdmin)

class EventMemberAdmin(object):
    list_display = ('event', 'member', 'is_response')
    list_filter = ('is_response',)
    readonly_fields = ('is_response', )

    model_icon = 'fa fa-bullhorn'
xadmin.site.register(EventMember, EventMemberAdmin)


from xadmin.views.form import FormAdminView
from dynamic_forms.forms import FormModelForm

class EventFormView(FormAdminView):
    form = FormModelForm
    form_template = 'event/show.html'
    title = '活动通知'

    def init_request(self, event_id, *args, **kwargs):
        self.form_model = Event.objects.get(id=event_id)
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

xadmin.site.register_view(r'^event/show/(\d+)$', EventFormView, name='event_show')

