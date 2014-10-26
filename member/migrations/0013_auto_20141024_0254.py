# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_auto_20141023_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='members',
        ),
        migrations.AddField(
            model_name='member',
            name='departments',
            field=models.ManyToManyField(related_name=b'members', null=True, verbose_name='\u6240\u5c5e\u90e8\u95e8', to='member.Department', blank=True),
            preserve_default=True,
        ),
    ]
