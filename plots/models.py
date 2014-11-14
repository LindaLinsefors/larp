from django.db import models



# Create your models here.

class BasicModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def __unicode__(self):          # for Python 2 
        return unicode(self.name)

    plot_is_finished = models.BooleanField(default=False)


class RelationMeta(models.Model):
    rank = FloatField( default=0 )
    class Meta:
        abstract = True
        ordering = ['rank']

class Membership(RelationMeta)
    character = models.ForeginKey('Character')
    Group = models.ForeginKey('Group')

class PlotConection(RelationMeta):
    plot_pice = models.ForeginKey('PlotPice')
    plot_thread = models.ForeginKey('PlotThread')

class GroupPlotPice(RelationMeta):
    plot_pice = models.ForeginKey('PlotPice')
    group = models.ForeginKey('Group')

class PersonalPloPice(RelationMeta):
    plot_pice = models.ForeginKey('PlotPice')
    character = models.ForeginKey('Character')


class PlotPice(BasicModel):
    characters = models.ManyToManyField(
                'Character', null=True, blank=True, through='PersonalPloPice')
    groups = models.ManyToManyField(
                'Group', null=True, blank=True through='GroupPlotPice')
    plot_thread = models.ManyToManyField( 
                'PlotThred', null=True, blank=True, through='PlotConection')

    plot_pice = models.TextField(blank=True, default='')

    def grous_string(self):
        return ', '.join([group.name for group in self.groups.all()])
    grous_string.string = True
    grous_string.verbose_name = 'Groups'

    def characters_string(self):
        return ', '.join([character.name for character in self.characters.all()])
    characters_string.string = True
    characters_string.verbose_name = 'Characters'

    def plot_lines_string(self):
        return ', '.join([plot_line.name for plot_line in self.plot_lines.all()])
    plot_lines_string.string = True
    plot_lines_string.verbose_name = 'Plot threds'



class Character(BasicModel):
    groups = models.ManyToManyField( 
                'Group', null=True, blank=True, through='Membership')

    character_concept = models.CharField(max_length=50, blank=True)

    presentation = models.TextField(blank=True, default='', max_length=500)
    character_description = models.TextField(blank=True, default='', max_length=5000)
    comments_to_player = models.TextField(blank=True, default='')
    seceret_comments = models.TextField(blank=True, default='')


    def groups_string(self):
        return ', '.join([group.name for group in self.groups.all()])
    groups_string.string = True
    groups_string.verbose_name = 'Groups'

    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including group plots'

    # def plot_line_by_groups(self):
    # plot_line_by_groups.short_description = 'Part of plot line, including group plots'
        

    
class Group(BasicModel):
    is_open = models.BooleanField('open', default=False)
    is_open.help_text = 'Group is open for self registration by users'

    group_description = models.TextField(blank=True, default='')

    seceret_comments = models.TextField(blank=True, default='')
    
    members_presentations = models.TextField(blank=True, default='')    
    shows_members = models.BooleanField(default=False) 
    shows_members.help_text = 'Members presentation is made public'
    
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
        return self.plot_set.all()
    
    def no_of_plot_parts(self):
        return self.plot_parts().count()
    no_of_plot_parts.verbose_name = 'number of plot parts'


    def characters(self):
        return Character.objects.filter(plot__in=self.plot_parts() )
    characters.help_text = (
         'Characters that have part in the plot line, not including group plots')
    characters.short_description = 'Characters involved'
    def characters_string(self):
        return ', '.join([character.name for character in self.characters().all()])
    characters_string.string = True
    characters_string.help_text = characters.help_text
    characters_string.short_description = characters.short_description
    characters_string.verbose_name = 'characters'


    def groups(self):
        return Group.objects.filter(plot__in=self.plot_parts() )
    groups.help_text = (
        'Groupes that have part in the plot line, not including individual character plots')
    groups.short_description = 'Groupes involved'
    def groups_string(self):
        return ', '.join([group.name for group in self.groups().all()])
    groups_string.string = True
    groups_string.help_text = groups.help_text
    groups_string.short_description = groups.short_description
    groups_string.verbose_name = 'groups'


    def groups_incl_char(self):
        return Group.objects.filter(
                    models.Q( plot__in=self.plot_parts() ) | 
                    models.Q( character__in=self.characters() )
               ).distinct()        
    groups_incl_char.help_text = (
        'Groupes that have part in the plot line, including individual character plots')
    groups_incl_char.short_description = 'Someone in gruop is involved'
    groups_incl_char.verbose_name = 'groups incl. personal plots'
    def groups_incl_char_string(self):
        return ', '.join([group.name for group in self.groups_incl_char().all()])
    groups_incl_char_string.string = True
    groups_incl_char_string.short_description = groups_incl_char.short_description
    groups_incl_char_string.help_text = groups_incl_char.help_text
    groups_incl_char_string.verbose_name = groups_incl_char.verbose_name



