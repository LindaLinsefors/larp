# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0007_auto_20141120_1241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupplotpice',
            old_name='plot_pice_name',
            new_name='plot_pice',
        ),
        migrations.RenameField(
            model_name='personalplotpice',
            old_name='plot_pice_name',
            new_name='plot_pice',
        ),
        migrations.RenameField(
            model_name='plotpart',
            old_name='plot_pice_name',
            new_name='plot_pice',
        ),
        migrations.AlterUniqueTogether(
            name='groupplotpice',
            unique_together=set([('group', 'plot_pice')]),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('group', 'character')]),
        ),
        migrations.AlterUniqueTogether(
            name='personalplotpice',
            unique_together=set([('character', 'plot_pice')]),
        ),
        migrations.AlterUniqueTogether(
            name='plotpart',
            unique_together=set([('plot_thread', 'plot_pice')]),
        ),
    ]
