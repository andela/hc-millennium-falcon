# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-20 13:09
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180519_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]