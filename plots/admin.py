from django.contrib import admin
from plots.models import *
from django import forms



def make_finished(modeladmin, request, queryset):
    queryset.update(plot_is_finished = True)
make_finished.short_description = "Mark plots as finished"

def make_unfinished(modeladmin, request, queryset):
    queryset.update(plot_is_finished = False)
make_unfinished.short_description = "Mark plots as not finished"


def make_open(modeladmin, request, queryset):
    queryset.update(is_open = True)
make_open.short_description = "Open for registration"

def make_closed(modeladmin, request, queryset):
    queryset.update(is_open = False)
make_closed.short_description = "Close for registration"


def publish_members(modeladmin, request, queryset):
    queryset.update(show_members = True)
publish_members.short_description = "Publish members pressentations"

def unpublish_members(modeladmin, request, queryset):
    queryset.update(show_members = False)
unpublish_members.short_description = "Un-publish members pressentations"


def make_secret(modeladmin, request, queryset):
    queryset.update(secret = True)


def make_not_secret(modeladmin, request, queryset):
    queryset.update(secret = False)




def make_members_presentations(modeladmin, request, queryset):
    for group in queryset:
        group.make_members_presentations()
        group.save()




#PlotPice
class PlotPiceInline(admin.TabularInline):
    extra = 0
    fields = ('plot_pice_name','plot_pice','rank')
    readonly_fields = ( 'plot_pice', )




#Groups

class Character_in_Groupe(admin.TabularInline):
    model = Membership
    extra = 0

class PlotPice_in_Groupe(PlotPiceInline):
    model = GroupPlotPice
    extra = 0  

class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                      {'fields': ['name',
                                                ('is_open', 
                                                 'show_members',
                                                 'secret'),
                                                'plot_is_finished']}),
        ('Group description',       {'fields': ['group_description',
                                                'secret_comments'], 
                                     'classes': ['collapse']}),
        ('Members presentation',    {'fields': ['members_presentations'], 
                                     'classes': ['collapse']})
    ]

    inlines = [Character_in_Groupe, PlotPice_in_Groupe]

    list_display = ('name', 
                    'no_of_members',
                    'plot_is_finished', 
                    'is_open', 
                    'show_members',
                    'secret')

    list_filter = ['plot_is_finished', 'is_open', 'show_members']

    actions = [ make_members_presentations,
                publish_members, 
                unpublish_members, 
                make_finished, 
                make_unfinished, 
                make_closed,
                make_open,
                make_secret,
                make_not_secret]

admin.site.register(Group, GroupAdmin)




#Characters

class Group_in_Character(admin.TabularInline):
    model = Membership
    extra = 0
    exclude = ('rank',)

class PlotPice_in_Character(PlotPiceInline):
    model = PersonalPlotPice
    extra = 0  
 

class CharacterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                      {'fields': [('name',
                                                'character_concept','user'),
                                                'plot_is_finished']}),
        ('Character description',   {'fields': ['presentation',
                                                'character_description',
                                                'comments_to_player',
                                                'seceret_comments'], 
                                     'classes': ['collapse']})
    ]

    inlines = [Group_in_Character, PlotPice_in_Character]

    list_display = ('name', 'character_concept', 'user', 'groups_string', 'plot_is_finished')
    list_filter = ['groups','plot_is_finished']
    list_editable = ('character_concept',)
    actions = [make_finished, make_unfinished]
 

admin.site.register(Character, CharacterAdmin)


#PlotThread

class PlotPice_in_PlotThread(PlotPiceInline):
    model = PlotPart


class PlotThreadAdmin(admin.ModelAdmin):

    readonly_fields = ( 'characters_string',
                        'groups_string',
                        'groups_incl_char_string'   )

    fieldsets = [
        (None,  {'fields': ['name','summery',
                            (   'characters_string',
                                'groups_string',
                                'groups_incl_char_string'   ),
                            'plot_is_finished'  ] } )
                ]


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

    inlines = [PlotPice_in_PlotThread]
    actions = [make_finished, make_unfinished]


admin.site.register(PlotThread, PlotThreadAdmin)


#PlotPice

class Character_in_PlotPice(admin.TabularInline):
    model = PersonalPlotPice
    extra = 0
    exclude = ('rank',)

class Group_in_PlotPice(admin.TabularInline):
    model = GroupPlotPice
    extra = 0
    exclude = ('rank',)

class PlotThread_in_PlotPice(admin.TabularInline):
    model = PlotPart
    extra = 0
    exclude = ('rank',)


class PlotPiceAdmin(admin.ModelAdmin):

    list_display = ('name', 
                    'characters_string',
                    'groups_string',
                    'plot_threads_string',
                    'plot_is_finished' )

    list_filter = [ 'plot_is_finished',
                    'plot_threads',
                    'groups',
                    'characters'    ]

    actions = [make_finished, make_unfinished]

    inlines = [ Character_in_PlotPice, 
                Group_in_PlotPice, 
                PlotThread_in_PlotPice  ]


admin.site.register(PlotPice, PlotPiceAdmin)







