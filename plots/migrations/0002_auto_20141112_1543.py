# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='character_concept',
            field=models.CharField(default='gos', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='character',
            name='plot_is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='groop_plot_is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plot_line',
            name='plot_line_is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
