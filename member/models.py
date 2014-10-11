# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from sorl.thumbnail.fields import ImageWithThumbnailsField

class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(u'电子邮件', blank=False, unique=True)

    avatar = ImageWithThumbnailsField(u'头像', upload_to=lambda m, name: "images/avatar/%s.%s" % (
        m.number, name.split('.')[-1]), blank=True, null=True,
            thumbnail={'size': (148, 148), 'extension': 'jpg'},
            extra_thumbnails={
                'list': {'size': (34, 34), 'options': ['crop', 'upscale'], 'extension': 'jpg'},
                'phone': {'size': (148, 148), 'extension': 'jpg'},
            })

    classnum = models.PositiveIntegerField(u'班级', choices=((1, u'一班'), (2, u'二班'), (3, u'三班'), (4, u'四班')))

    number = models.CharField(u'学号', max_length=12, help_text=u'MBA学号，例如MB1408434', null=False, blank=False, unique=True)

    username = models.CharField('姓名', max_length=30)

    qq = models.CharField(u'QQ号码', max_length=15, null=False, blank=False)
    mobile = models.CharField(u'手机号', max_length=20, null=False, blank=False)
    weixin = models.CharField(u'微信号', max_length=25, null=True, blank=True)

    birthday = models.DateField(u'出生日期', null=False)
    gender = models.CharField(u'性别', max_length=1, choices=(('m', u'男'), ('f', u'女')))

    is_party = models.BooleanField(u'党员', default=False)
    is_direct = models.BooleanField(u'定向', default=False)
    is_move_hukou = models.BooleanField(u'迁移户口', default=False)

    title = models.CharField(u'班级职务', max_length=10, null=True, blank=True)

    industry = models.CharField(u'行业', max_length=50, blank=True)
    position = models.CharField(u'工作职务', max_length=20, blank=True)

    is_active = models.BooleanField(u'激活账号', default=True)

    note = models.TextField(u'备注', null=True, blank=True)

    is_staff = True

    objects = UserManager()

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['email', 'username']
    
    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = verbose_name

