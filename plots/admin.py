from django.contrib import admin
from plots.models import *
from django import forms



def make_finished(modeladmin, request, queryset):
    queryset.update(plot_is_finished = True)
make_finished.short_description = "Mark selected as plot is finished"

def make_unfinished(modeladmin, request, queryset):
    queryset.update(plot_is_finished = False)
make_unfinished.short_description = "Mark selected as plot is NOT finished"

def make_members_pressentation(modeladmin, request, queryset):
    for group in queryset:
        group.make_members_pressentation()



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
        (None,                      {'fields': ['name',
                                                'plot_is_finished']}),
        ('Group description',       {'fields': ['group_description',
                                                'seceret_comments'], 
                                     'classes': ['collapse']}),
        ('Members presentation',    {'fields': ['members_presentation'], 
                                     'classes': ['collapse']})
    ]

    inlines = [CharacterInlineGroupe, PlotInlineGroupe]
    list_display = ('name', 'no_of_members', 'plot_is_finished')
    list_filter = ['plot_is_finished']
    actions = [make_finished, make_unfinished]

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
    list_editable = ('character_concept',)
    actions = [make_finished, make_unfinished]


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
    actions = [make_finished, make_unfinished]


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
    actions = [make_finished, make_unfinished]


admin.site.register(Plot, PlotAdmin)







