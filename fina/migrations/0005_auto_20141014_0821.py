# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('fina', '0004_auto_20141013_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountdetail',
            name='record_time',
            field=models.DateTimeField(default=datetime.date(2014, 10, 14), verbose_name='\u8bb0\u5f55\u65f6\u95f4', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountdetail',
            name='charge_time',
            field=models.DateField(verbose_name='\u65f6\u95f4'),
        ),
    ]
