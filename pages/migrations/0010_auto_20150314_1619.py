# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0004_auto_20150228_2347'),
        ('pages', '0009_auto_20150313_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='sort_under_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='plots.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='sort_under_larp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='plots.Larp', null=True),
            preserve_default=True,
        ),
    ]
