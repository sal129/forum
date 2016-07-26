# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0006_auto_20160726_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplytoReply',
            fields=[
                ('id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('content', models.TextField(null=True, verbose_name='楼中楼回帖')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('PID', models.ForeignKey(to='studentforum.Reply')),
                ('author', models.ForeignKey(to='studentforum.MyUser')),
            ],
        ),
    ]
