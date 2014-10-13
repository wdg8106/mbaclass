# coding=utf-8
import xadmin
from .models import Account, MemberAccount, AccountDetail

class AccountAdmin(object):
    list_display = ('name', 'total')
    model_icon = 'fa fa-money'
xadmin.site.register(Account, AccountAdmin)

class MemberAccountAdmin(object):
    list_display = ('account', 'member', 'amount')
    list_filter = ('account', 'amount')
    readonly_fields = ('amount', )
    search_fields = ('member__number', 'member__username')
    model_icon = 'fa fa-credit-card'
    relfield_style = 'fk-ajax'
xadmin.site.register(MemberAccount, MemberAccountAdmin)

class AccountDetailAdmin(object):
    list_display = ('member_account', 'charge', 'charge_time', 'title', 'event')
    list_filter = ('member_account__account', 'member_account__member', 'charge', 'charge_time', 'event')
    search_fields = ('title',)
    model_icon = 'fa fa-table'
xadmin.site.register(AccountDetail, AccountDetailAdmin)