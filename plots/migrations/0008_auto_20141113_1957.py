# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0007_auto_20141113_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='show_members',
            new_name='shows_members',
        ),
    ]
