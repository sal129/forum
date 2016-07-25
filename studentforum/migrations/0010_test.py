# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0009_myuser_portrait'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(height_field=200, null=True, upload_to='/localStorage/portrait', width_field=200)),
                ('title', models.CharField(default=' test', max_length=100)),
            ],
        ),
    ]