# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20140929_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='username',
            field=models.CharField(max_length=30, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d'),
        ),
    ]
