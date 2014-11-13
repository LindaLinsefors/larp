# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('character_concept', models.CharField(max_length=50)),
                ('plot_is_finished', models.BooleanField(default=False)),
                ('character_description', models.TextField(default=b'', blank=True)),
                ('comments_from_God', models.TextField(default=b'', help_text=b'Comments on the character from GM to the player.', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('group_description', models.TextField(default=b'', blank=True)),
                ('plot_is_finished', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plot_is_finished', models.BooleanField(default=False)),
                ('plot', models.TextField(default=b'', blank=True)),
                ('characters', models.ManyToManyField(to='plots.Character', null=True, blank=True)),
                ('groups', models.ManyToManyField(to='plots.Group', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plot_line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plot_is_finished', models.BooleanField(default=False)),
                ('summery', models.TextField(default=b'', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='plot',
            name='plot_lines',
            field=models.ManyToManyField(to='plots.Plot_line', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='groups',
            field=models.ManyToManyField(to='plots.Group', null=True, blank=True),
            preserve_default=True,
        ),
    ]
