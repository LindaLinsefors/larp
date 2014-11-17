# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0003_auto_20141117_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='comments',
        ),
        migrations.AddField(
            model_name='group',
            name='secret_comments',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='group_description',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='members_presentations',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
