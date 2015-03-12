# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20150312_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='in_nav',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
