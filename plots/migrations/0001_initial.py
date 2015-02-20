# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('other_info', models.TextField(default=b'', blank=True)),
                ('secret_comments', models.TextField(default=b'', help_text=b'<i>Player can nether read nor write.</i>', blank=True)),
                ('plot_is_finished', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('is_open', models.BooleanField(default=False, help_text=b'Group is open for self registration by users.', verbose_name=b'open')),
                ('show_members', models.BooleanField(default=False, help_text=b'Members presentation is made public.')),
                ('plot_is_finished', models.BooleanField(default=False)),
                ('show_group', models.BooleanField(default=False, help_text=b'Group description is made public.')),
                ('group_description', models.TextField(default=b'', blank=True)),
                ('members_presentations', models.TextField(default=b'', blank=True)),
                ('secret_comments', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ['name'],
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
            name='Larp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('characters', models.ManyToManyField(to='plots.Character', null=True, blank=True)),
                ('groups', models.ManyToManyField(to='plots.Group', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.FloatField(default=0, help_text=b'Arrange in which order objects appear. Lowest to highest')),
                ('character', models.ForeignKey(to='plots.Character')),
                ('group', models.ForeignKey(to='plots.Group')),
                ('larp', models.ForeignKey(to='plots.Larp')),
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
                ('larp', models.ForeignKey(to='plots.Larp')),
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
                ('larp', models.ForeignKey(to='plots.Larp')),
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
                ('plot_pice', models.TextField(default=b'', blank=True)),
                ('plot_is_finished', models.BooleanField(default=False)),
                ('characters', models.ManyToManyField(to='plots.Character', null=True, through='plots.PersonalPlotPice', blank=True)),
                ('groups', models.ManyToManyField(to='plots.Group', null=True, through='plots.GroupPlotPice', blank=True)),
                ('larp', models.ForeignKey(to='plots.Larp')),
            ],
            options={
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
                'ordering': ['name'],
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
        migrations.AlterUniqueTogether(
            name='plotpart',
            unique_together=set([('plot_thread', 'plot_pice')]),
        ),
        migrations.AddField(
            model_name='personalplotpice',
            name='plot_pice',
            field=models.ForeignKey(to='plots.PlotPice'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='personalplotpice',
            unique_together=set([('character', 'plot_pice')]),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('group', 'character')]),
        ),
        migrations.AddField(
            model_name='larp',
            name='plot_threads',
            field=models.ManyToManyField(to='plots.PlotThread', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupplotpice',
            name='larp',
            field=models.ForeignKey(to='plots.Larp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupplotpice',
            name='plot_pice',
            field=models.ForeignKey(to='plots.PlotPice'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='groupplotpice',
            unique_together=set([('group', 'plot_pice')]),
        ),
        migrations.AddField(
            model_name='character',
            name='groups',
            field=models.ManyToManyField(to='plots.Group', null=True, through='plots.Membership', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='user',
            field=models.ForeignKey(default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
