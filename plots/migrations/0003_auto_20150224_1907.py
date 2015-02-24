# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0002_group_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='larps',
            field=models.ManyToManyField(to='plots.Larp', null=True, through='plots.PersonalPlot', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='characters',
            field=models.ManyToManyField(to='plots.Character', null=True, through='plots.Membership', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='larps',
            field=models.ManyToManyField(to='plots.Larp', null=True, through='plots.GroupPlot', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plotthread',
            name='larps',
            field=models.ManyToManyField(to='plots.Larp', null=True, through='plots.LarpPlotThread', blank=True),
            preserve_default=True,
        ),
    ]
