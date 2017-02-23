# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 21:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='amc_10_scores',
            field=models.CharField(default=datetime.datetime(2016, 7, 28, 21, 3, 45, 649902, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='amc_8_scores',
            field=models.CharField(default='-/24,-/24,-/24;-/24,-/24,-/24;-/24,-/24,-/24;-/24,-/24,-/24;-/24,-/24,-/24', max_length=100),
            preserve_default=False,
        ),
    ]