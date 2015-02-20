from django import forms

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlotPice, PersonalPlotPice, PlotPart, Membership



#Plot Head

class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery', 
                    'plot_is_finished'     ]


class GroupPlotForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [  'secret_comments',   
                    'plot_is_finished'     ]


class PersonalPlotForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'secret_comments',   
                    'plot_is_finished',
                    'character_description',
                    'other_info'             ]

    character_description = forms.CharField(
            widget=forms.Textarea(attrs={'readonly':'readonly'}), 
            required=False,      )

    other_info = forms.CharField(
            widget=forms.Textarea(attrs={'readonly':'readonly'}), 
            required=False,      )




# Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [  'name',
                    'is_open',
                    'show_group',
                    'show_members',
                    'group_description',
                    'members_presentations',
                    'secret_comments',       ]


def MembersForm(*args, **kw):
    class MembersFormClass(forms.ModelForm):
        class Meta:
            model = Group
            fields = []

        characters = for_views.checkboxes( Character.objects.all() )

        def __init__(self, *args, **kw):
            forms.ModelForm.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['characters'].initial = self.instance.character_set.all()

        def save(self):
            self.is_valid()
            forms.ModelForm.save(self)
         
            for_views.save_relations(   self.instance,
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
                    'other_info',
                    'secret_comments'       ]
   
    
def CharacterForm(*args, **kw):
    class CharacterFormClass(CharacterFormBasic):

        groups = for_views.checkboxes( Group.objects.all() )

        def __init__(self, *args, **kw):
            CharacterFormBasic.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['groups'].initial = self.instance.groups.all()
            
        def save(self):
            self.is_valid()
            CharacterFormBasic.save(self)
            for_views.save_relations(   self.instance,
                                        Group.objects.all(),
                                        self.instance.groups.all(), 
                                        self.cleaned_data['groups'],
                                        Membership, 'character', 'group' )

    return CharacterFormClass(*args, **kw)





#Plot Pice

class PlotPiceFormBasic(forms.ModelForm):
    class Meta:
        model=PlotPice
        fields = [ 'plot_pice', 'plot_is_finished' ]
    
    new_character_name = forms.CharField(required=False, max_length=50)
    new_group_name = forms.CharField(required=False, max_length=50)    
    new_plot_thread_name = forms.CharField(required=False, max_length=50)

    def save_new_relation(self, Class, class_name, RelationClass):
        if self.cleaned_data['new_'+class_name+'_name']:
            new = Class( name=self.cleaned_data['new_'+class_name+'_name'] )
            new.save()
            RelationClass( plot_pice=self.instance, plot_thread=new ).save()

        def save(self):
            self.is_valid()
            forms.ModelForm.save(self)
            self.save_new_relation(Character, character, CharacterPlotPice)
            self.save_new_relation(Group, group, GroupPlotPice)
            self.save_new_relation(PlotThread, PlotThread, PlotPart)



def PlotPiceForm(*args, **kw):

    class PlotPiceFromClass(PlotPiceFormBasic):
        characters = for_views.checkboxes( Character.objects.all() )
        groups = for_views.checkboxes( Group.objects.all() )
        plot_threads = for_views.checkboxes( PlotThread.objects.all() )

        def __init__(self, *args, **kw):
            PlotPiceFormBasic.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['groups'].initial = self.instance.groups.all()
                self.fields['characters'].initial = self.instance.characters.all()
                self.fields['plot_threads'].initial = self.instance.plot_threads.all()

        def save(self):
            self.is_valid()
            PlotPiceFormBasic.save(self)
            for_views.save_relations(   self.instance,
                                        Group.objects.all(),
                                        self.instance.groups.all(), 
                                        self.cleaned_data['groups'],
                                        GroupPlotPice, 'plot_pice', 'group' )
         
            for_views.save_relations(   self.instance,
                                        Character.objects.all(),
                                        self.instance.characters.all(), 
                                        self.cleaned_data['characters'],
                                        PersonalPlotPice, 'plot_pice', 'character' )

            for_views.save_relations(   self.instance,
                                        PlotThread.objects.all(),
                                        self.instance.plot_threads.all(), 
                                        self.cleaned_data['plot_threads'],
                                        PlotPart, 'plot_pice', 'plot_thread' )
            
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

PlotPartForms = forms.inlineformset_factory(PlotThread, PlotPart, 
                                            form=PlotPartForm, 
                                            can_delete=False, #Look in to this
                                            extra=0                             )  



class GroupPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PlotPart

GroupPlotPiceForms = forms.inlineformset_factory(   Group, GroupPlotPice, 
                                                    form=GroupPlotPiceForm, 
                                                    can_delete=False,
                                                    extra=0                 )



class PersonalPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PersonalPlotPice

PersonalPlotPiceForms = forms.inlineformset_factory(Character, PersonalPlotPice, 
                                                    form=GroupPlotPiceForm, 
                                                    can_delete=False,
                                                    extra=0                 )
