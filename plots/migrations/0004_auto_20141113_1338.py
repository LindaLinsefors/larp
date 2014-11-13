# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0003_group_members_pressentation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='members_pressentation',
            new_name='members_presentation',
        ),
    ]
