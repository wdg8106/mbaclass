# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_member_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='note',
            field=models.TextField(null=True, verbose_name='\u5907\u6ce8'),
            preserve_default=True,
        ),
    ]
