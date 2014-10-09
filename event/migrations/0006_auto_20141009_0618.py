# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20141007_0233'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_type', models.CharField(max_length=255, verbose_name=b'\xe5\xad\x97\xe6\xae\xb5\xe7\xb1\xbb\xe5\x9e\x8b', choices=[('dynamic_forms.formfields.BooleanField', 'Boolean'), ('dynamic_forms.formfields.ChoiceField', 'Choices'), ('dynamic_forms.formfields.DateField', 'Date'), ('dynamic_forms.formfields.DateTimeField', 'Date and Time'), ('dynamic_forms.formfields.EmailField', 'Email'), ('dynamic_forms.formfields.IntegerField', 'Integer'), ('dynamic_forms.formfields.MultiLineTextField', 'Multi Line Text'), ('dynamic_forms.formfields.SingleLineTextField', 'Single Line Text'), ('dynamic_forms.formfields.TimeField', 'Time')])),
                ('label', models.CharField(max_length=20, verbose_name=b'\xe6\x98\xbe\xe7\xa4\xba\xe5\x90\x8d\xe7\xa7\xb0')),
                ('name', models.SlugField(verbose_name=b'\xe5\xad\x97\xe6\xae\xb5\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('_options', models.TextField(null=True, verbose_name=b'\xe9\x80\x89\xe9\xa1\xb9', blank=True)),
                ('position', models.SmallIntegerField(default=0, verbose_name=b'\xe6\x98\xbe\xe7\xa4\xba\xe4\xbd\x8d\xe7\xbd\xae', blank=True)),
                ('event', models.ForeignKey(related_name=b'fields', verbose_name='\u901a\u77e5', to='event.Event')),
            ],
            options={
                'ordering': ['event', 'position'],
                'verbose_name': '\u901a\u77e5\u5b57\u6bb5',
                'verbose_name_plural': '\u901a\u77e5\u5b57\u6bb5',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventfield',
            unique_together=set([('event', 'name')]),
        ),
    ]
