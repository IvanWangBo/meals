# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-06-09 06:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_mealorders_time_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealorders',
            name='order_data',
            field=models.DateField(default=datetime.date(2018, 6, 10)),
        ),
        migrations.AddField(
            model_name='mealorders',
            name='screen_order_id',
            field=models.CharField(default=b'', max_length=256),
        ),
    ]
