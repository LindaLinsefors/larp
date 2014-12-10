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


def plot_thread(request, id): 
    return render(request, 'plots/GM_plot_thread.html')
