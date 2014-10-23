# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fina', '0006_accountdetail_is_send_wx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetail',
            name='is_send_wx',
            field=models.BooleanField(default=False, verbose_name='\u5df2\u5fae\u4fe1\u901a\u77e5'),
        ),
    ]
