from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def checkboxes(choice_list):
    return forms.MultipleChoiceField(
                    required = False,
                    widget  = forms.CheckboxSelectMultiple , 
                    choices = [ (choice, choice.name) 
                                for choice
                                in choice_list   ] )

def save_relations( instance,
                    choice_list, old_relations, new_relation_names,  
                    RelationClass, instance_type, choice_type ):

    for choice in choice_list:
        if (        (choice not in old_relations) 
                and (choice.name in new_relation_names) ):
            print choice.name
            RelationClass(**{choice_type:choice, instance_type:instance}).save()
        elif (      (choice in old_relations) 
                and (choice.name not in new_relation_names) ):
            RelationClass.objects.get(**{choice_type:choice, instance_type:instance}).delete()        
            

def edit(request, Class, id, ClassForm, template='plots/form_template'):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()
    else:
        class_form = ClassForm(instance=class_instance)     

    return render(  request, template,
                   {'class_form': class_form, 'id':id,
                    'class_instance': class_instance}   )   


def new(request, Class, ClassForm, url='GM:stuff', template='plots/form_template'):
    if request.method == 'POST':
        class_form = ClassForm(request.POST)
        if class_form.is_valid():
            class_form.save()
            return HttpResponseRedirect(            
                reverse(url, args=(class_form.instance.id,))  )
    else:
        class_form = ClassForm()

    return render(  request, template,
                   {'class_form': class_form}   )   
        
