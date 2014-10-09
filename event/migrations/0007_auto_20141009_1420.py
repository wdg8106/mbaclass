# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20141009_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='status',
            field=models.SmallIntegerField(default=1, verbose_name='\u72b6\u6001', choices=[(1, b'\xe6\x9c\xaa\xe6\x9f\xa5\xe7\x9c\x8b'), (2, b'\xe5\xb7\xb2\xe6\x9f\xa5\xe7\x9c\x8b'), (3, b'\xe5\xb7\xb2\xe6\x8f\x90\xe4\xba\xa4')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventmember',
            name='value',
            field=models.TextField(default=b'', verbose_name='\u63d0\u4ea4\u6570\u636e', blank=True),
            preserve_default=True,
        ),
    ]
