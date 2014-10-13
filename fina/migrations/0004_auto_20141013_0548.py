# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fina', '0003_auto_20141013_0540'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='memberaccount',
            unique_together=set([('account', 'member')]),
        ),
    ]
