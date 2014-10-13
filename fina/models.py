# coding=utf-8
import datetime
from django.db import models

try:  # pragma: no cover
    from django.db.transaction import atomic
except ImportError:  # pragma: no cover
    from django.db.transaction import commit_on_success as atomic

from member.models import Member
from event.models import Event

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
    charge_time = models.DateTimeField(u'时间')
    title = models.CharField(u'名称', max_length=200)
    note = models.TextField(u'备注', null=True, blank=True)
    event = models.ForeignKey(Event, verbose_name=u'活动', null=True, blank=True)

    def save(self, *args, **kwargs):
        with atomic():
            if not self.pk:
                self.member_account.amount += self.charge
                self.member_account.save()
            super(AccountDetail, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '账户记录'
        verbose_name_plural = verbose_name

def charge(account, member, amount, title, event=None, note=None):
    am, created = MemberAccount.objects.get_or_create(account=account, member=member)
    AccountDetail(member_account=am, charge=charge, charge_time=datetime.datetime.now(), title=title, \
        note=note, event=event).save()

