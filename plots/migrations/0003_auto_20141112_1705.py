# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0002_auto_20141112_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='groop_plot_is_finished',
            new_name='plot_is_finished',
        ),
        migrations.RenameField(
            model_name='plot_line',
            old_name='plot_line_is_finished',
            new_name='plot_is_finished',
        ),
    ]
