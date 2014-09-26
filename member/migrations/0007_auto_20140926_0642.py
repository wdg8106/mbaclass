# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_member_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='note',
            field=models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
    ]
