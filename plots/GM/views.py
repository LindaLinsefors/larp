from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlotPice, PersonalPlotPice, PlotPart, Membership
from plots.GM.forms import PlotPiceForm, PlotPartForms GroupPlotForm, GroupPlotPiceForms, PersonalPlotForm, PersonalPlotPiceForms, GroupForm, MembersForm, CharacterForm, LarpForm


#General

def edit(request, id, ClassForm, template='plots/form_template.html'):
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


def new(request, ClassForm, url='GM:stuff', template='plots/form_template.html'):
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


#Index
def index(request)
    return render( request, 'plots/GM/index.html',
                { 'laprs': Larp.objects.all() }     )

#Larp

def larp(request, larp_id):
    return edit( request, larp_id, LarpForm )

def new_larp(request):
    return new( request, LarpForm, url='GM:larp' )

def lapr_plots(request, larp_id): 

    larp = get_object_or_404(Larp, larp_id)
    plot_threads = larp.plot_threads
    groups = larp.groups
    characters = larp.characters

    return render(request, 'plots/GM/larp_plots.html',
              { 'larp': larp
                'plot_threads': plot_threads,
                'groups': groups,
                'characters': characters,  
                # There is probably a better way to do this with filter
                'characters_without_group': 
                   [character for character in characters
                    if list( character.groups.filter(lapr=larp) )==[] ],
                'plot_pices_without_character_or_group':
                   [plot_pice for plot_pice in larp.plot_pices
                    if (list( plot_pice.characters.filter(lapr=larp) )==[]
                        and list( plot_pice.groups.filter(lapr=larp) )==[] ) ],   
                'plot_pices_without_plot_thread':
                   [plot_pice for plot_pice in larp.plot.pices
                    if list( plot_pice.plot_threads.filter(lapr=larp) )==[] ],       
                } )

#Plot Pice


def plot_pice(request, larp_id, parent_type, parent_id, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)

    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect(            
                reverse('GM:'+parent_type, args=( parent_id,))  )

    plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id                  }   )


def plot_pice_no_parent(request, larp_id, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)

    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect( reverse('GM:index') )

    plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:index'         }   )


def new_plot_pice(request, larp_id, parent_type, parent_id):  
    
    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect(            
                reverse('GM:'+parent_type, args=( parent_id,))  )
    else:
        plot_pice_form = PlotPiceForm()
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id                  }   )





#Plot Pice Inline

def save_formset(formset): #Is this needed?
    for form in formset:
        form.save()           


def plots(request, Class, id, ClassForm, InlineFormset, template='plots/GM/plots.html'):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()

        inline_formset = InlineFormset(request.POST, instance=class_instance)
        #import pdb; pdb.set_trace()
        if inline_formset.is_valid():
            save_formset(inline_formset)

    class_form = ClassForm(instance=class_instance)
    inline_formset = InlineFormset(instance=class_instance)

    return render(request, template,
           {'class_form': class_form,
            'class_instance': class_instance ,
            'plot_pice_forms': inline_formset}   )   


#Plot Thread

def plot_thread(request, larp_id, id): 
    return plots(   request, PlotThread, id, PlotThreadForm, PlotPartForms, 
                    template='plots/GM/plot_thread.html'        )

def new_plot_thread(request, larp_id):
    pass 



# Group Plot

def group_plot(request, larp_id, id): 
    return plots(   request, Group, id, GroupPlotForm, GroupPlotPiceForms, 
                    template='plots/GM/plots.html'        )


# Personal Plot

def personal_plot(request, larp_id, id): 
    return plots(   request, Character, id, PersonalPlotForm, PersonalPlotPiceForms, 
                    template='plots/GM/personal_plot.html'        )


def new_personal_plot(request, larp_id): 
    pass


# Group

def save_group(request, larp_id):
    # import pdb; pdb.set_trace()
    print request.POST
    return HttpResponse('saved')

def group(request, larp_id, id): 
    group = get_object_or_404(Group, pk=id)
    half = ( Character.objects.count()+1 )/2
    return render(request, 'plots/GM/group.html',
            {   'group': group, 
                'members': group.character_set.all(),
                'characters_fist_half': Character.objects.all()[:half],
                'characters_second_half': Character.objects.all()[half:],
            }   )

def new_group(request, larp_id): 
    return new( request, GroupForm,  url='GM:group' )

def members_old(request, larp_id, id, back): # This one works
    return edit( request, id, MembersForm  )

def members(request, larp_id, id, back):
    group = get_object_or_404(Group, pk=id)

    if request.method == 'POST':
        members_form = MembersForm(request.POST, instance=group)
        if members_form.is_valid():
            members_form.save()
            return HttpResponseRedirect( back )

    members_form = MembersForm(instance=group)
    
    return render(request, 'plots/GM/members.html',
            {   'members_form': members_form,
                'group': group,                 }   )

def members_from_index(request, larp_id, id):
    return members(request, id, reverse('GM:index') )

def members_from_parent(request, larp_id, id, parent_type ):
    return members( request, id, 
                    reverse('GM:'+parent_type, args=(id,)) )

# Character

def character(request, larp_id, id): 
    return edit( request, id, CharacterForm, 
                                template='plots/GM/character.html'   )


def new_character(request, larp_id): 
    return new(  request, CharacterForm, 
                                url='GM:character',
                                template='plots/GM/character.html'  )

#Delete

class_dict = {  'group': Group,
                'character': Character,
                'plot_thread': PlotThread,
                'plot_pice': PlotPice   }

def delete(request, larp_id, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    if request.method == 'POST':
        class_instance.delete()
        return HttpResponseRedirect( reverse('GM:index') )
    
    if class_name == 'plot_pice': 
        name = 'Plot Pice'
    else: 
        name = class_instance.name
        
    return render(  request, 'plots/GM/delete.html',
                   {'name': name,
                    'back': reverse('GM:'+class_name, args=(id,)) })
        

def delete_plot_pice(request, larp_id, parent_type, parent_id, id):
    plot_pice = get_object_or_404(PlotPice, pk=id)
    if request.method == 'POST':
        plot_pice.delete()
        return HttpResponseRedirect( 
                reverse('GM:'+parent_type, args=(parent_id,) ))

    return render( request, 'plots/GM/delete.html',
                   {'name': 'Plot Pice',
                    'back': reverse('GM:'+class_name, 
                                    args=(parent_type, parent_id, id)) 
                    })


