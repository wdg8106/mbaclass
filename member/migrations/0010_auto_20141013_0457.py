# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import member.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_auto_20141011_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(upload_to=member.models.avatar_upload_to, null=True, verbose_name='\u5934\u50cf', blank=True),
        ),
    ]
