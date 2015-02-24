# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_open',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
