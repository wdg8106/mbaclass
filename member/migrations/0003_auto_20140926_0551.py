# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20140926_0329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': '\u6210\u5458', 'verbose_name_plural': '\u6210\u5458'},
        ),
        migrations.RemoveField(
            model_name='member',
            name='order',
        ),
        migrations.AddField(
            model_name='member',
            name='avatar',
            field=models.ImageField(default='.', upload_to=b'avatar/', verbose_name='\u5934\u50cf', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='birthday',
            field=models.DateField(default=datetime.date(2014, 9, 26), verbose_name='\u51fa\u751f\u65e5\u671f'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='classnum',
            field=models.PositiveIntegerField(default=4, verbose_name='\u73ed\u7ea7', choices=[(1, '\u4e00\u73ed'), (2, '\u4e8c\u73ed'), (3, '\u4e09\u73ed'), (4, '\u56db\u73ed')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(default='m', max_length=1, verbose_name='\u6027\u522b', choices=[(b'm', '\u7537'), (b'f', '\u5973')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='industry',
            field=models.CharField(default='', max_length=50, verbose_name='\u884c\u4e1a', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='is_direct',
            field=models.BooleanField(default=False, verbose_name='\u5b9a\u5411'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='is_move_hukou',
            field=models.BooleanField(default=False, verbose_name='\u8fc1\u79fb\u6237\u53e3'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='is_party',
            field=models.BooleanField(default=False, verbose_name='\u515a\u5458'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='number',
            field=models.CharField(default='MB1408400', help_text='MBA\u5b66\u53f7\uff0c\u4f8b\u5982MB1408434', unique=True, max_length=12, verbose_name='\u5b66\u53f7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='position',
            field=models.CharField(default='', max_length=20, verbose_name='\u5de5\u4f5c\u804c\u52a1', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='qq',
            field=models.CharField(default='000000', max_length=15, verbose_name='QQ\u53f7\u7801'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='title',
            field=models.CharField(max_length=10, null=True, verbose_name='\u73ed\u7ea7\u804c\u52a1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='weixin',
            field=models.CharField(default='123', max_length=25, verbose_name='\u5fae\u4fe1\u53f7'),
            preserve_default=False,
        ),
    ]
