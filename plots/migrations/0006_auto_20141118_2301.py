# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0005_character_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='Group',
            new_name='group',
        ),
        migrations.AlterField(
            model_name='character',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
