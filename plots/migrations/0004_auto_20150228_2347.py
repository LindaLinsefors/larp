# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0003_auto_20150224_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plotpice',
            old_name='group_plotss',
            new_name='group_plots',
        ),
        migrations.AlterUniqueTogether(
            name='groupplot',
            unique_together=set([('larp', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='larpplotthread',
            unique_together=set([('larp', 'plot_thread')]),
        ),
        migrations.AlterUniqueTogether(
            name='personalplot',
            unique_together=set([('larp', 'character')]),
        ),
    ]
