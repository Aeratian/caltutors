# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_student_num_tries'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
