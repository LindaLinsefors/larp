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
        print 'plot thread saved'
        self.is_valid()
        forms.ModelForm.save(self)
        self.instance.plot_pice.plot_pice = self.cleaned_data['plot_pice']
        self.instance.plot_pice.save()


PlotPartForms = forms.inlineformset_factory(PlotThread, PlotPart, 
                                            form=PlotPartForm, 
                                            can_delete=False,
                                            extra=0 )
def save_formset(formset):
    for form in formset:
        form.save()


def plot_thread(request, id): 
    plot_thread = get_object_or_404(PlotThread, pk=id)

    if request.method == 'POST':
        plot_thread_form = PlotThreadForm(request.POST, instance=plot_thread)
        if plot_thread_form.is_valid():
            plot_thread_form.save()

        plot_part_forms = PlotPartForms(request.POST, instance=plot_thread)
        if plot_part_forms.is_valid():
            save_formset(plot_part_forms)
        else: 
            print 'Errors: ' +  plot_part_forms.errors

    else: 
        plot_thread_form = PlotThreadForm(instance=plot_thread)   
    plot_part_forms = PlotPartForms(instance=plot_thread) 

    #plot_part_forms = [ PlotPartForm(instance=plot_part) for plot_part in plot_thread.plotpart_set.all()]

    return render(request, 'plots/GM_plot_thread.html',
           {'plot_thread_form': plot_thread_form,
            'plot_thread': plot_thread ,
            'plot_part_forms': plot_part_forms}   )      




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




def plot_pice(request, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)

    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
    else:
        plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM_plot_pice.html',
            {'plot_pice_form': plot_pice_form} )


