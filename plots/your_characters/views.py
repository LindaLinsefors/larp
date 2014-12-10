from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django import forms

from plots.models import Character, Group, Membership


class YourCharacterFormBasic(forms.ModelForm):
    class Meta:
        model = Character
        fields = [  'name', 
                    'character_concept', 
                    'presentation', 
                    'character_description'   ]

def checkboxes(choice_list):
    return forms.MultipleChoiceField(
                    required = False,
                    widget  = forms.CheckboxSelectMultiple , 
                    choices = [ (choice, choice.name) 
                                for choice
                                in choice_list   ] )


def YourCharacterForm(*args, **kw):
    class YourCharacterFormClass(YourCharacterFormBasic):
    #    groups = forms.MultipleChoiceField(
     #               required = False,
      #              widget  = forms.CheckboxSelectMultiple , 
       #             choices = [ (group, group.name) 
        #                        for group
         #                       in Group.objects.filter(is_open=True)   ] )
        groups = checkboxes( Group.objects.filter(is_open=True) )

        def __init__(self, *args, **kw):
            YourCharacterFormBasic.__init__(self, *args, **kw)
            if kw.has_key('instance'):
                self.fields['groups'].initial = self.instance.groups.filter(is_open=True)
    
        def get_initial(self):  #What is the pupous of this function?
            initial = YourCharacterFormBasic.get_initial(self) 

        def save(self):
            self.is_valid()
            YourCharacterFormBasic.save(self)
            old_member_groups = self.instance.groups.filter(is_open=True)
            new_member_groups = self.cleaned_data['groups']
            for group in Group.objects.filter(is_open=True):
                if (group not in old_member_groups) and (group.name in new_member_groups):
                    Membership(group=group, character=self.instance).save()
                elif (group in old_member_groups) and (group.name not in new_member_groups):
                    Membership.objects.get(group=group, character=self.instance).delete()   
            
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
            print character.id
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




