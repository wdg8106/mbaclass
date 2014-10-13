# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fina', '0002_auto_20141013_0532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='members',
        ),
        migrations.AlterField(
            model_name='memberaccount',
            name='account',
            field=models.ForeignKey(related_name=b'members', verbose_name='\u8d26\u6237', to='fina.Account'),
        ),
    ]
