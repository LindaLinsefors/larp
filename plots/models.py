from django.db import models
from django.contrib import auth
from django.core import urlresolvers, validators



# Create your models here.

class BasicModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['name']
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def __unicode__(self):          # for Python 2 
        return unicode(self.name)
    


class BasicRelation(models.Model):
    rank = models.FloatField( default=0 )
    rank.help_text = 'Arrange in which order objects appear. Lowest to highest'

    class Meta:
        abstract = True
        ordering = ['rank']

class Membership(BasicRelation):
    character = models.ForeignKey('Character')
    group = models.ForeignKey('Group')
    class Meta(BasicPlotRelation.Meta):
        unique_together = (("group", "character"),)
    former_member = models.BooleanField(default=False)




class BasicPlotRelation(BasicRelation):
    plot_pice = models.ForeignKey('PlotPice')
    class Meta(BasicRelation.Meta):
        abstract = True

class PlotPart(BasicPlotRelation):
    larp_plot_thread = models.ForeignKey('LarpPlotThread')
    class Meta(BasicPlotRelation.Meta):
        unique_together = (("larp_plot_thread", "plot_pice"),)

class GroupPlotPice(BasicPlotRelation):
    group_plot = models.ForeignKey('GroupPlot')
    class Meta(BasicPlotRelation.Meta):
        unique_together = (("group_plot", "plot_pice"),)

class PersonalPlotPice(BasicPlotRelation):
    personal_plot = models.ForeignKey('PersonalPlot')
    class Meta(BasicPlotRelation.Meta):
        unique_together = (("personal_plot", "plot_pice"),)


class GroupPlot(modes.Model):
    larp = models.ForeignKey('Larp')
    group = models.ForeignKey('Group')

    secret_comments = models.TextField(blank=True, default='')

    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = "group's plot is finished"

    def name(self):
        return self.group.name

    def __str__(self):
        return self.group.name + ', ' + self.larp.name
    def __unicode__(self):          # for Python 2 
        return unicode( self.group.name + ', ' + self.larp.name )


class PersonalPlot(models.Model):
    larp = models.ForeignKey('Larp')
    character = models.ForeignKey('Character')

    secret_comments = models.TextField(blank=True, default='')

    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = "character's plot is finished"

    def name(self):
        return self.character.name

    def __str__(self):
        return self.character.name + ', ' + self.larp.name
    def __unicode__(self):          # for Python 2 
        return unicode( self.character.name + ', ' + self.larp.name )


class LarpPlotThread(models.Model):
    larp = models.ForeignKey('Larp')
    plot_thread = models.ForeignKey('PlotThread')

    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = "plot thread is finished"

    def name(self):
        return self.plot_thread.name

    def __str__(self):
        return self.plot_thread.name + ', ' + self.larp.name
    def __unicode__(self):          # for Python 2 
        return unicode( self.plot_thread.name + ', ' + self.larp.name )

    def characters(self):
        return [PersonalPlot.objects.filter(plotpice__in=self.plot_parts() )
    characters.help_text = (
         'Characters that have part in the plot line, not including group plots')
    characters.short_description = 'Characters involved'
    def characters_string(self):
        return ',\n '.join([character.name for character in self.characters().all()])
    characters_string.help_text = characters.help_text
    characters_string.short_description = characters.short_description
    characters_string.verbose_name = 'characters'

    def groups(self):
        return GroupPlot.objects.filter(plotpice__in=self.plot_parts() )
    groups.help_text = (
        'Groupes that have part in the plot line, not including individual character plots')
    groups.short_description = 'Groupes involved'
    def groups_string(self):
        return ',\n '.join([group.name for group in self.groups().all()])
    groups_string.help_text = groups.help_text
    groups_string.short_description = groups.short_description
    groups_string.verbose_name = 'groups'

    def groups_incl_char(self):
        return GroupPlot.objects.filter(
                    models.Q( plotpice__in=self.plot_parts() ) | 
                    models.Q( character__in=self.characters() )
               ).distinct()        
    groups_incl_char.help_text = (
        'Groupes that have part in the plot line, including individual character plots')
    groups_incl_char.short_description = 'Someone in group is involved'
    groups_incl_char.verbose_name = 'groups incl. personal plots'
    def groups_incl_char_string(self):
        return ',\n '.join([group.name for group in self.groups_incl_char().all()])
    groups_incl_char_string.short_description = groups_incl_char.short_description
    groups_incl_char_string.help_text = groups_incl_char.help_text
    groups_incl_char_string.verbose_name = groups_incl_char.verbose_name



class PlotPice(models.Model):

    def __str__(self):
        return self.plot_pice[0:50]+'...' 
    def __unicode__(self):          # for Python 2 
        return unicode(self.plot_pice[0:50])+'...' 
    __str__.short_description = 'str'

    characters = models.ManyToManyField(
                'Character', null=True, blank=True, through='PersonalPlotPice')
    groups = models.ManyToManyField(
                'Group', null=True, blank=True, through='GroupPlotPice')
    plot_threads = models.ManyToManyField( 
                'PlotThread', null=True, blank=True, through='PlotPart')

    plot_pice = models.TextField(blank=True, default='')
    
    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = 'plot pice is finished'
    plot_is_finished.short_description = 'plot is finished'

    def groups_string(self):
        return ',\n '.join([group.name for group in self.groups.all()])
    groups_string.verbose_name = 'Groups'
    groups_string.short_description = 'Groups'

    def characters_string(self):
        return ',\n '.join([character.name for character in self.characters.all()])
    characters_string.verbose_name = 'Characters'
    characters_string.short_description = 'Characters'

    def plot_threads_string(self):
        return ',\n '.join([plot_thread.name for plot_thread in self.plot_threads.all()])
    plot_threads_string.verbose_name = 'Plot threds'
    plot_threads_string.short_description = 'Plot threds'

    larp = models.ForeignKey('Larp')



class Character(BasicModel):
    
    user = models.ForeignKey(auth.models.User, null=True, blank=True, default=None )  
    
    def heading(self):
        if self.character_concept == '':
            return self.name
        else: 
            return self.name + ', <small> ' +  self.character_concept + ' </small>'

    
    groups = models.ManyToManyField( 
                'Group', null=True, blank=True, through='Membership')

    character_concept = models.CharField(max_length=50, blank=True)

    presentation = models.TextField(blank=True, default='', max_length=500)
    presentation.help_text = (
        'A short pressentation of the character to be read by all players. Can be written by player or Game Master <br><i>Player can read and write.</i>')

    character_description = models.TextField(blank=True, default='', max_length=5000)
    character_description.help_text = (
        'Character description is usually provided by the player but can also be written by Game Master. Do not change a character description written by a player. <br><i>Player can read and write.</i>')

    other_info = models.TextField(blank=True, default='')

    def groups_string(self):
        return ', '.join([group.name for group in self.groups.all()])
    groups_string.verbose_name = 'Groups'
    groups_string.short_description = 'Groups'
  
  
    
class Group(BasicModel):

    def url(self):
        ret = ''
        for char in self.name:
            if char == ' ':  ret += '_'
            else:           ret += char
        return ret

       
    show_members = models.BooleanField(default=False) 
    show_members.help_text = 'Members presentation is made public.'

    show_group = models.BooleanField(default=False)
    show_group.help_text = 'Group description is made public.'

    group_description = models.TextField(blank=True, default='')
    members_presentations = models.TextField(blank=True, default='')


    def make_members_presentations(self):
        characters = []
        for member in self.members():
            characters.append( 
                        '<h2>' + member.heading() + '</h2>' +
                        '\n<p>\n' + member.presentation + '\n</p>')

        self.members_presentations = '\n\n'.join( characters )



class PlotThread(BasicModel):
    summery = models.TextField(blank=True, default='')



class Larp(BasicModel):
    characters = models.ManyToManyField(
                'Character', null=True, blank=True, through='PersonalPlot')
    groups = models.ManyToManyField(
                'Group', null=True, blank=True, through='GroupPlot' )
    plot_threads = models.ManyToManyField( 
                'PlotThread', null=True, blank=True, through='LarpPlotThread')
