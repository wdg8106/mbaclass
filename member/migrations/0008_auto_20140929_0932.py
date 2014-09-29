# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20140926_0642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='name',
        ),
        migrations.AddField(
            model_name='member',
            name='username',
            field=models.CharField(default='\u7ba1\u7406\u5458', max_length=30, verbose_name=b'\xe6\x80\xa7\xe5\x90\x8d'),
            preserve_default=False,
        ),
    ]
