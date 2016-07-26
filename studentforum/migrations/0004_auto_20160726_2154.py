# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentforum', '0003_reply_numgood'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='numgood',
            new_name='supportNum',
        ),
    ]
