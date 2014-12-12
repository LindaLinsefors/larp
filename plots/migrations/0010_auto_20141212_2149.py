# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0009_auto_20141212_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='comments_to_player',
        ),
        migrations.AddField(
            model_name='character',
            name='other_info',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
