# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_auto_20141009_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='is_send_sms',
            field=models.BooleanField(default=False, verbose_name='\u5df2\u53d1\u9001\u77ed\u4fe1'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventmember',
            name='is_send_wx',
            field=models.BooleanField(default=False, verbose_name='\u5df2\u53d1\u9001\u5fae\u4fe1'),
            preserve_default=True,
        ),
    ]
