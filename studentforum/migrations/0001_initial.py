# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, default=4, serialize=False)),
                ('intro', models.TextField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name=' 标题', max_length=100)),
                ('content', models.TextField(verbose_name=' 内容', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(to='studentforum.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('content', models.TextField(verbose_name=' 回帖内容', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('PID', models.ForeignKey(to='studentforum.Post')),
                ('author', models.ForeignKey(to='studentforum.MyUser')),
            ],
        ),
    ]
