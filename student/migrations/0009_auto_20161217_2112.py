# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-18 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20160819_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='usaco_bronze_locks',
            field=models.CharField(default='aaa', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='usaco_bronze_scores',
            field=models.CharField(default='aaa', max_length=500),
            preserve_default=False,
        ),
    ]
