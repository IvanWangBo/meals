# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-14 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0008_auto_20180514_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurants',
            name='is_enabled',
            field=models.IntegerField(default=True),
        ),
    ]
