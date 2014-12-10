from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import PlotThread, PlotPart, PlotPice


def index(request): 
    return render(request, 'plots/GM_index.html',
            { 'plot_threads': PlotThread.objects.all() }    )




class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery', 
                    'plot_is_finished'     ]

class PlotPartForm(forms.ModelForm):
    class Meta:
        model = PlotPart
        fields = [ 'rank' ]

    plot_pice = forms.CharField(widget = forms.Textarea)

    def __init__(self, *args, **kw):
        forms.ModelForm.__init__(self, *args, **kw)
        if kw.has_key('instance'):
            self.fields['plot_pice'].initial = self.instance.plot_pice.plot_pice

    def save(self):
        self.is_valid()
        forms.ModelForm.save(self)
        self.instance.plot_pice.plot_pice = self.cleaned_data['plot_pice']
        self.instance.plot_pice.plot_pice.save()



def plot_thread(request, id): 
    plot_thread = get_object_or_404(PlotThread, pk=id)

    if request.method == 'POST':
        plot_thread_form = PlotThreadForm(request.POST, instance=plot_thread)
        if plot_thread_form.is_valid():
            plot_thread_form.save()
    else: 
        plot_thread_form = PlotThreadForm(instance=plot_thread)    

    plot_part_forms = [ PlotPartForm(instance=plot_part) for plot_part in plot_thread.plotpart_set.all()]

    return render(request, 'plots/GM_plot_thread.html',
           {'plot_thread_form': plot_thread_form,
            'plot_thread': plot_thread ,
            'plot_part_forms': plot_part_forms}   )       

