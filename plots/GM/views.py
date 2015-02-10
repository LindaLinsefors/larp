from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlotPice, PersonalPlotPice, PlotPart, Membership
from plots import for_views


def index(request): 
    return render(request, 'plots/GM/index.html',
              { 'plot_threads': PlotThread.objects.all(),
                'groups': Group.objects.all(),
                'characters': Character.objects.all(),  
                # There is probably a better way to do this with filter
                'characters_without_group': 
                   [character for character 
                    in Character.objects.all() 
                    if list( character.membership_set.all() )==[] ],
                'plot_pices_without_character_or_group':
                   [plot_pice for plot_pice
                    in PlotPice.objects.all()
                    if (list( plot_pice.characters.all() )==[]
                        and list( plot_pice.groups.all() )==[] ) ],   
                'plot_pices_without_plot_thread':
                   [plot_pice for plot_pice
                    in PlotPice.objects.all()
                    if list( plot_pice.plot_threads.all() )==[] ],       
                } )



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




def plot_pice(request, parent_type, parent_id, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)

    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect(            
                reverse('GM:'+parent_type, args=( parent_id,))  )

    plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id                  }   )


def plot_pice_no_parent(request, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)

    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect( reverse('GM:index') )

    plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:index'         }   )


def new_plot_pice(request, parent_type, parent_id):  
    
    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect(            
                reverse('GM:'+parent_type, args=( parent_id,))  )
    else:
        plot_pice_form = PlotPiceForm()
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id                  }   )





#Plot Pice Inline

def save_formset(formset): #Is this needed?
    for form in formset:
        form.save()           


def plots(request, Class, id, ClassForm, InlineFormset, template='plots/GM/plots.html'):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()

        inline_formset = InlineFormset(request.POST, instance=class_instance)
        #import pdb; pdb.set_trace()
        if inline_formset.is_valid():
            save_formset(inline_formset)

    class_form = ClassForm(instance=class_instance)
    inline_formset = InlineFormset(instance=class_instance)

    return render(request, template,
           {'class_form': class_form,
            'class_instance': class_instance ,
            'plot_pice_forms': inline_formset}   )   


class PlotPiceInlineForm(forms.ModelForm):
    class Meta:
        fields = [ 'rank' ]

    plot_pice = forms.CharField(widget=forms.Textarea, required=False)
    plot_is_finished = forms.BooleanField(required=False) 

    def __init__(self, *args, **kw):
        forms.ModelForm.__init__(self, *args, **kw)
        if kw.has_key('instance'):
            self.fields['plot_pice'].initial = self.instance.plot_pice.plot_pice
            self.fields['plot_is_finished'].initial = self.instance.plot_pice.plot_is_finished

    def save(self):
        self.is_valid()
        forms.ModelForm.save(self)
        self.instance.plot_pice.plot_pice = self.cleaned_data['plot_pice']
        self.instance.plot_pice.plot_is_finished = self.cleaned_data['plot_is_finished']
        self.instance.plot_pice.save()


#Plot Thread

class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery', 
                    'plot_is_finished'     ]

class PlotPartForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PlotPart

PlotPartForms = forms.inlineformset_factory(PlotThread, PlotPart, 
                                            form=PlotPartForm, 
                                            can_delete=False, #Look in to this
                                            extra=0             )

def plot_thread(request, id): 
    return plots(   request, PlotThread, id, PlotThreadForm, PlotPartForms, 
                    template='plots/GM/plot_thread.html'        )

def new_plot_thread(request):
    pass 



# Group Plot

class GroupPlotForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [  'secret_comments',   
                    'plot_is_finished'     ]

class GroupPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PlotPart

GroupPlotPiceForms = forms.inlineformset_factory(   Group, GroupPlotPice, 
                                                    form=GroupPlotPiceForm, 
                                                    can_delete=False,
                                                    extra=0                 )

def group_plot(request, id): 
    return plots(   request, Group, id, GroupPlotForm, GroupPlotPiceForms, 
                    template='plots/GM/plots.html'        )


# Personal Plot

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




class PersonalPlotPiceForm(PlotPiceInlineForm):
    class Meta(PlotPiceInlineForm.Meta):
        model=PersonalPlotPice

PersonalPlotPiceForms = forms.inlineformset_factory(Character, PersonalPlotPice, 
                                                    form=GroupPlotPiceForm, 
                                                    can_delete=False,
                                                    extra=0                 )

def personal_plot(request, id): 
    return plots(   request, Character, id, PersonalPlotForm, PersonalPlotPiceForms, 
                    template='plots/GM/personal_plot.html'        )


def new_personal_plot(request): 
    pass


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
        

def save_group(request):
    print request.POST

def group(request, id): 
    group = get_object_or_404(Group, pk=id)
    half = ( Character.objects.count()+1 )/2
    return render(request, 'plots/GM/group.html',
            {   'group': group, 
                'members': group.character_set.all(),
                'characters_fist_half': Character.objects.all()[:half],
                'characters_second_half': Character.objects.all()[half:],
            }   )

def new_group(request): 
    return for_views.new(  request, Group, GroupForm, 
                           url='GM:group',       )

def members_old(request, id, back): # This one works
    return for_views.edit( request, Group, id, MembersForm  )

def members(request, id, back):
    group = get_object_or_404(Group, pk=id)

    if request.method == 'POST':
        members_form = MembersForm(request.POST, instance=group)
        if members_form.is_valid():
            members_form.save()
            return HttpResponseRedirect( back )

    members_form = MembersForm(instance=group)
    
    return render(request, 'plots/GM/members.html',
            {   'members_form': members_form,
                'group': group,                 }   )

def members_from_index(request, id):
    return members(request, id, reverse('GM:index') )

def members_from_parent(request, id, parent_type ):
    return members( request, id, 
                    reverse('GM:'+parent_type, args=(id,)) )

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



def character(request, id): 
    return for_views.edit( request, Character, id, CharacterForm, 
                                template='plots/GM/character.html'   )


def new_character(request): 
    return for_views.new(  request, Character, CharacterForm, 
                                url='GM:character',
                                template='plots/GM/character.html'  )

#Delete

class_dict = {  'group': Group,
                'character': Character,
                'plot_thread': PlotThread,
                'plot_pice': PlotPice   }

def delete(request, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    if request.method == 'POST':
        class_instance.delete()
        return HttpResponseRedirect( reverse('GM:index') )
    
    if class_name == 'plot_pice': 
        name = 'Plot Pice'
    else: 
        name = class_instance.name
        
    return render(  request, 'plots/GM/delete.html',
                   {'name': name,
                    'back': reverse('GM:'+class_name, args=(id,)) })
        

def delete_plot_pice(request, parent_type, parent_id, id):
    plot_pice = get_object_or_404(PlotPice, pk=id)
    if request.method == 'POST':
        plot_pice.delete()
        return HttpResponseRedirect( 
                reverse('GM:'+parent_type, args=(parent_id,) ))

    return render( request, 'plots/GM/delete.html',
                   {'name': 'Plot Pice',
                    'back': reverse('GM:'+class_name, 
                                    args=(parent_type, parent_id, id)) 
                    })


