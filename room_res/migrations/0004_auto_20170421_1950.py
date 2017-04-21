# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-21 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('room_res', '0003_auto_20170421_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservations',
            name='date',
        ),
        migrations.RemoveField(
            model_name='reservations',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='reservations',
            name='start_time',
        ),
        migrations.AddField(
            model_name='reservations',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservations',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
    ]