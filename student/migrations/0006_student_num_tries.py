# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_saved_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='num_tries',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
