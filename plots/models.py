from django.db import models

from django.core import urlresolvers, validators



# Create your models here.

class BasicModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def __unicode__(self):          # for Python 2 
        return unicode(self.name)

    def get_admin_url(self):
        return urlresolvers.reverse("admin:%s_%s_change" %
            (self._meta.app_label, self._meta.module_name), args=(self.id,))

    


class RelationMeta(models.Model):
    rank = models.FloatField( default=0 )
    rank.help_text = 'Arrange in which order objects appear. Lowest to highest'
    class Meta:
        abstract = True
        ordering = ['rank']

class Membership(RelationMeta):
    character = models.ForeignKey('Character')
    Group = models.ForeignKey('Group')

class PlotPart(RelationMeta):
    plot_pice = models.ForeignKey('PlotPice')
    plot_thread = models.ForeignKey('PlotThread')

class GroupPlotPice(RelationMeta):
    plot_pice = models.ForeignKey('PlotPice')
    group = models.ForeignKey('Group')

class PersonalPlotPice(RelationMeta):
    plot_pice = models.ForeignKey('PlotPice')
    character = models.ForeignKey('Character')


class PlotPice(BasicModel):
    characters = models.ManyToManyField(
                'Character', null=True, blank=True, through='PersonalPlotPice')
    groups = models.ManyToManyField(
                'Group', null=True, blank=True, through='GroupPlotPice')
    plot_threads = models.ManyToManyField( 
                'PlotThread', null=True, blank=True, through='PlotPart')

    plot_pice = models.TextField(blank=True, default='')
    
    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = 'plot pice is finiched'
    plot_is_finished.short_description = 'plot is finiched'

    def groups_string(self):
        return ',\n '.join([group.name for group in self.groups.all()])
    groups_string.string = True
    groups_string.verbose_name = 'Groups'
    groups_string.short_description = 'Groups'

    def characters_string(self):
        return ',\n '.join([character.name for character in self.characters.all()])
    characters_string.string = True
    characters_string.verbose_name = 'Characters'
    characters_string.short_description = 'Characters'

    def plot_threads_string(self):
        return ',\n '.join([plot_thread.name for plot_thread in self.plot_threads.all()])
    plot_threads_string.string = True
    plot_threads_string.verbose_name = 'Plot threds'
    plot_threads_string.short_description = 'Plot threds'



class Character(BasicModel):
    groups = models.ManyToManyField( 
                'Group', null=True, blank=True, through='Membership')

    character_concept = models.CharField(max_length=50, blank=True)

    presentation = models.TextField(blank=True, default='', max_length=500)
    presentation.help_text = (
        'A short pressentation of the character to be read by all players. Can be written by player or Game Master <br><i>Player can read and write.</i>')

    character_description = models.TextField(blank=True, default='', max_length=5000)
    character_description.help_text = (
        'Character description is usually provided by the player but can also be written by Game Master. Do not change a character description written by a player. <br><i>Player can read and write.</i>')

    comments_to_player = models.TextField(blank=True, default='')
    comments_to_player.help_text = '<i>Player can read but not write.</i>'
    
    seceret_comments = models.TextField(blank=True, default='')
    seceret_comments.help_text = '<i>Player can nether read nor write.</i>'

    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = "character's plot is finiched"
    plot_is_finished.short_description = "plot is finiched"

    def groups_string(self):
        return ', '.join([group.name for group in self.groups.all()])
    groups_string.string = True
    groups_string.verbose_name = 'Groups'
    groups_string.short_description = 'Groups'

    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including group plots'

    # def plot_line_by_groups(self):
    # plot_line_by_groups.short_description = 'Part of plot line, including group plots'
      
  
    
class Group(BasicModel):

    def url(self):
        ret = ''
        for char in self.name:
            if char == ' ':  ret += '_'
            else:           ret += char
        return ret

    is_open = models.BooleanField('open', default=False)
    is_open.help_text = 'Group is open for self registration by users'
       
    show_members = models.BooleanField(default=False) 
    show_members.help_text = 'Members presentation is made public'

    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = "group's plot is finiched"

    secret = models.BooleanField(default=True)
    secret.help_text = 'Group is not visible on the web page'

    group_description = models.TextField(blank=True, default='')
    members_presentations = models.TextField(blank=True, default='')
    secret_comments = models.TextField(blank=True, default='')

    
    def members(self):
        return self.character_set.all()
    
    def no_of_members(self):
        return self.members().count()
    no_of_members.verbose_name = 'number of members'

    def make_members_presentations(self):
        characters = []
        for member in self.members():
            if member.character_concept == '':
                characters.append( 
                        '<h2>' + member.name + '</h2>' +
                        '\n<p>\n' + member.presentation + '\n</p>')
            else: 
                characters.append(  
                        '<h2>' + member.name + 
                        ', <small> ' +  member.character_concept + ' </small>'
                        + '</h2>' +
                        '\n<p>\n' + member.presentation + '\n</p>')
     
        self.members_presentations = '\n\n'.join( characters )



    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including individual character plots'

    # def plot_line_by_characters(self):
    # plot_line_by_characters.short_description = 'Part of plot line, including individual character plots'




class PlotThread(BasicModel):
    summery = models.TextField(blank=True, default='')

    def plot_parts(self):
        return self.plotpice_set.all()
    
    def no_of_plot_parts(self):
        return self.plot_parts().count()
    no_of_plot_parts.verbose_name = 'number of plot parts'

    plot_is_finished = models.BooleanField(default=False)
    plot_is_finished.verbose_name = "plot thread plot is finiched"


    def characters(self):
        return Character.objects.filter(plotpice__in=self.plot_parts() )
    characters.help_text = (
         'Characters that have part in the plot line, not including group plots')
    characters.short_description = 'Characters involved'
    def characters_string(self):
        return ',\n '.join([character.name for character in self.characters().all()])
    characters_string.string = True
    characters_string.help_text = characters.help_text
    characters_string.short_description = characters.short_description
    characters_string.verbose_name = 'characters'


    def groups(self):
        return Group.objects.filter(plotpice__in=self.plot_parts() )
    groups.help_text = (
        'Groupes that have part in the plot line, not including individual character plots')
    groups.short_description = 'Groupes involved'
    def groups_string(self):
        return ',\n '.join([group.name for group in self.groups().all()])
    groups_string.string = True
    groups_string.help_text = groups.help_text
    groups_string.short_description = groups.short_description
    groups_string.verbose_name = 'groups'


    def groups_incl_char(self):
        return Group.objects.filter(
                    models.Q( plotpice__in=self.plot_parts() ) | 
                    models.Q( character__in=self.characters() )
               ).distinct()        
    groups_incl_char.help_text = (
        'Groupes that have part in the plot line, including individual character plots')
    groups_incl_char.short_description = 'Someone in group is involved'
    groups_incl_char.verbose_name = 'groups incl. personal plots'
    def groups_incl_char_string(self):
        return ',\n '.join([group.name for group in self.groups_incl_char().all()])
    groups_incl_char_string.string = True
    groups_incl_char_string.short_description = groups_incl_char.short_description
    groups_incl_char_string.help_text = groups_incl_char.help_text
    groups_incl_char_string.verbose_name = groups_incl_char.verbose_name



