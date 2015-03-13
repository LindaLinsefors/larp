# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20150313_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='sort_under',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='pages.Page', null=True),
            preserve_default=True,
        ),
    ]
