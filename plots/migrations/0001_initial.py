# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='plots.BasicModel')),
                ('character_description', models.TextField(default=b'', blank=True)),
                ('comments_from_God', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=('plots.basicmodel',),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='plots.BasicModel')),
                ('group_description', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=('plots.basicmodel',),
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='plots.BasicModel')),
                ('plot', models.TextField(default=b'', blank=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='plots.Character', null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='plots.Group', null=True)),
            ],
            options={
            },
            bases=('plots.basicmodel',),
        ),
        migrations.CreateModel(
            name='Plot_line',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='plots.BasicModel')),
                ('summery', models.TextField()),
            ],
            options={
            },
            bases=('plots.basicmodel',),
        ),
        migrations.AddField(
            model_name='plot',
            name='plot_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='plots.Plot_line', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='group',
            field=models.ManyToManyField(to='plots.Group'),
            preserve_default=True,
        ),
    ]
