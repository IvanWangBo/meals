# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-24 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_mealorders_is_canceled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mealorders',
            old_name='state',
            new_name='status',
        ),
    ]
