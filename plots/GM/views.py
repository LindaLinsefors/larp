from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlotPice, PersonalPlotPice, PlotPart, Membership
from plots import for_views


def index(request): 
    return render(request, 'plots/GM_index.html',
              { 'plot_threads': PlotThread.objects.all(),
                'groups': Group.objects.all(),
                'characters': Character.objects.all(),  
                'characters_without_group': 
                       [character for character 
                        in Character.objects.all() 
                        if list( character.membership_set.all() )==[] ]     } )



#Plot Pice

class PlotPiceFormBasic(forms.ModelForm):
    class Meta:
        model=PlotPice
        fields = [ 'plot_pice' ]

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
                                        Character.objects.filter(),
                                        self.instance.characters.filter(), 
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
    else:
        plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM_plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id                  }   )


def new_plot_pice(request, parent_type, parent_id):  
    
    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect(            
                reverse('GM:plot_pice', 
                        args=(parent_type, parent_id, 
                              class_plot_form.instance.id,))  )
    else:
        plot_pice_form = PlotPiceForm()
    
    return render(request, 'plots/GM_plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id                  }   )





#Plot Pice Inline

def save_formset(formset): 
    for form in formset:
        form.save()           


def plots(request, Class, id, ClassForm, InlineFormset, template='plots/GM_plots.html'):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()

        inline_formset = InlineFormset(request.POST, instance=class_instance)
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

    def __init__(self, *args, **kw):
        forms.ModelForm.__init__(self, *args, **kw)
        if kw.has_key('instance'):
            self.fields['plot_pice'].initial = self.instance.plot_pice.plot_pice

    def save(self):
        self.is_valid()
        forms.ModelForm.save(self)
        self.instance.plot_pice.plot_pice = self.cleaned_data['plot_pice']
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
                                            can_delete=False,
                                            extra=0             )

def plot_thread(request, id): 
    return plots(   request, PlotThread, id, PlotThreadForm, PlotPartForms, 
                    template='plots/GM_plot_thread.html'        )

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
                    template='plots/GM_plots.html'        )


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
                    template='plots/GM_personal_plot.html'        )


def new_personal_plot(request): 
    pass


# Group
def group(request, id): 
    pass

def new_group(request): 
    pass

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
    return for_views.form_view( request, Character, id, CharacterForm, 
                                template='plots/GM_character.html'      )


def new_character(request): 
    return for_views.new_view(  request, Character, CharacterForm, 
                                url='GM:character',
                                template='plots/GM_character.html'  )

#Delete

class_dict = {  'group': Group,
                'character': Character,
                'plot_thread': PlotThread   }

def delete(request, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    if request.method == 'POST':
        class_instance.delete()
        return HttpResponseRedirect( reverse('GM:index') )
    
    return render(  request, 'plots/GM_delete.html',
                    {'name': class_instance.name}   )
        
