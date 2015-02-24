from django import forms

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
                    choice_list, old_relations, new_relation_names,  
                    RelationClass, instance_type, choice_type ):

    for choice in choice_list:
        if (        (choice not in old_relations) 
                and (choice.name in new_relation_names) ):
            print choice.name
            RelationClass( **{  choice_type:choice, 
                                instance_type:instance, 
                                'larp':instance.larp,       }).save()

        elif (      (choice in old_relations) 
                and (choice.name not in new_relation_names) ):
            RelationClass.objects.get( **{  choice_type:choice, 
                                            instance_type:instance, 
                                            'larp':instance.larp,   }).delete()     


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


#Plot Head

class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery',  
                    'larps',     ]
        widgets = {'larps': forms.CheckboxSelectMultiple, }

class PlotThreadForm_noLarps(forms.ModelForm):
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
                    'plot_is_finished', 
                    'larp',             ]




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

class CharacterFormBasic(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description',
                    'other_info',               ]
   
    
def CharacterForm(*args, **kw):
    class CharacterFormClass(CharacterFormBasic):

        groups = checkboxes( Group.objects.all() )

        def __init__(self, *args, **kw):
            CharacterFormBasic.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['groups'].initial = self.instance.groups.all()
            
        def save(self):
            self.is_valid()
            CharacterFormBasic.save(self)
            save_relations( self.instance,
                            Group.objects.all(),
                            self.instance.groups.all(), 
                            self.cleaned_data['groups'],
                            Membership, 'character', 'group' )

    return CharacterFormClass(*args, **kw)





#Plot Pice

class PlotPiceFormBasic(forms.ModelForm):
    class Meta:
        model=PlotPice
        fields = [ 'plot_pice', 'plot_is_finished', 'larp' ]
    
    new_character_name = forms.CharField(required=False, max_length=50)
    new_group_name = forms.CharField(required=False, max_length=50)    
    new_plot_thread_name = forms.CharField(required=False, max_length=50)

    def save_new_relation(self, Class, class_name, RelationClass):
        if self.cleaned_data['new_'+class_name+'_name']:
            new_class_instance = Class( name=self.cleaned_data['new_'+class_name+'_name'] )
            new_class_instance.save()

            kw = {  'plot_pice': slef.instance,
                    class_name: new_class_instance,
                    'larp': self.instance.larp,     }
            RelationClass( **kw ).save()



def PlotPiceForm(*args, **kw):

    class PlotPiceFromClass(PlotPiceFormBasic):
        characters = checkboxes( Character.objects.all() )
        groups = checkboxes( Group.objects.all() )
        plot_threads = checkboxes( PlotThread.objects.all() )

        def __init__(self, *args, **kw):
            PlotPiceFormBasic.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['groups'].initial = self.instance.groups.all()
                self.fields['characters'].initial = self.instance.characters.all()
                self.fields['plot_threads'].initial = self.instance.plot_threads.all()

        def save(self):
            self.is_valid()
            forms.ModelForm.save(self)
            save_relations( self.instance,
                            Group.objects.all(),
                            self.instance.groups.all(), 
                            self.cleaned_data['groups'],
                            GroupPlotPice, 'plot_pice', 'group' )
         
            save_relations( self.instance,
                            Character.objects.all(),
                            self.instance.characters.all(), 
                            self.cleaned_data['characters'],
                            PersonalPlotPice, 'plot_pice', 'character' )

            save_relations( self.instance,
                            PlotThread.objects.all(),
                            self.instance.plot_threads.all(), 
                            self.cleaned_data['plot_threads'],
                            PlotPart, 'plot_pice', 'plot_thread' )

            self.save_new_relation(Character, 'character', PersonalPlotPice)
            self.save_new_relation(Group, 'group', GroupPlotPice)
            self.save_new_relation(PlotThread, 'plot_thread', PlotPart)

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

PlotPartForms = forms.inlineformset_factory(LarpPlotThread, PlotPart, 
                                            form=PlotPartForm, 
                                            can_delete=False, #Look in to this
                                            extra=0                             )  



class GroupPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=GroupPlotPice

GroupPlotPiceForms = forms.inlineformset_factory(   GroupPlot, GroupPlotPice, 
                                                    form=GroupPlotPiceForm, 
                                                    can_delete=False,
                                                    extra=0                 )



class PersonalPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PersonalPlotPice

PersonalPlotPiceForms = forms.inlineformset_factory(PersonalPlot, PersonalPlotPice, 
                                                    form=GroupPlotPiceForm, 
                                                    can_delete=False,
                                                    extra=0                 )
