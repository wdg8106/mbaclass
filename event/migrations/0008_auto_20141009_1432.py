# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_auto_20141009_1420'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventmember',
            unique_together=set([('event', 'member')]),
        ),
    ]
