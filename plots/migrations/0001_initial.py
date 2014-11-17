# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('character_concept', models.CharField(max_length=50, blank=True)),
                ('presentation', models.TextField(default=b'', help_text=b'A short pressentation of the character to be read by all players. Can be written by player or Game Master <br><i>Player can read and write.</i>', max_length=500, blank=True)),
                ('character_description', models.TextField(default=b'', help_text=b'Character description is usually provided by the player but can also be written by Game Master. Do not change a character description written by a player. <br><i>Player can read and write.</i>', max_length=5000, blank=True)),
                ('comments_to_player', models.TextField(default=b'', help_text=b'<i>Player can read but not write.</i>', blank=True)),
                ('seceret_comments', models.TextField(default=b'', help_text=b'<i>Player can nether read nor write.</i>', blank=True)),
                ('plot_is_finished', models.BooleanField(default=False)),
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
                ('url', models.CharField(default=b'', help_text=b'The end bit of the webadress for the group page. If left blank no page for this group will be produced. The group will then be seceret.', max_length=50, blank=True, validators=[django.core.validators.RegexValidator(b'^\\w*$', b'Only alphanumeric characters and underscores are allowed.')])),
                ('is_open', models.BooleanField(default=False, help_text=b'Group is open for self registration by users', verbose_name=b'open')),
                ('group_description', models.TextField(default=b'', blank=True)),
                ('seceret_comments', models.TextField(default=b'', blank=True)),
                ('members_presentations', models.TextField(default=b'', blank=True)),
                ('shows_members', models.BooleanField(default=False, help_text=b'Members presentation is made public')),
                ('plot_is_finished', models.BooleanField(default=False)),
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
                ('rank', models.FloatField(default=0, help_text=b'Arrange in which order objects appear. Lowest to highest')),
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
                ('rank', models.FloatField(default=0, help_text=b'Arrange in which order objects appear. Lowest to highest')),
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
                ('rank', models.FloatField(default=0, help_text=b'Arrange in which order objects appear. Lowest to highest')),
                ('character', models.ForeignKey(to='plots.Character')),
            ],
            options={
                'ordering': ['rank'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlotPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.FloatField(default=0, help_text=b'Arrange in which order objects appear. Lowest to highest')),
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
                ('plot_pice', models.TextField(default=b'', blank=True)),
                ('plot_is_finished', models.BooleanField(default=False)),
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
                ('summery', models.TextField(default=b'', blank=True)),
                ('plot_is_finished', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='plotpice',
            name='plot_threads',
            field=models.ManyToManyField(to='plots.PlotThread', null=True, through='plots.PlotPart', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plotpart',
            name='plot_pice',
            field=models.ForeignKey(to='plots.PlotPice'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plotpart',
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
