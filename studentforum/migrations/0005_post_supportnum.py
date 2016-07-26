# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0004_auto_20160726_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='supportNum',
            field=models.IntegerField(default=0),
        ),
    ]
