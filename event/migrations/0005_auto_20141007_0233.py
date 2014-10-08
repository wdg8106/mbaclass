# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20140930_0146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventmember',
            options={'verbose_name': '\u901a\u77e5\u6210\u5458', 'verbose_name_plural': '\u901a\u77e5\u6210\u5458'},
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=DjangoUeditor.models.UEditorField(verbose_name='\u901a\u77e5\u5185\u5bb9'),
        ),
    ]
