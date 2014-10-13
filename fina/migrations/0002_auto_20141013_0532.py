# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fina', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetail',
            name='note',
            field=models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AlterField(
            model_name='memberaccount',
            name='amount',
            field=models.DecimalField(default=0, verbose_name='\u8d26\u6237\u4f59\u989d', max_digits=10, decimal_places=2),
        ),
    ]
