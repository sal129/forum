# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0005_post_supportnum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('pstNum', models.IntegerField(default=0)),
                ('collectNum', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ForWidgetTest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.CharField(max_length=100, verbose_name=' 内容')),
                ('title', models.CharField(default=' test', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('userFromID', models.IntegerField(default=0)),
                ('userToID', models.IntegerField(default=0)),
                ('content', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('url_height', models.PositiveIntegerField(null=True)),
                ('url_width', models.PositiveIntegerField(null=True)),
                ('photo', models.ImageField(null=True, height_field='url_height', upload_to='studentforum/portraits', width_field='url_width')),
                ('title', models.CharField(default=' test', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('topicType', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('pstNum', models.IntegerField(default=0)),
                ('heat', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='replytoreply',
            name='PID',
        ),
        migrations.RemoveField(
            model_name='replytoreply',
            name='author',
        ),
        migrations.AddField(
            model_name='myuser',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='collectClsNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='collectPst',
            field=models.ManyToManyField(to='studentforum.Post'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='collectPstNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='fansNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='follow',
            field=models.ManyToManyField(to='studentforum.MyUser'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='followNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='manageType',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='portrait',
            field=models.ImageField(null=True, height_field='url_height', upload_to='studentforum/portraits', width_field='url_width'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='pstNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='myuser',
            name='url_height',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='url_width',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='collectNum',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ReplyToReply',
        ),
        migrations.AddField(
            model_name='column',
            name='manager',
            field=models.ManyToManyField(to='studentforum.MyUser'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='collectCls',
            field=models.ManyToManyField(to='studentforum.Column'),
        ),
        migrations.AddField(
            model_name='post',
            name='ofColumn',
            field=models.ForeignKey(null=True, to='studentforum.Column'),
        ),
        migrations.AddField(
            model_name='post',
            name='ofTopic',
            field=models.ForeignKey(null=True, to='studentforum.Topic'),
        ),
    ]
