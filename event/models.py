# coding=utf-8
from django.db import models

from member.models import Member
from dynamic_forms.models import FormModel

from DjangoUeditor.models import UEditorField

# Create your models here.
class Event(models.Model):
    slug = models.CharField(u'通知摘要', max_length=200)
    content = UEditorField(u'通知内容', height=300, toolbars="full", imagePath="event/img/", filePath="event/file/", blank=False)

    public_time = models.DateTimeField(u'发布时间', auto_now=True)

    start_time = models.DateTimeField(u'开始时间')
    end_time = models.DateTimeField(u'结束时间')

    use_qq = models.BooleanField(u'QQ通知', default=True)
    use_weixin = models.BooleanField(u'微信通知', default=True)
    use_sms = models.BooleanField(u'短信通知', default=False)

    sms_delay = models.IntegerField(u'短信通知延时', default=60, help_text=u'经过多长时间（分钟）同学没有响应后，进行短信通知')

    is_active = models.BooleanField(u'有效', default=True)

    author = models.ForeignKey(Member, verbose_name=u'发布者', related_name='public_events')

    members = models.ManyToManyField(Member, verbose_name=u'通知人', through='EventMember', through_fields=('event', 'member'))
    forms = models.ManyToManyField(FormModel, verbose_name=u'表单', through='EventForm', through_fields=('event', 'form'))

    def __unicode__(self):
        return self.slug

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name

class EventMember(models.Model):
    event = models.ForeignKey(Event, verbose_name=u'通知')
    member = models.ForeignKey(Member, verbose_name=u'成员')

    is_response = models.BooleanField(u'是否已经回应', default=False)

    def __unicode__(self):
        return "%s对通知%s的应答" % (self.member, self.event)

    class Meta:
        verbose_name = '通知成员'
        verbose_name_plural = verbose_name

class EventForm(models.Model):
    event = models.ForeignKey(Event, verbose_name=u'通知')
    form = models.ForeignKey(FormModel, verbose_name=u'表单')

    def __unicode__(self):
        return "%s通知的%s表单" % (self.event, self.form)

    class Meta:
        verbose_name = '通知表单'
        verbose_name_plural = verbose_name



