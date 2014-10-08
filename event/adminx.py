# coding=utf-8
import xadmin
from xadmin.layout import *
from xadmin.plugins.inline import Inline
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from .models import Event, EventMember, EventForm
from django.forms import Media

class EventMemberInline(object):
    model = EventMember
    readonly_fields = ('is_response', )
    extra = 1    

class EventFormInline(object):
    model = EventForm
    extra = 1    

class EventAdmin(object):
    list_display = ('slug', 'public_time', 'start_time', 'end_time', 'author', 'is_active')
    list_filter = ('public_time', 'start_time', 'end_time', 'author', 'is_active')

    search_fields = ('slug',)

    model_icon = 'fa fa-bullhorn'

    user_fields = ('author',)

    inlines = (EventMemberInline, EventFormInline, )

    formfield_overrides = {UEditorField: {'widget': UEditorWidget({'width':'100%', 'height':300, 'toolbars':"full", 'imagePath':"event/img/", 'filePath':"event/file/"})}}

xadmin.site.register(Event, EventAdmin)

class EventMemberAdmin(object):
    list_display = ('event', 'member', 'is_response')
    list_filter = ('is_response',)
    readonly_fields = ('is_response', )

    model_icon = 'fa fa-bullhorn'
xadmin.site.register(EventMember, EventMemberAdmin)

class EventFormAdmin(object):
    list_display = ('event', 'form')

    model_icon = 'fa fa-bullhorn'
xadmin.site.register(EventForm, EventFormAdmin)

from dynamic_forms.admin import AdminFormModelForm, AdminFormFieldInlineForm
from dynamic_forms.models import FormModel, FormFieldModel

class FormFieldModelInlineAdmin(object):
    model = FormFieldModel
    extra = 1
    style = 'accordion'
    form = AdminFormFieldInlineForm
    list_display = ('field_type', 'name', 'label')

class FormModelAdmin(object):
    form = AdminFormModelForm
    inlines = (FormFieldModelInlineAdmin,)
    list_display = ('name', 'submit_url', 'success_url', 'allow_display')
    relfield_style = 'fk-ajax'

xadmin.site.register(FormModel, FormModelAdmin)


from xadmin.views.form import FormAdminView
from dynamic_forms.forms import FormModelForm

class EventFormView(FormAdminView):
    form = FormModelForm

    def init_request(self, form_id, *args, **kwargs):
        self.form_model = FormModel.objects.get(id=form_id)
        self.title = self.form_model.name
        self.prepare_form()

    def get_form_datas(self):
        data = super(EventFormView, self).get_form_datas()
        data['model'] = self.form_model
        return data

xadmin.site.register_view(r'^event/show/(\d+)$', EventFormView, name='event_show')

