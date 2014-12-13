# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0010_auto_20141212_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plotpice',
            name='name',
        ),
    ]
