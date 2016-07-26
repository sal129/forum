# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyToReply',
            fields=[
                ('id', models.AutoField(primary_key=True, unique=True, serialize=False)),
                ('content', models.TextField(null=True, verbose_name='楼中楼回帖')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('PID', models.ForeignKey(to='studentforum.Reply')),
                ('author', models.ForeignKey(to='studentforum.MyUser')),
            ],
        ),
    ]
