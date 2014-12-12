# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0008_auto_20141210_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='seceret_comments',
            new_name='secret_comments',
        ),
    ]
