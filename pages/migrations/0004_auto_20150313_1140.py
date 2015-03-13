# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_page_in_nav'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='page',
            old_name='text',
            new_name='html',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='up',
            new_name='sort_under',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='in_nav',
            new_name='top_page',
        ),
    ]
