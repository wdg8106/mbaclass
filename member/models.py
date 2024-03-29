# coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

import mptt
from mptt.fields import TreeForeignKey, TreeOneToOneField, TreeManyToManyField
from mptt.models import MPTTModel
from mptt.managers import TreeManager

def avatar_upload_to(m, name):
    return "images/avatar/%s.%s" % (m.number, name.split('.')[-1])
        
class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(u'电子邮件', blank=False, unique=True)

    avatar = models.ImageField(u'头像', upload_to=avatar_upload_to, blank=True, null=True)

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
    departments = models.ManyToManyField('Department', verbose_name=u'所属部门', related_name='members', null=True, blank=True)

    is_staff = True

    objects = UserManager()

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['email', 'username']
    
    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = verbose_name


class Department(MPTTModel):
    name = models.CharField(u'名称', max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name=u'父级部门', null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def display_name(self):
        return ('---' * self.level) + self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

