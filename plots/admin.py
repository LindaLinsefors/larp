from django.contrib import admin
from plots.models import *
from django import forms



def make_finished(modeladmin, request, queryset):
    queryset.update(plot_is_finished = True)
make_finished.short_description = "Mark selected as plot is finished"

def make_unfinished(modeladmin, request, queryset):
    queryset.update(plot_is_finished = False)
make_unfinished.short_description = "Mark selected as plot is NOT finished"


def make_open(modeladmin, request, queryset):
    queryset.update(is_open = True)
make_open.short_description = "Open selectd groupe for registration"

def make_closed(modeladmin, request, queryset):
    queryset.update(is_open = False)
make_closed.short_description = "Close selectd groupe for registration"


def publish_members(modeladmin, request, queryset):
    queryset.update(shows_members = True)
publish_members = "Publish members pressentations for selected groups"

def unpublish_members(modeladmin, request, queryset):
    queryset.update(shows_members = False)
unpublish_members = "Un-publish members pressentations for selected groups"




def make_members_presentations(modeladmin, request, queryset):
    for group in queryset:
        group.make_members_presentations()
        group.save()



#Groups

class CharacterInlineGroupe(admin.TabularInline):
    model = Membership
    extra = 0
    #raw_id_fields = ("character",)


class PlotInlineGroupe(admin.TabularInline):
    model = GroupPlotPice
    extra = 0
    

class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                      {'fields': ['name',
                                                ('is_open', 
                                                 'shows_members'),
                                                'plot_is_finished']}),
        ('Group description',       {'fields': ['group_description',
                                                'seceret_comments'], 
                                     'classes': ['collapse']}),
        ('Members presentation',    {'fields': ['members_presentations'], 
                                     'classes': ['collapse']})
    ]

    inlines = [CharacterInlineGroupe, PlotInlineGroupe]

    list_display = ('name', 
                    'no_of_members',
                    'plot_is_finished', 
                    'is_open', 
                    'shows_members')

    list_filter = ['plot_is_finished', 'is_open', 'shows_members']

    actions = [ make_finished, 
                make_unfinished, 
                make_members_presentations,
                publish_members, #Why does not this show
                unpublish_members, #Why does not this show
                make_closed,
                make_open]

admin.site.register(Group, GroupAdmin)


#Characters

class PlotInlineCharacter(admin.TabularInline):
    model = PersonalPloPice
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

    list_display = ('name', 'character_concept', 'groups_string', 'plot_is_finished')
    list_filter = ['groups','plot_is_finished']
    list_editable = ('character_concept',)
    actions = [make_finished, make_unfinished]


admin.site.register(Character, CharacterAdmin)


#PlotThread

class PlotPiceInlinePlotThread(admin.TabularInline):
    model = PersonalPloPice
    extra = 0


class PlotThreadAdmin(admin.ModelAdmin):

    fields =       ('name', 
                    'plot_is_finished',
                    #'characters_string',
                    #'groups_string',
                    #'groups_incl_char_string'
                    )

    list_display = ('name', 
                    'no_of_plot_parts',
                    'characters_string',
                    'groups_string',
                    'groups_incl_char_string', 
                    'plot_is_finished' )

    list_filter = [ 'plot_is_finished',
                    #'groups_incl_char',
                    #'groups',
                    #'characters'
                    ]

    inlines = [PlotPiceInlinePlotThread]
    actions = [make_finished, make_unfinished]


admin.site.register(PlotThread, PlotThreadAdmin)


#PlotPice

class PlotPiceAdmin(admin.ModelAdmin):


    list_display = ('name', 
                    'characters_string',
                    'groups_string',
                    'plot_lines_string',
                    'plot_is_finished' )

    list_filter = [ 'plot_is_finished',
                    'plot_lines',
                    'groups',
                    'characters'
                    ]

    actions = [make_finished, make_unfinished]


admin.site.register(Plot, PlotAdmin)







