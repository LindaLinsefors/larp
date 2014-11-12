# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0003_auto_20141112_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='plot',
            name='plot_is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='character',
            name='groups',
            field=models.ManyToManyField(to='plots.Group', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='characters',
            field=models.ManyToManyField(to='plots.Character', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='groups',
            field=models.ManyToManyField(to='plots.Group', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plot',
            name='plot_lines',
            field=models.ManyToManyField(to='plots.Plot_line', null=True, blank=True),
            preserve_default=True,
        ),
    ]
