# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_home'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopLogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='home',
            name='title',
            field=models.CharField(default=b'WebSiteName', max_length=50),
            preserve_default=True,
        ),
    ]
