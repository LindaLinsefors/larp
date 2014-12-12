from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlotPice, PersonalPlotPice, PlotPart
from plots import for_views


def index(request): 
    return render(request, 'plots/GM_index.html',
            { 'plot_threads': PlotThread.objects.all() }    )




class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery', 
                    'plot_is_finished'     ]



#Plot Thread

class PlotPartForm(forms.ModelForm):
    class Meta:
        model = PlotPart
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


PlotPartForms = forms.inlineformset_factory(PlotThread, PlotPart, 
                                            form=PlotPartForm, 
                                            can_delete=False,
                                            extra=0 )

def plots(request, Class, id, ClassForm, InlineFormset, template='plots/GM_plots.html'):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()

        inline_formset = InlineFormset(request.POST, instance=class_instance)
        import pdb; pdb.set_trace()
        if inline_formset.is_valid():
            inline_formset.save()

    class_form = ClassForm(instance=class_instance)
    inline_formset = InlineFormset(instance=class_instance)

    return render(request, template,
           {'class_form': class_form,
            'class_instance': class_instance ,
            'plot_pice_forms': inline_formset}   )   

           


def plot_thread_new(request, id): 
    return plots(   request, PlotThread, id, PlotThreadForm, PlotPartForms, 
                    template='plots/GM_plot_thread.html'        )




def plot_thread(request, id):
    plot_thread = get_object_or_404(PlotThread, pk=id)

    if request.method == 'POST':
        plot_thread_form = PlotThreadForm(request.POST, instance=plot_thread)
        if plot_thread_form.is_valid():
            plot_thread_form.save()

        plot_part_forms = PlotPartForms(request.POST, instance=plot_thread)
        if plot_part_forms.is_valid():
            plot_part_forms.save()
    else:
        plot_thread_form = PlotThreadForm(instance=plot_thread)
    plot_part_forms = PlotPartForms(instance=plot_thread)
    
    return render(request, 'plots/GM_plot_thread.html',
           {'plot_thread_form': plot_thread_form,
            'plot_thread': plot_thread ,
            'plot_pice_forms': plot_part_forms}     ) 


# Group Plot




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


