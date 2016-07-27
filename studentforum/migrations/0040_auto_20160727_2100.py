# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0039_auto_20160727_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='userFromID',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='userToID',
        ),
        migrations.AddField(
            model_name='letter',
            name='userFrom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reverse_from', to='studentforum.MyUser'),
        ),
        migrations.AddField(
            model_name='letter',
            name='userTo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reverse_to', to='studentforum.MyUser'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='collectPst',
            field=models.ManyToManyField(to='studentforum.Post'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='follow',
            field=models.ManyToManyField(to='studentforum.MyUser'),
        ),
    ]
