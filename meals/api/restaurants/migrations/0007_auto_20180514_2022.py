# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-14 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0006_auto_20180514_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timerange',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='timerange',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
