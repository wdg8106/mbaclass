# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20141011_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(default='notic', max_length=20, verbose_name='\u901a\u77e5\u7c7b\u578b', choices=[(b'notic', '\u901a\u77e5'), (b'poll', '\u6295\u7968'), (b'sign', '\u62a5\u540d'), (b'info', '\u586b\u8868'), (b'other', '\u5176\u5b83')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='pic',
            field=models.ImageField(default='', upload_to=b'eventicon/', verbose_name='\u901a\u77e5\u56fe\u6807', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='asdad', max_length=200, verbose_name='\u901a\u77e5\u6807\u9898'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.TextField(verbose_name='\u901a\u77e5\u6458\u8981', blank=True),
        ),
    ]
