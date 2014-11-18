from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import Character, Group


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description'   ]



class GroupForm(forms.Form):
    groups = forms.MultipleChoiceField(
                    widget  = forms.CheckboxSelectMultiple , 
                    choices = [ (group, group.name) 
                                for group
                                in Group.objects.filter(is_open=True)   ] 
    ) 


def index(request): 
    return render(request, 'plots/your_characters_index.html',
            { 'character_list':Character.objects.filter(user=request.user) }
    )

def new(request):
    if request.method != 'POST':
        return render(request, 'plots/your_character_edit.html',
               {'character_form': CharacterForm(),
                'group_form': GroupForm()  }
        )

    character=Character(user=request.user)
    character_form = CharacterForm(request.POST, instance=character)
    character_form.save()

    return HttpResponseRedirect(
            reverse('your_characters:character', args=(character.id,) ))
        

def character(request,id):
    character = get_object_or_404(Character, pk=id)
    if character.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        character_form = CharacterForm(request.POST, instance=character)
        character_form.save()
        group_form = GroupForm(request.POST)
        
    else: 
        group_data = {'groups': character.groups.filter(is_open=True)}        
        group_form = GroupForm(group_data)

    return render(request, 'plots/your_character_edit.html',
               {'character_form': CharacterForm(instance=character),
                'group_form': group_form  }   
    )


