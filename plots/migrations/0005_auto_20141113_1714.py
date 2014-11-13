# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0004_auto_20141113_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_open',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='show_group_description',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='show_members_presentation',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='character',
            name='character_concept',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
