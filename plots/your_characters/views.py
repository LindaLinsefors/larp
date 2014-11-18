from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm

from plots.models import Character


class YourCharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'groups', 
                    'presentation', 
                    'character_description'   ]


def index(request): 
    return render(request, 'plots/your_characters_index.html',
            { 'character_list':Character.objects.filter(user=request.user) }
    )

def new(request):
    return HttpResponse('Make a new character')

def character(request,id):
    character = get_object_or_404(Character, pk=id)
    if character.user != request.user:
        raise PermissionDenied
    return render(request, 'plots/your_character_form.html',
            {   'character':character,
                'form': YourCharacterForm(instance=character)   }
    )



