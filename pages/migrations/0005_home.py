# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20150313_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html', models.TextField(default='<p>\nFist paragraph... \n</p>\n\n<p>\nSecond paragraph...\n</p>\n\n<h2> Sub-title </h2>\n<p>\nEvem more text...\n</p>', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
