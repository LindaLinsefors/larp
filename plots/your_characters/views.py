from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm

from plots.models import Character


class YourCharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description'   ]


def index(request): 
    return render(request, 'plots/your_characters_index.html',
            { 'character_list':Character.objects.filter(user=request.user) }
    )

def new(request):
    if request.method != 'POST':
        return render(request, 'plots/your_character_edit.html',
                { 'form': YourCharacterForm()   }
        )

    character=Character()
    form = YourCharacterForm(request.POST, instance=character)
    form.save()

    return HttpResponseRedirect(
            reverse('your_characters:character', args=(character.id,) ))
        

def character(request,id):
    character = get_object_or_404(Character, pk=id)
    if character.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = YourCharacterForm(request.POST, instance=character)
        form.save()
    
    return render(request, 'plots/your_character_edit.html',
            { 'form': YourCharacterForm(instance=character)   }
    )



