# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0006_auto_20141118_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupplotpice',
            old_name='plot_pice',
            new_name='plot_pice_name',
        ),
        migrations.RenameField(
            model_name='personalplotpice',
            old_name='plot_pice',
            new_name='plot_pice_name',
        ),
        migrations.RenameField(
            model_name='plotpart',
            old_name='plot_pice',
            new_name='plot_pice_name',
        ),
    ]
