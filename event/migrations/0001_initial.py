# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=200, verbose_name='\u901a\u77e5\u6458\u8981')),
                ('content', models.TextField(verbose_name='\u901a\u77e5\u5185\u5bb9')),
                ('public_time', models.DateTimeField(auto_now=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('use_qq', models.BooleanField(default=True, verbose_name='QQ\u901a\u77e5')),
                ('use_weixin', models.BooleanField(default=True, verbose_name='\u5fae\u4fe1\u901a\u77e5')),
                ('use_sms', models.BooleanField(default=False, verbose_name='\u77ed\u4fe1\u901a\u77e5')),
                ('sms_delay', models.IntegerField(default=60, help_text='\u7ecf\u8fc7\u591a\u957f\u65f6\u95f4\uff08\u5206\u949f\uff09\u540c\u5b66\u6ca1\u6709\u54cd\u5e94\u540e\uff0c\u8fdb\u884c\u77ed\u4fe1\u901a\u77e5', verbose_name='\u77ed\u4fe1\u901a\u77e5\u5ef6\u65f6')),
                ('author', models.ForeignKey(related_name=b'public_events', verbose_name='\u53d1\u5e03\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u901a\u77e5',
                'verbose_name_plural': '\u901a\u77e5',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_response', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u56de\u5e94')),
                ('event', models.ForeignKey(verbose_name='\u901a\u77e5', to='event.Event')),
                ('member', models.ForeignKey(verbose_name='\u6210\u5458', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u901a\u77e5\u53cd\u9988',
                'verbose_name_plural': '\u901a\u77e5\u53cd\u9988',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='event.EventMember'),
            preserve_default=True,
        ),
    ]
