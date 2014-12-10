from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import PlotThread


def index(request): 
    return render(request, 'plots/GM_index.html',
            { 'plot_threads': PlotThread.objects.all() }    )




class PlotThreadForm(forms.ModelForm):
    class Meta:
        model = PlotThread
        fields = [  'name', 
                    'summery', 
                    'plot_is_finished'     ]



def plot_thread(request, id): 
    plot_thread = get_object_or_404(PlotThread, pk=id)

    if request.method == 'POST':
        plot_thread_form = PlotThreadForm(request.POST, instance=plot_thread)
        if plot_thread_form.is_valid():
            plot_thread_form.save()
    else: 
        plot_thread_form = PlotThreadForm(instance=plot_thread)     

    return render(request, 'plots/GM_plot_thread.html',
           {'plot_thread_form': plot_thread_form,
            'plot_thread': plot_thread }   )       

