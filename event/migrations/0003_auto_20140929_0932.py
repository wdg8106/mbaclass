# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u901a\u77e5\u4eba', through='event.EventMember'),
        ),
    ]
