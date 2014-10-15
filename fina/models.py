# coding=utf-8
import datetime
from django.db import models

try:  # pragma: no cover
    from django.db.transaction import atomic
except ImportError:  # pragma: no cover
    from django.db.transaction import commit_on_success as atomic

from member.models import Member
from event.models import Event
from weixin.pyweixin import wx

class Account(models.Model):
    name = models.CharField(u'账户名称', max_length=64)
    alipay = models.CharField(u'支付宝账号', max_length=100, blank=True, null=True)

    def total(self):
        return sum([m.amount for m in self.members.all()])
    total.short_description = u"账户余额"

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = verbose_name

class MemberAccount(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'账户', related_name="members")
    member = models.ForeignKey(Member, verbose_name=u'用户')
    amount = models.DecimalField(u'账户余额', max_digits=10, decimal_places=2, default=0)

    def __unicode__(self):
        return u'%s在%s中的账户' % (self.member.username, self.account.name)

    class Meta:
        unique_together = ("account", "member",)
        verbose_name = '个人账户'
        verbose_name_plural = verbose_name

class AccountDetail(models.Model):
    member_account = models.ForeignKey(MemberAccount, verbose_name=u'账户')
    charge = models.DecimalField(u'金额', max_digits=10, decimal_places=2)
    charge_time = models.DateField(u'时间')
    title = models.CharField(u'名称', max_length=200)
    note = models.TextField(u'备注', null=True, blank=True)
    event = models.ForeignKey(Event, verbose_name=u'活动', null=True, blank=True)
    record_time = models.DateTimeField(u'记录时间', auto_now=True)
    is_send_wx = models.BooleanField(u'已微信通知', default=False)

    def __unicode__(self):
        return unicode(self.member_account.member) + '的账户明细'

    def save(self, *args, **kwargs):
        with atomic():
            if not self.pk:
                self.member_account.amount += self.charge
                self.member_account.save()

            if not self.is_send_wx:
                mode = (self.charge > 0)
                content = u'您的账户%s刚刚%s%.2f元，用于%s，账户余额为%.2f元。\n您可以查看账户明细了解更多信息，如有疑问请联系班委。' % \
                    (str(self.member_account.account), (mode and u'充入' or u'扣除'), self.charge, self.title, self.member_account.amount)
                wx.send_msg({
                    "touser": self.member_account.member.number,
                    "msgtype": "text",
                    "agentid": "2",
                    "text": {
                        "content": content
                    }
                })
                self.is_send_wx = True

            super(AccountDetail, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '账户记录'
        verbose_name_plural = verbose_name

def charge(account, member, amount, title, charge_date=None, event=None, note=None):
    am, created = MemberAccount.objects.get_or_create(account=account, member=member)
    AccountDetail(member_account=am, charge=amount, charge_time=charge_date or datetime.date.today(), title=title, \
        note=note, event=event).save()

def charges(account, members, amount, title, charge_date=None, event=None, note=None):
    for m in members:
        charge(account, m, amount, title, charge_date, event, note)

