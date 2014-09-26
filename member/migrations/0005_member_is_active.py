# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20140926_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u6fc0\u6d3b\u8d26\u53f7'),
            preserve_default=True,
        ),
    ]
