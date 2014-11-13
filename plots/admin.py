from django.contrib import admin
from plots.models import *
from django import forms



#Groups

class CharacterInlineGroupe(admin.TabularInline):
    model = Character.groups.through
    extra = 0
    #raw_id_fields = ("character",)


class PlotInlineGroupe(admin.TabularInline):
    model = Plot.groups.through
    extra = 0
    

class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['name',
                                            'plot_is_finished']}),
        ('Group description',   {'fields': ['group_description',
                                            'seceret_comments'], 
                                 'classes': ['collapse']})
    ]

    inlines = [CharacterInlineGroupe, PlotInlineGroupe]

    list_display = ('name', 'no_of_members', 'plot_is_finished')

    list_filter = ['plot_is_finished']

admin.site.register(Group, GroupAdmin)


#Characters

class PlotInlineCharacter(admin.TabularInline):
    model = Plot.characters.through
    extra = 0

class CharacterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                      {'fields': [('name',
                                                'character_concept'),
                                                'groups',
                                                'plot_is_finished']}),
        ('Character description',   {'fields': ['presentation',
                                                'character_description',
                                                'comments_to_player',
                                                'seceret_comments'], 
                                     'classes': ['collapse']})
    ]

    inlines = [PlotInlineCharacter]

    list_display = ('name', 'character_concept', 'groupsString', 'plot_is_finished')
    list_filter = ['groups','plot_is_finished']

admin.site.register(Character, CharacterAdmin)


#Plot_line

class PlotInlinePlot_line(admin.TabularInline):
    model = Plot.plot_lines.through
    extra = 0


class Plot_lineAdmin(admin.ModelAdmin):

    list_display = ('name', 
                    'no_of_plot_parts',
                    'charactersString',
                    'groupsString',
                    'groups_incl_charString', 
                    'plot_is_finished' )

    list_filter = [ 'plot_is_finished',
                    #'groups_incl_char',
                    #'groups',
                    #'characters'
                    ]

    inlines = [PlotInlinePlot_line]

admin.site.register(Plot_line, Plot_lineAdmin)


#Plot

class PlotAdmin(admin.ModelAdmin):

    list_display = ('name', 
                    'charactersString',
                    'groupsString',
                    'plot_linesString',
                    'plot_is_finished' )

    list_filter = [ 'plot_is_finished',
                    'plot_lines',
                    'groups',
                    'characters'
                    ]

    list_filter = ['groups', 'characters', 'plot_lines', 'plot_is_finished']

admin.site.register(Plot, PlotAdmin)







