# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0005_auto_20160723_0801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='department',
        ),
        migrations.AddField(
            model_name='myuser',
            name='intro',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sexuality',
            field=models.BooleanField(default=True),
        ),
    ]
