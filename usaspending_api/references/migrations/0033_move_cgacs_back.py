# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-29 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0032_auto_20190918_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='FREC',
            fields=[
                ('frec_code', models.TextField(primary_key=True, serialize=False)),
                ('agency_name', models.TextField()),
                ('agency_abbreviation', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'frec',
            },
        ),
    ]
