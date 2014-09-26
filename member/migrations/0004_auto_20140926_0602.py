# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20140926_0551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='member',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='member',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='member',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='username',
        ),
        migrations.AddField(
            model_name='member',
            name='mobile',
            field=models.CharField(default='13888888888', max_length=20, verbose_name='\u624b\u673a\u53f7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(default='\u7ba1\u7406\u5458', unique=True, max_length=30, verbose_name=b'\xe6\x80\xa7\xe5\x90\x8d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name='\u7535\u5b50\u90ae\u4ef6'),
        ),
        migrations.AlterField(
            model_name='member',
            name='weixin',
            field=models.CharField(max_length=25, null=True, verbose_name='\u5fae\u4fe1\u53f7', blank=True),
        ),
    ]
