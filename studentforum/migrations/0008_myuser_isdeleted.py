# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0007_replytoreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='isdeleted',
            field=models.BooleanField(default=False),
        ),
    ]
