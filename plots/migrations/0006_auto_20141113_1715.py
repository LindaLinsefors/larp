# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0005_auto_20141113_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='show_group_description',
        ),
        migrations.RemoveField(
            model_name='group',
            name='show_members_presentation',
        ),
        migrations.AddField(
            model_name='group',
            name='public',
            field=models.BooleanField(default=False, help_text=b'Group decription is made public'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='show_members',
            field=models.BooleanField(default=False, help_text=b'Members presentation is made public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='is_open',
            field=models.BooleanField(default=False, help_text=b'Group is open for self registration by users'),
            preserve_default=True,
        ),
    ]
