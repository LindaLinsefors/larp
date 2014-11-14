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
                ('plot_is_finished', models.BooleanField(default=False)),
                ('character_concept', models.CharField(max_length=50, blank=True)),
                ('presentation', models.TextField(default=b'', max_length=500, blank=True)),
                ('character_description', models.TextField(default=b'', max_length=5000, blank=True)),
                ('comments_to_player', models.TextField(default=b'', blank=True)),
                ('seceret_comments', models.TextField(default=b'', blank=True)),
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
                ('plot_is_finished', models.BooleanField(default=False)),
                ('is_open', models.BooleanField(default=False, help_text=b'Group is open for self registration by users', verbose_name=b'open')),
                ('group_description', models.TextField(default=b'', blank=True)),
                ('seceret_comments', models.TextField(default=b'', blank=True)),
                ('members_presentations', models.TextField(default=b'', blank=True)),
                ('shows_members', models.BooleanField(default=False, help_text=b'Members presentation is made public')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupPlotPice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.FloatField(default=0)),
                ('group', models.ForeignKey(to='plots.Group')),
            ],
            options={
                'ordering': ['rank'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.FloatField(default=0)),
                ('Group', models.ForeignKey(to='plots.Group')),
                ('character', models.ForeignKey(to='plots.Character')),
            ],
            options={
                'ordering': ['rank'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalPlotPice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.FloatField(default=0)),
                ('character', models.ForeignKey(to='plots.Character')),
            ],
            options={
                'ordering': ['rank'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlotConection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['rank'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlotPice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plot_is_finished', models.BooleanField(default=False)),
                ('plot_pice', models.TextField(default=b'', blank=True)),
                ('characters', models.ManyToManyField(to='plots.Character', null=True, through='plots.PersonalPlotPice', blank=True)),
                ('groups', models.ManyToManyField(to='plots.Group', null=True, through='plots.GroupPlotPice', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlotThread',
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
            model_name='plotpice',
            name='plot_threads',
            field=models.ManyToManyField(to='plots.PlotThread', null=True, through='plots.PlotConection', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plotconection',
            name='plot_pice',
            field=models.ForeignKey(to='plots.PlotPice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plotconection',
            name='plot_thread',
            field=models.ForeignKey(to='plots.PlotThread'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personalplotpice',
            name='plot_pice',
            field=models.ForeignKey(to='plots.PlotPice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupplotpice',
            name='plot_pice',
            field=models.ForeignKey(to='plots.PlotPice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='groups',
            field=models.ManyToManyField(to='plots.Group', null=True, through='plots.Membership', blank=True),
            preserve_default=True,
        ),
    ]
