# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0006_auto_20141113_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='members_presentation',
            new_name='members_presentations',
        ),
        migrations.RemoveField(
            model_name='group',
            name='public',
        ),
    ]
