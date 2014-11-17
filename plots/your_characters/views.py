from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from plots.models import Group


def index(request):
    return HttpResponse('Here should be a list of your characters and a button to make new ones')

def character(request,id):
    return HttpResponse('Here should be a character form')
