# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0011_auto_20141013_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u8d26\u6237\u540d\u79f0')),
                ('alipay', models.CharField(max_length=100, null=True, verbose_name='\u652f\u4ed8\u5b9d\u8d26\u53f7', blank=True)),
            ],
            options={
                'verbose_name': '\u8d26\u6237',
                'verbose_name_plural': '\u8d26\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge', models.DecimalField(verbose_name='\u91d1\u989d', max_digits=10, decimal_places=2)),
                ('charge_time', models.DateTimeField(verbose_name='\u65f6\u95f4')),
                ('title', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
                ('note', models.TextField(verbose_name='\u5907\u6ce8')),
                ('event', models.ForeignKey(verbose_name='\u6d3b\u52a8', blank=True, to='event.Event', null=True)),
            ],
            options={
                'verbose_name': '\u8d26\u6237\u8bb0\u5f55',
                'verbose_name_plural': '\u8d26\u6237\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(verbose_name='\u8d26\u6237\u4f59\u989d', max_digits=10, decimal_places=2)),
                ('account', models.ForeignKey(verbose_name='\u8d26\u6237', to='fina.Account')),
                ('member', models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4e2a\u4eba\u8d26\u6237',
                'verbose_name_plural': '\u4e2a\u4eba\u8d26\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='accountdetail',
            name='member_account',
            field=models.ForeignKey(verbose_name='\u8d26\u6237', to='fina.MemberAccount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237', through='fina.MemberAccount'),
            preserve_default=True,
        ),
    ]
