# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-13 16:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_auto_20180514_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dishes',
            name='count',
        ),
    ]
