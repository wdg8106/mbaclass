# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='members',
            field=models.ManyToManyField(related_name=b'departments', null=True, verbose_name='\u90e8\u95e8\u6210\u5458', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='department',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name=b'children', verbose_name='\u7236\u7ea7\u90e8\u95e8', blank=True, to='member.Department', null=True),
        ),
    ]
