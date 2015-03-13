# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_delete_toplogo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='sort_under',
            field=models.ForeignKey(blank=True, to='pages.Page', null=True),
            preserve_default=True,
        ),
    ]
