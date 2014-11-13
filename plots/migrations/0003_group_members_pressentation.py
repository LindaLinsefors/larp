# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0002_auto_20141113_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members_pressentation',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
