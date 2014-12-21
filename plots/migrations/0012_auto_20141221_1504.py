# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0011_remove_plotpice_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='plotthread',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='group',
            name='secret',
        ),
        migrations.AddField(
            model_name='group',
            name='show_group',
            field=models.BooleanField(default=False, help_text=b'Group description is made public.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='is_open',
            field=models.BooleanField(default=False, help_text=b'Group is open for self registration by users.', verbose_name=b'open'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='show_members',
            field=models.BooleanField(default=False, help_text=b'Members presentation is made public.'),
            preserve_default=True,
        ),
    ]
