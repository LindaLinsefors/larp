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






class Plot(BasicModel):
    characters = models.ManyToManyField( 'Character', null=True, blank=True)
    groups = models.ManyToManyField( 'Group', null=True, blank=True)
    plot_lines = models.ManyToManyField( 'Plot_line', null=True, blank=True)
    plot_is_finished = models.BooleanField(default=False)

    plot = models.TextField(blank=True, default='')

    def groupsString(self):
        return ', '.join([group.name for group in self.groups.all()])
    groupsString.string = True
    groupsString.short_description = 'Groups'

    def charactersString(self):
        return ', '.join([character.name for character in self.characters.all()])
    charactersString.string = True
    charactersString.short_description = 'Characters'

    def plot_linesString(self):
        return ', '.join([plot_line.name for plot_line in self.plot_lines.all()])
    plot_linesString.string = True
    plot_linesString.short_description = 'Plot lines'



class Character(BasicModel):
    groups = models.ManyToManyField( 'Group', null=True, blank=True)
    character_concept = models.CharField(max_length=50)
    plot_is_finished = models.BooleanField(default=False)

    character_description = models.TextField(blank=True, default='')
    comments_from_God = models.TextField(blank=True, default='')
    comments_from_God.help_text='Comments on the character from GM to the player.'

    def groupsString(self):
        return ', '.join([group.name for group in self.groups.all()])
    groupsString.string = True
    groupsString.short_description = 'Groups'

    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including group plots'

    # def plot_line_by_groups(self):
    # plot_line_by_groups.short_description = 'Part of plot line, including group plots'
        

    
class Group(BasicModel):
    group_description = models.TextField(blank=True, default='')
    plot_is_finished = models.BooleanField(default=False)

    def members(self):
        return Character.objects.filter(groups=self)
    
    def no_of_members(self):
        return self.members().count()

    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including individual character plots'

    # def plot_line_by_characters(self):
    # plot_line_by_characters.short_description = 'Part of plot line, including individual character plots'




class Plot_line(BasicModel):
    plot_is_finished = models.BooleanField(default=False)
    summery = models.TextField(blank=True, default='')

    def plot_parts(self):
        return Plot.objects.filter(plot_lines=self)
    
    def no_of_plot_parts(self):
        return self.plot_parts().count()


    def characters(self):
        return Character.objects.filter(plot__in=self.plot_parts() )
    characters.short_description = (
         'Characters that have part in the plot line, not including individual group plots')
    def charactersString(self):
        return ', '.join([character.name for character in self.character.all()])
    charactersString.string = True
    charactersString.short_description = characters.short_description


    def groups(self):
        return Group.objects.filter(plot__in=self.plot_parts() )
    groups.short_description = (
        'Groupes that have part in the plot line, not including individual character plots')
    def groupsString(self):
        return ', '.join([group.name for group in self.groups.all()])
    groupsString.string = True
    groupsString.short_description = groups.short_description


    def groups_incl_char(self):
        return Group.objects.filter(
                    models.Q( plot__in=self.plot_parts() ) | 
                    models.Q( character__in=self.characters() )
               ).distinct()        
    groups_incl_char.short_description = (
        'Groupes that have part in the plot line, including individual character plots')
    groups_incl_char.query=True
    def groups_incl_charString(self):
        return ', '.join([group.name for group in self.groups_incl_char.all()])
    groups_incl_charString.string = True
    groups_incl_charString.short_description = groups.short_description



