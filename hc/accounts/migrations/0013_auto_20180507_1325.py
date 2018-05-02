# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-07 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20180507_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reports_period',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='reports_allowed',
            field=models.BooleanField(default=True),
        ),
    ]
