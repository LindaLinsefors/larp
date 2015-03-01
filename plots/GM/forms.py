from django import forms as djangoforms
import floppyforms.__future__  as forms

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlotPice, PersonalPlotPice, PlotPart, Membership, Larp, LarpPlotThread, PersonalPlot, GroupPlot



#Help functions

def checkboxes(choice_list):
    return forms.MultipleChoiceField(
                    required = False,
                    widget  = forms.CheckboxSelectMultiple , 
                    choices = [ (choice, choice.name) 
                                for choice
                                in choice_list   ] )

def save_relations( instance,
                    choice_list, old_relations, new_relations,  
                    RelationClass, instance_type, choice_type ):

    for choice in choice_list:
        if (        (choice not in old_relations) 
                and (choice in new_relations) ):

            RelationClass( **{  choice_type:choice, 
                                instance_type:instance, }).save()

        elif (      (choice in old_relations) 
                and (choice not in new_relations) ):
            RelationClass.objects.get( **{  choice_type:choice, 
                                            instance_type:instance, }).delete()     


#Larp

class LarpForm(forms.ModelForm):
    class Meta:
        model = Larp
        fields = [  'name',
                    'groups',
                    'plot_threads',
                    'characters',    ]
        widgets = {
            'groups': forms.CheckboxSelectMultiple,
            'plot_threads': forms.CheckboxSelectMultiple,
            'characters': forms.CheckboxSelectMultiple,     }

    def save(self):
        larp = self.instance
        larp.name = self.cleaned_data['name']
        larp.save()
        save_relations( larp,
                        Group.objects.all(), 
                        larp.groups.all(), self.cleaned_data['groups'],
                        GroupPlot, 'larp', 'group')

        save_relations( larp,
                        PlotThread.objects.all(), 
                        larp.plot_threads.all(), self.cleaned_data['plot_threads'],
                        LarpPlotThread, 'larp', 'plot_thread')

        save_relations( larp,
                        Character.objects.all(), 
                        larp.characters.all(), self.cleaned_data['characters'],
                        PersonalPlot, 'larp', 'character')




#Plot Head

class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery',  
                    'larps',     ]
        widgets = {'larps': forms.CheckboxSelectMultiple, }

    def save(self):
        plot_thread = self.instance
        plot_thread.name = self.cleaned_data['name']
        plot_thread.summery = self.cleaned_data['summery']
        plot_thread.save()
        save_relations( plot_thread,
                        Larp.objects.all(), 
                        plot_thread.larps.all(), self.cleaned_data['larps'],
                        LarpPlotTread, 'plot_thread', 'larp')



class PlotThreadFormLarp(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery',   ]




class LarpPlotThreadForm(forms.ModelForm):
    name = PlotThreadForm.base_fields['name']
    summery = PlotThreadForm.base_fields['summery']
    class Meta:
        model = LarpPlotThread
        fields = [  'name',
                    'summery',
                    'plot_is_finished',  ]

    def __init__(self, *args, **kw):
        forms.ModelForm.__init__(self, *args, **kw)
        if kw.has_key('instance'):
            self.fields['name'].initial = self.instance.plot_thread.name
            self.fields['summery'].initial = self.instance.plot_thread.summery

    def save(self):
        self.is_valid()
        forms.ModelForm.save(self)
        self.instance.plot_thread.name = self.cleaned_data['name']
        self.instance.plot_thread.summery = self.cleaned_data['summery']
        self.instance.plot_thread.save()




class GroupPlotForm(forms.ModelForm):
    class Meta:
        model = GroupPlot
        fields = [  'secret_comments',   
                    'plot_is_finished',  ]


class PersonalPlotForm(forms.ModelForm):
    class Meta:
        model = PersonalPlot
        fields = [  'secret_comments',   
                    'plot_is_finished', ]




# Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [  'name',
                    'group_description',
                    'is_open',
                    'show_group',
                    'show_members',
                    'larps',
                    'characters',       ]
        widgets = { 'larps': forms.CheckboxSelectMultiple,
                    'characters': forms.CheckboxSelectMultiple,  }

    def save(self):
        group = self.instance
        group.name = self.cleaned_data['name']
        group.group_description = self.cleaned_data['group_description']
        group.is_open = self.cleaned_data['is_open']
        group.show_group = self.cleaned_data['show_group']
        group.show_members = self.cleaned_data['show_members']
        group.save()
        save_relations( group,
                        Larp.objects.all(), 
                        group.larps.all(), self.cleaned_data['larps'],
                        GroupPlot, 'group', 'larp')

        save_relations( group,
                        Character.objects.all(), 
                        group.characters.all(), self.cleaned_data['characters'],
                        Membership, 'group', 'character')


class GroupFormLarp(forms.ModelForm):
    class Meta:
        model = Group
        fields = [  'name',
                    'group_description',
                    'is_open',
                    'show_group',
                    'show_members',
                    'characters',       ]

        widgets = { 'characters': forms.CheckboxSelectMultiple,  }

    def save(self):
        group = self.instance
        group.name = self.cleaned_data['name']
        group.group_description = self.cleaned_data['group_description']
        group.is_open = self.cleaned_data['is_open']
        group.show_group = self.cleaned_data['show_group']
        group.show_members = self.cleaned_data['show_members']
        group.save()

        save_relations( group,
                        Character.objects.all(), 
                        group.characters.all(), self.cleaned_data['characters'],
                        Membership, 'group', 'character')



def MembersForm(*args, **kw):
    class MembersFormClass(forms.ModelForm):
        class Meta:
            model = Group
            fields = []

        characters = checkboxes( Character.objects.all() )

        def __init__(self, *args, **kw):
            forms.ModelForm.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['characters'].initial = self.instance.character_set.all()

        def save(self):
            self.is_valid()
            forms.ModelForm.save(self)
         
            save_relations( self.instance,
                            Character.objects.all(),
                            self.instance.character_set.all(), 
                            self.cleaned_data['characters'],
                            Membership, 'character', 'group' )

    return MembersFormClass(*args, **kw)


# Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description',
                    'other_info',               
                    'groups',
                    'larps',               ]

        widgets = { 'larps': forms.CheckboxSelectMultiple,
                    'groups': forms.CheckboxSelectMultiple,  }

    def save(self):
        character = self.instance
        character.name = self.cleaned_data['name']
        character.character_concept = self.cleaned_data['character_concept']
        character.presentation = self.cleaned_data['presentation']
        character.character_description = self.cleaned_data['character_description']
        character.other_info = self.cleaned_data['other_info']
        character.save()
        save_relations( character,
                        Larp.objects.all(), 
                        character.larps.all(), self.cleaned_data['larps'],
                        PersonalPlot, 'character', 'larp')

        save_relations( character,
                        Group.objects.all(), 
                        character.groups.all(), self.cleaned_data['groups'],
                        Membership, 'character', 'group')


class CharacterFormLarp(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description',
                    'other_info',               
                    'groups',              ]

        widgets = { 'groups': forms.CheckboxSelectMultiple,  }

    def save(self):
        character = self.instance
        character.name = self.cleaned_data['name']
        character.character_concept = self.cleaned_data['character_concept']
        character.presentation = self.cleaned_data['presentation']
        character.character_description = self.cleaned_data['character_description']
        character.other_info = self.cleaned_data['other_info']
        character.save()

        save_relations( character,
                        Group.objects.all(), 
                        character.groups.all(), self.cleaned_data['groups'],
                        Membership, 'character', 'group')

   



#Plot Pice

def PlotPiceForm(larp, *args, **kw):

    class PlotPiceFromClass(forms.ModelForm):
        class Meta:
            model=PlotPice
            fields = [  'plot_pice', 
                        'plot_is_finished',  
                        'larp_plot_threads',
                        'group_plots',
                        'personal_plots',]

            widgets = { 'group_plots': forms.CheckboxSelectMultiple(
                                choices = GroupPlot.objects.filter(larp=larp)   ),

                        'personal_plots': forms.CheckboxSelectMultiple(
                                choices = PersonalPlot.objects.filter(larp=larp)    ),

                        'larp_plot_threads': forms.CheckboxSelectMultiple(
                                choices = LarpPlotThread.objects.filter(larp=larp)  ),  }
        
        new_character_name = forms.CharField(required=False, max_length=50)
        new_group_name = forms.CharField(required=False, max_length=50)    
        new_plot_thread_name = forms.CharField(required=False, max_length=50)

        def save_new_relation(self, Class, class_name, PlotClass, plot_name, RelationClass):
            if self.cleaned_data['new_'+class_name+'_name']:
                new_class_instance = Class( name=self.cleaned_data['new_'+class_name+'_name'] )
                new_class_instance.save()
                new_plot_instance = PlotClass( **{'plot':plot, class_name: new_class_instance} )
                new_plot_instance.save() 
                RelationClass( **{  'plot_pice': self.instance,
                                    plot_name: new_plot_instance,
                                    'rank': -1,                     } ).save()

        def save(self):
            self.is_valid()

            plot_pice = self.instance
            plot_pice.larp = larp
            plot_pice.plot_pice = self.cleaned_data['plot_pice']
            plot_pice.plot_is_finished = self.cleaned_data['plot_is_finished']

            save_relations( self.instance,
                            larp.groupplot_set.all(),
                            self.instance.group_plots.all(), 
                            self.cleaned_data['group_plots'],
                            GroupPlotPice, 'plot_pice', 'group_plot' )
         
            save_relations( self.instance,
                            larp.personalplot_set.all(),
                            self.instance.personal_plots.all(), 
                            self.cleaned_data['personal_plots'],
                            PersonalPlotPice, 'plot_pice', 'personal_plot' )

            save_relations( self.instance,
                            larp.larpplotthread_set.all(),
                            self.instance.larp_plot_threads.all(), 
                            self.cleaned_data['larp_plot_threads'],
                            PlotPart, 'plot_pice', 'larp_plot_thread' )

            self.save_new_relation( Character, 'character', 
                                    PersonalPlot, 'personal_plot', 
                                    PersonalPlotPice,                )

            self.save_new_relation( Group, 'group', 
                                    GroupPlot, 'group_plot',
                                    GroupPlotPice,               )

            self.save_new_relation( PlotThread, 'plot_thread', 
                                    LarpPlotThread, 'larp_plot_thread', 
                                    PlotPart,                           )

    return PlotPiceFromClass(*args, **kw)


#Plot Pice Inline

class PlotPiceInlineForm(forms.ModelForm):
    class Meta:
        fields = [ ]

    plot_pice_text = forms.CharField(widget=forms.Textarea, required=False)
    plot_is_finished = forms.BooleanField(required=False) 

    def __init__(self, *args, **kw):
        forms.ModelForm.__init__(self, *args, **kw)
        if kw.has_key('instance'):
            self.fields['plot_pice_text'].initial = self.instance.plot_pice.plot_pice
            self.fields['plot_is_finished'].initial = self.instance.plot_pice.plot_is_finished

    def save(self):
        self.is_valid()
        forms.ModelForm.save(self)
        self.instance.plot_pice.plot_pice = self.cleaned_data['plot_pice_text']
        self.instance.plot_pice.plot_is_finished = self.cleaned_data['plot_is_finished']
        self.instance.plot_pice.save()




class PlotPartForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PlotPart

PlotPartForms = djangoforms.inlineformset_factory(
                                LarpPlotThread, PlotPart, 
                                form=PlotPartForm, 
                                can_delete=False, #Look in to this
                                extra=0                             )  



class GroupPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=GroupPlotPice

GroupPlotPiceForms = djangoforms.inlineformset_factory(   
                                    GroupPlot, GroupPlotPice, 
                                    form=GroupPlotPiceForm, 
                                    can_delete=False,
                                    extra=0                 )



class PersonalPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PersonalPlotPice

PersonalPlotPiceForms = djangoforms.inlineformset_factory(
                                PersonalPlot, PersonalPlotPice, 
                                form=GroupPlotPiceForm, 
                                can_delete=False,
                                extra=0                 )
