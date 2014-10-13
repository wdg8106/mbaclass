# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20141011_0721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventmember',
            options={'verbose_name': '\u901a\u77e5\u53cd\u9988', 'verbose_name_plural': '\u901a\u77e5\u53cd\u9988'},
        ),
        migrations.AlterField(
            model_name='event',
            name='pic',
            field=models.ImageField(upload_to=event.models.pic_upload_to, null=True, verbose_name='\u901a\u77e5\u56fe\u6807', blank=True),
        ),
    ]
