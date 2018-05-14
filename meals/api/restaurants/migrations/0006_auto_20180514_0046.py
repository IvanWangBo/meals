# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-13 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_remove_dishes_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timerange',
            name='dish_id',
        ),
        migrations.AddField(
            model_name='dishes',
            name='support_times',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
