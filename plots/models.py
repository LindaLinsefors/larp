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






class Plot(BasicModel):
    characters = models.ManyToManyField( 'Character', null=True, blank=True)
    groups = models.ManyToManyField( 'Group', null=True, blank=True)
    plot_lines = models.ManyToManyField( 'Plot_line', null=True, blank=True)

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
    character_concept = models.CharField(max_length=50, blank=True)

    presentation = models.TextField(blank=True, default='', max_length=500)
    character_description = models.TextField(blank=True, default='', max_length=5000)
    comments_to_player = models.TextField(blank=True, default='')
    seceret_comments = models.TextField(blank=True, default='')


    def groupsString(self):
        return ', '.join([group.name for group in self.groups.all()])
    groupsString.string = True
    groupsString.short_description = 'Groups'

    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including group plots'

    # def plot_line_by_groups(self):
    # plot_line_by_groups.short_description = 'Part of plot line, including group plots'
        

    
class Group(BasicModel):
    is_open = models.BooleanField(default=False)
    is_open.short_descripion = 'Open'
    is_open.help_text = 'Group is open for self registration by users'

    group_description = models.TextField(blank=True, default='')
    public = models.BooleanField(default=False) 
    public.help_text = 'Group decription is made public'

    seceret_comments = models.TextField(blank=True, default='')
    
    members_presentation = models.TextField(blank=True, default='')    
    show_members = models.BooleanField(default=False) 
    show_members.help_text = 'Members presentation is made public'
    
    def members(self):
        return self.character_set.all()
    
    def no_of_members(self):
        return self.members().count()

    def make_members_presentation(self):
        characters = []
        for member in self.members():
            if member.character_concept == '':
                characters.append(member.name + '\n' + member.presentation)
            else: 
                characters.append(  member.name + ', ' +
                                    member.character_concept +
                                   '\n' + member.presentation)
     
        self.members_presentation = '\n\n'.join( characters )



    # def plot_line(self):
    # plot_line.short_description = 'Part of plot line, not including individual character plots'

    # def plot_line_by_characters(self):
    # plot_line_by_characters.short_description = 'Part of plot line, including individual character plots'




class Plot_line(BasicModel):
    summery = models.TextField(blank=True, default='')

    def plot_parts(self):
        return self.plot_set.all()
    
    def no_of_plot_parts(self):
        return self.plot_parts().count()


    def characters(self):
        return Character.objects.filter(plot__in=self.plot_parts() )
    characters.help_text = (
         'Characters that have part in the plot line, not including individual group plots')
    characters.short_description = 'Characters involved'
    def charactersString(self):
        return ', '.join([character.name for character in self.characters().all()])
    charactersString.string = True
    charactersString.help_text = characters.help_text
    charactersString.short_description = characters.short_description


    def groups(self):
        return Group.objects.filter(plot__in=self.plot_parts() )
    groups.help_text = (
        'Groupes that have part in the plot line, not including individual character plots')
    groups.short_description = 'Groupes involved'
    def groupsString(self):
        return ', '.join([group.name for group in self.groups().all()])
    groupsString.string = True
    groupsString.help_text = groups.help_text
    groupsString.short_description = groups.short_description


    def groups_incl_char(self):
        return Group.objects.filter(
                    models.Q( plot__in=self.plot_parts() ) | 
                    models.Q( character__in=self.characters() )
               ).distinct()        
    groups_incl_char.help_text = (
        'Groupes that have part in the plot line, including individual character plots')
    groups_incl_char.short_description = 'Someone in gruop is involved'
    def groups_incl_charString(self):
        return ', '.join([group.name for group in self.groups_incl_char().all()])
    groups_incl_charString.string = True
    groups_incl_charString.short_description = groups_incl_char.short_description
    groups_incl_charString.help_text = groups_incl_char.help_text



