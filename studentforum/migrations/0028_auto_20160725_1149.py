# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0027_auto_20160725_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='photo',
            field=models.ImageField(height_field='url_height', null=True, upload_to='studentforum/portraits', width_field='url_width'),
        ),
    ]
