# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-06-09 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180609_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealorders',
            name='order_data',
            field=models.DateField(),
        ),
    ]