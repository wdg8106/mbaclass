# coding=utf-8
from django import forms
import xadmin
from xadmin.layout import TabHolder, Tab, Fieldset
from xadmin.forms import AdminAuthenticationForm

from .models import Member

class MemberAdmin(object):

    def show_avatar(self, event):
        return event.avatar and '<img src="%s" height="30"/>' % event.avatar.url or ''
    show_avatar.short_description = "头像"
    show_avatar.allow_tags = True

    list_display = ('number', 'show_avatar', 'username', 'email', 'qq', 'gender', 'title')
    list_filter = ('username', 'email', 'qq', 'gender', 'classnum', 'mobile', 'birthday')

    search_fields = ('number', 'username', 'email')

    ordering = ('number',)
    style_fields = {'user_permissions': 'm2m_transfer', 'gender': 'radio-inline'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    exclude = ('last_login',)

    form_layout = (
        TabHolder(
            Tab('必填项目',
                Fieldset('个人信息',
                    'number', 'username', 'avatar', 'classnum', 'birthday', 'gender', 'is_active',
                    description="个人注册所需信息"
                ),
                Fieldset('联系方式',
                    'email', 'qq', 'mobile', 'weixin',
                    description="务必仔细填写您的联系方式，以便接受通知"
                ),
                css_id='comm'
            ),
            Tab('权限分配',
                'password',
                'groups', 'user_permissions',
                'is_superuser',
                css_id='permission'
            ),
            Tab('选填项目',
                'title', 'industry', 'position',
                'is_party', 'is_direct', 'is_move_hukou',
                'note',
                css_id='option'
            ),
        ),
    )

try:
    xadmin.site.unregister(Member)
except Exception, e:
    pass
xadmin.site.register(Member, MemberAdmin)

class MBANumberField(forms.CharField):

    def to_python(self, value):
        value = super(MBANumberField, self).to_python(value)
        return value.upper()

class MBAAdminAuthenticationForm(AdminAuthenticationForm):
    username = MBANumberField(max_length=254, label="学号")

class LoginSetting(object):
    title = '北航MBA信息管理系统'
    login_form = MBAAdminAuthenticationForm
    login_template = 'mbaclass/login.html'
xadmin.site.register(xadmin.views.LoginView, LoginSetting)
