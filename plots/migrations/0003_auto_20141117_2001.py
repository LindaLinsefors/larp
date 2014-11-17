# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0002_remove_group_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='seceret_comments',
        ),
        migrations.RemoveField(
            model_name='group',
            name='shows_members',
        ),
        migrations.AddField(
            model_name='group',
            name='comments',
            field=models.TextField(default=b'', help_text=b'These comments does not appear anywhere else.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='secret',
            field=models.BooleanField(default=True, help_text=b'Group is not visible on the web page'),
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
            name='group_description',
            field=models.TextField(default=b'', help_text=b'The group descripion will appear pyblicly on the web page if the group is not marked as secret.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='members_presentations',
            field=models.TextField(default=b'', help_text=b'Members presentations will appear pyblicly on the web page if "show members" is ticked.', blank=True),
            preserve_default=True,
        ),
    ]
