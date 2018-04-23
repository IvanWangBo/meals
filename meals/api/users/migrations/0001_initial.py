# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-04-23 18:16
from __future__ import unicode_literals

import api.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('real_name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('admin_type', models.IntegerField(default=0)),
                ('gender', models.IntegerField(default=0)),
                ('company_id', models.IntegerField(default=0)),
                ('department_id', models.IntegerField(default=0)),
                ('is_enabled', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', api.users.models.UserManager()),
            ],
        ),
    ]
