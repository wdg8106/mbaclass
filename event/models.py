# coding=utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import escape, mark_safe
from django.utils.encoding import force_text

try:  # pragma: no cover
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from django.utils.datastructures import SortedDict as OrderedDict

import json

from member.models import Member
from dynamic_forms.models import FormModel

from weixin.pyweixin import wx

import uuid
from DjangoUeditor.models import UEditorField

from sorl.thumbnail.fields import ImageWithThumbnailsField

from dynamic_forms.actions import action_registry
from dynamic_forms.conf import settings
from dynamic_forms.fields import TextMultiSelectField
from dynamic_forms.formfields import formfield_registry

# Create your models here.
class Event(models.Model):
    title = models.CharField(u'通知标题', max_length=200)

    pic = ImageWithThumbnailsField(u'通知图标', upload_to=lambda m, name: "images/event/%s.%s" % (
        uuid.uuid4(), name.split('.')[-1]), blank=True, null=True,
            thumbnail={'size': (148, 148), 'extension': 'jpg'},
            extra_thumbnails={
                'list': {'size': (34, 34), 'options': ['crop', 'upscale'], 'extension': 'jpg'},
                'phone': {'size': (148, 148), 'extension': 'jpg'},
            }, )

    slug = models.TextField(u'通知摘要', blank=True)
    content = UEditorField(u'通知内容', height=300, toolbars="full", imagePath="event/img/", filePath="event/file/", blank=False)

    public_time = models.DateTimeField(u'发布时间', auto_now=True)

    event_type = models.CharField(u'通知类型', max_length=20, choices=(('notic', u'通知'), ('poll', u'投票'), ('sign', u'报名'), ('info', u'填表'), ('other', u'其它')))

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
        return self.title

    def get_fields_as_dict(self):
        return OrderedDict(self.fields.values_list('name', 'label').all())

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name

class EventField(models.Model):
    event = models.ForeignKey(Event, verbose_name=u'通知', on_delete=models.CASCADE, related_name='fields')
    field_type = models.CharField('字段类型', max_length=255, choices=formfield_registry.get_as_choices())
    label = models.CharField('显示名称', max_length=20)
    name = models.SlugField('字段名称', max_length=50, blank=True)
    _options = models.TextField('选项', blank=True, null=True)
    position = models.SmallIntegerField('显示位置', blank=True, default=0)

    class Meta:
        ordering = ['event', 'position']
        unique_together = ("event", "name",)
        verbose_name = '通知字段'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.label

    def generate_form_field(self, form):
        field_type_cls = formfield_registry.get(self.field_type)
        field = field_type_cls(**self.get_form_field_kwargs())
        field.contribute_to_form(form)
        return field

    def get_form_field_kwargs(self):
        kwargs = self.options
        kwargs.update({
            'name': self.name,
            'label': self.label,
        })
        return kwargs

    @property
    def options(self):
        """Options passed to the form field during construction."""
        if not hasattr(self, '_options_cached'):
            self._options_cached = {}
            if self._options:
                try:
                    self._options_cached = json.loads(self._options)
                except ValueError:
                    pass
        return self._options_cached

    @options.setter
    def options(self, opts):
        if hasattr(self, '_options_cached'):
            del self._options_cached
        self._options = json.dumps(opts)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = slugify(self.label)

        given_options = self.options
        field_type_cls = formfield_registry.get(self.field_type)
        invalid = set(self.options.keys()) - set(field_type_cls._meta.keys())
        if invalid:
            for key in invalid:
                del given_options[key]
            self.options = given_options

        super(EventField, self).save(*args, **kwargs)

class EventMember(models.Model):
    event = models.ForeignKey(Event, verbose_name=u'通知')
    member = models.ForeignKey(Member, verbose_name=u'成员')

    is_response = models.BooleanField(u'是否已经回应', default=False)
    status = models.SmallIntegerField(u'状态', default=1, choices=((1,'未查看'), (2,'已查看'), (3,'已提交')))
    is_send_wx = models.BooleanField(u'已发送微信', default=False)
    is_send_sms = models.BooleanField(u'已发送短信', default=False)

    value = models.TextField(u'提交数据', blank=True, default='')

    def __str__(self):
        return str(self.member)

    class Meta:
        unique_together = ("event", "member",)
        verbose_name = '通知反馈'
        verbose_name_plural = verbose_name

    @property
    def json_value(self):
        return OrderedDict(sorted(json.loads(self.value).items()))

    def pretty_value(self):
        try:
            output = ['<dl>']
            for k, v in self.json_value.items():
                output.append('<dt>%(key)s</dt><dd>%(value)s</dd>' % {
                    'key': escape(force_text(k)),
                    'value': escape(force_text(v)),
                })
            output.append('</dl>')
            return mark_safe(''.join(output))
        except ValueError:
            return self.value
    pretty_value.allow_tags = True

    def send_wx(self):
        e = self.event
        wx.send_msg({
            "touser": self.member.number,
            "msgtype": "news",
            "agentid": "1",
            "news": {
               "articles": [{
                   "title": e.title,
                   "description": e.slug,
                   "url": wx.auth_url('http://182.92.101.78/event/show/%d' % e.pk),
                   "picurl": e.pic and e.pic.url or "http://www.sucai123.com/sucai/img2/193/064.jpg"
               }]
            }
        })
        self.is_send_wx = True

    def save(self, *args, **kwargs):
        if not self.is_send_wx and self.event.use_weixin:
            # 发送微信
            self.send_wx()
        super(EventMember, self).save(*args, **kwargs)

class EventForm(models.Model):
    event = models.ForeignKey(Event, verbose_name=u'通知')
    form = models.ForeignKey(FormModel, verbose_name=u'表单')

    def __unicode__(self):
        return "%s通知的%s表单" % (self.event, self.form)

    class Meta:
        verbose_name = '通知表单'
        verbose_name_plural = verbose_name



