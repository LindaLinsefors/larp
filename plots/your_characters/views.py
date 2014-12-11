from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import Character, Group, Membership
from plots import for_views


class YourCharacterFormBasic(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description'   ]


def YourCharacterForm(*args, **kw):
    class YourCharacterFormClass(YourCharacterFormBasic):

        groups = for_views.checkboxes( Group.objects.filter(is_open=True) )

        def __init__(self, *args, **kw):
            YourCharacterFormBasic.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['groups'].initial = self.instance.groups.filter(is_open=True)
    
#        def get_initial(self):  #What is the pupous of this function?
#            initial = YourCharacterFormBasic.get_initial(self)   
            
        def save(self):
            self.is_valid()
            YourCharacterFormBasic.save(self)
            for_views.save_relations(   self.instance,
                                        Group.objects.filter(is_open=True),
                                        self.instance.groups.filter(is_open=True), 
                                        self.cleaned_data['groups'],
                                        Membership, 'character', 'group' )


    return YourCharacterFormClass(*args, **kw)


def index(request): 
    return render(request, 'plots/your_characters_index.html',
            { 'character_list': Character.objects.filter(user=request.user) }    )


def new(request):
    if request.method == 'POST':
        character_form = YourCharacterForm(request.POST)
        if character_form.is_valid():
            character = Character(user=request.user)
            character.save()
            character_form = YourCharacterForm(request.POST, instance=character )
            character_form.save()
            return HttpResponseRedirect(            
                reverse('your_characters:character', args=(character.id,))  )
    else:
        character_form = YourCharacterForm()

    return render(request, 'plots/your_character_edit.html',
               {'character_form': character_form} )
        

def character(request, id):
    character = get_object_or_404(Character, pk=id)
    if character.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        character_form = YourCharacterForm(request.POST, instance=character)
        if character_form.is_valid():
            character_form.save()
    else: 
        character_form = YourCharacterForm(instance=character)     

    return render(request, 'plots/your_character_edit.html',
           {'character_form': character_form}   )     




