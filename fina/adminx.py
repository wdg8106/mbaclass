# coding=utf-8
import xadmin
import re
from django import forms
from django.core.exceptions import ValidationError
from xadmin.views.form import FormAdminView
from .models import Account, MemberAccount, AccountDetail, charges
from member.models import Member
from event.models import Event

class AccountAdmin(object):
    list_display = ('name', 'total')
    model_icon = 'fa fa-money'
xadmin.site.register(Account, AccountAdmin)

class MemberAccountAdmin(object):
    list_display = ('account', 'member', 'amount')
    list_filter = ('account', 'amount')
    search_fields = ('member__number', 'member__username')
    model_icon = 'fa fa-credit-card'
    relfield_style = 'fk-ajax'
    
    user_can_access_owned_objects_only = True
    user_owned_objects_field = 'member'
xadmin.site.register(MemberAccount, MemberAccountAdmin)

class AccountDetailAdmin(object):
    list_display = ('member_account', 'charge', 'charge_time', 'title', 'is_send_wx', 'event')
    list_filter = ('member_account__account', 'member_account__member', 'charge', 'charge_time', 'event')
    search_fields = ('title',)
    model_icon = 'fa fa-table'
    delete_models_batch = False

    aggregate_fields = {"charge": "sum"}
    user_can_access_owned_objects_only = True
    user_owned_objects_field = 'member_account__member'
xadmin.site.register(AccountDetail, AccountDetailAdmin)

class MembersField(forms.CharField):

    def to_python(self, value):
        ms = []
        for n in re.split('[,\t\n]',value):
            n = n.replace('\n','').replace('\r','').replace('\t','').replace(',','')
            try:
                ms.append(Member.objects.get(number=n))
            except Exception:
                ms.append(n)
        return ms

    def validate(self, value):
        super(MembersField, self).validate(value)
        miss = []
        for m in value:
            if type(m) is not Member:
                miss.append(m)
        if len(miss):
            raise ValidationError(','.join(miss) + ' 未找到对应的用户', code='miss_number')

class AccountBatForm(forms.Form):
    members = MembersField(label=u'用户ID', max_length=1024, widget=forms.Textarea, required=True, help_text=u'用逗号分隔')
    account = forms.IntegerField(label=u'选择账户', required=True)
    charge_time = forms.DateField(label=u'支付时间', required=True, widget=xadmin.widgets.AdminDateWidget)
    amount = forms.DecimalField(label=u'支付金额', required=True, max_digits=10, decimal_places=2)
    title = forms.CharField(label=u'支付说明', required=True, max_length=100)
    note = forms.CharField(label=u'备注', required=False)
    event = forms.IntegerField(label=u'关联活动', required=False)

class AccountFormView(FormAdminView):
    form = AccountBatForm
    title = '批量添加'

    def save_forms(self):
        data = self.form_obj.cleaned_data
        account = Account.objects.get(id=data['account'])
        if data['event']:
            eve = Event.objects.get(id=data['event'])
        else:
            eve = None
        charges(account, data['members'], amount=data['amount'], title=data['title'], \
            charge_date=data['charge_time'], event=eve, note=data['note'])

    def post_response(self):
        msg = u'账户明细导入成功'
        self.message_user(msg, 'success')

        return self.get_redirect_url()

xadmin.site.register_view(r'^fina/bat$', AccountFormView, name='fina_bat')

class AccountChargeForm(forms.Form):
    account = forms.IntegerField(label=u'选择账户', required=True)
    amount = forms.DecimalField(label=u'充值金额', required=True, max_digits=10, decimal_places=2)

class AccountChargeView(FormAdminView):
    form = AccountChargeForm
    title = '账户充值'

    def save_forms(self):
        data = self.form_obj.cleaned_data

    def post_response(self):
        msg = u'非常抱歉，支付接口正在申请中，该功能暂时无法使用。'
        self.message_user(msg, 'error')

        return self.get_redirect_url()

xadmin.site.register_view(r'^fina/charge$', AccountChargeView, name='fina_charge')
