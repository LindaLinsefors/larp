# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='comments_from_God',
        ),
        migrations.AddField(
            model_name='character',
            name='comments_to_player',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='presentation',
            field=models.TextField(default=b'', max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='seceret_comments',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='seceret_comments',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='character',
            name='character_description',
            field=models.TextField(default=b'', max_length=5000, blank=True),
            preserve_default=True,
        ),
    ]
