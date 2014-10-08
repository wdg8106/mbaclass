# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_forms', '0003_auto_20140916_1433'),
        ('event', '0003_auto_20140929_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(verbose_name='\u901a\u77e5', to='event.Event')),
                ('form', models.ForeignKey(verbose_name='\u8868\u5355', to='dynamic_forms.FormModel')),
            ],
            options={
                'verbose_name': '\u901a\u77e5\u8868\u5355',
                'verbose_name_plural': '\u901a\u77e5\u8868\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='forms',
            field=models.ManyToManyField(to='dynamic_forms.FormModel', verbose_name='\u8868\u5355', through='event.EventForm'),
            preserve_default=True,
        ),
    ]
