from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlot, PersonalPlot, LarpPlotThread, GroupPlotPice, PersonalPlotPice, PlotPart, Membership, Larp

from plots.GM.forms import PlotPiceForm, PlotPartForms, GroupPlotForm, GroupPlotPiceForms, PersonalPlotForm, PersonalPlotPiceForms, GroupForm, MembersForm, CharacterForm, LarpForm, PlotThreadForm, PlotThreadForm_noLarps, LarpPlotThreadForm

#Dicts

class_dict = {  'larp':Larp,
                'group':Group,
                'character':Character,
                'plot_pice':PlotPice,
                'plot_thread': PlotThread,
                'group_plot':GroupPlot,
                'personal_plot':PersonalPlot,
                'larp_plot_thred':LarpPlotThread,   }

form_dict = {   'larp':LarpForm,
                'group':GroupForm,
                'character':CharacterForm,
                'plot_pice':PlotPiceForm,
                'plot_thread': PlotThreadForm,
                'group_plot':GroupPlotForm,
                'personal_plot':PersonalPlotForm,
                'larp_plot_thred':LarpPlotThreadForm,   }


#Edit/New

def edit_form(request, id, Class, ClassForm):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method != 'POST':
        return ClassForm(instance=class_instance)

    class_form = ClassForm(request.POST, instance=class_instance)
    if class_form.is_valid():
        class_form.save()
        return class_form

def new_form(request, Class, ClassForm):
    if request.method != 'POST':
        return ClassForm()

    class_form = ClassForm(request.POST)
    if class_form.is_valid():
        class_form.save()
        return class_form

#Topp

def edit_topp(request, class_name, id):
    class_form = edit_form( request, id,
                            class_dict[class_name],  
                            form_dict[class_name]   )

    return render(  request, 'plots/GM/basic_form.html',
                   {'class_form': class_form,
                    'class_instance': class_form.instance,    }   ) 

def new_topp(request, class_name):
    if request.method != 'POST':
        if class_name == 'plot_thread':
            class_name = 'plot thread'
        return render(  request, 'plots/GM/basic_form.html',
                       {'class_form': form_dict[class_name](),  
                        'class_name': class_name                }   ) 

    class_form = form_dict[class_name](request.POST)
    if class_form.is_valid():
        class_form.save()
        return HttpResponseRedirect(            
                reverse('GM:edit_topp', 
                        args=(  'class_name',
                                class_form.instance.id,)  ))  

def delete_topp(request, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    class_instance.delete()
    return HttpResponseRedirect( reverse('GM:index') )



def edit_under_larp(    request, larp_id, Class, id, ClassForm, 
                        template='plots/GM/basic_form.html'     ):

    class_form = edit_save_if_POST(request, Class, id, ClassForm)
    larp = get_object_or_404(Larp, pk=larp_id)   

    return render(  request, template,
                   {'class_form': class_form, 
                    'class_instance': class_instance,
                    'larp': larp,                      }   )   


def new(    request, larp_id, Class, ClassForm, 
            url='GM:stuff', template='plots/GM/basic_form.html'):

    if request.method == 'POST':
        class_form = ClassForm(request.POST)
        if class_form.is_valid():
            class_form.save()
            if Class == Larp:
                return HttpResponseRedirect(            
                    reverse(url, args=(class_form.instance.id,))  )

            larp = get_object_or_404(Larp, pk=larp_id)
            if Class == PlotThread:
                larp.plot_threads.add(class_form.instance)
            elif Class == Group:
                larp.groups.add(class_form.instance)
            elif Class == Character.add(class_form.instance):
                larp.characers.add(class_form.instance)

            larp.save()
            return HttpResponseRedirect(            
                reverse(url, args=(larp_id, class_form.instance.id))  )
    else:
        class_form = ClassForm()
        if Class == Larp:
            return render (  request, template,
                            {'class_form': class_form,}   ) 

        larp = get_object_or_404(Larp, pk=larp_id) 
        
    return render(  request, template,
                   {'class_form': class_form,
                    'larp': larp,               }   )  


def new_under_larp(    request, Class, ClassForm, 
            url='GM:stuff', template='plots/GM/basic_form.html'):

    if request.method == 'POST':
        class_form = ClassForm(request.POST)
        if class_form.is_valid():
            class_form.save()
            if Class == Larp:
                return HttpResponseRedirect(            
                    reverse(url, args=(class_form.instance.id,))  )

            larp = get_object_or_404(Larp, pk=larp_id)
            if Class == PlotThread:
                larp.plot_threads.add(class_form.instance)
            elif Class == Group:
                larp.groups.add(class_form.instance)
            elif Class == Character.add(class_form.instance):
                larp.characers.add(class_form.instance)

            larp.save()
            return HttpResponseRedirect(            
                reverse(url, args=(larp_id, class_form.instance.id))  )
    else:
        class_form = ClassForm()
        if Class == Larp:
            return render (  request, template,
                            {'class_form': class_form,}   ) 

        larp = get_object_or_404(Larp, pk=larp_id) 
        
    return render(  request, template,
                   {'class_form': class_form,
                    'larp': larp,               }   )  

#Index
def index(request):
    return render( request, 'plots/GM/index.html',
                {   'larps': Larp.objects.all(),
                    'groups': Group.objects.all(),
                    'characters': Character.objects.all(), }     )

#Larp

def larp(request, larp_id):
    return edit( request, Larp, larp_id, LarpForm )

def new_larp(request):
    return new( request, Larp, LarpForm, url='GM:larp' )

def delete_larp(request, larp_id):
    larp = get_object_or_404(Larp, pk=larp_id)
    larp.delete()
    return HttpResponseRedirect( reverse('GM:index') )

def larp_plots(request, id): 

    larp = get_object_or_404(Larp, pk=id)
    larp_plot_threads = larp.larpplotthread_set.all()
    groups = larp.groups.all()
    characters = larp.characters.all()

    return render(request, 'plots/GM/larp_plots.html',
              { 'larp': larp,
                'larp_plot_threads': larp_plot_threads,
                'groups': groups,
                'characters': characters,  
                # There is probably a better way to do this with filter
                'characters_without_group': 
                   [character for character in characters
                    if list( character.groups.filter(larp=larp) )==[] ],
                'plot_pices_without_character_or_group':
                   [plot_pice for plot_pice in larp.plotpice_set.all()
                    if (list( plot_pice.characters.filter(larp=larp) )==[]
                        and list( plot_pice.groups.filter(larp=larp) )==[] ) ],   
                'plot_pices_without_plot_thread':
                   [plot_pice for plot_pice in larp.plotpice_set.all()
                    if list( plot_pice.plot_threads.filter(larp=larp) )==[] ],       
                } )

#Plot Pice


def plot_pice(request, larp_id, parent_type, parent_id, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)
    larp = get_object_or_404(Larp, pk=larp_id)

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
                'parent_id': parent_id,                 
                'larp': larp,
                'heading': 'Edit',                        }   )


def plot_pice_no_parent(request, larp_id, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)
    larp = get_object_or_404(Larp, pk=larp_id)

    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST, instance=plot_pice)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect( reverse('GM:index') )

    plot_pice_form = PlotPiceForm(instance=plot_pice)
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:index',
                'larp': larp,
                'heading': 'Edit',                       }   )


def new_plot_pice(request, larp_id, parent_type, parent_id):  
    larp = get_object_or_404(Larp, pk=larp_id)
    
    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(request.POST)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect(            
                reverse('GM:'+parent_type, args=( parent_id,))  )
        print 'Form is not vaild'
    else:
        PlotPiceForm(initial={'larp':larp})
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'parent_url': 'GM:'+parent_type,
                'parent_id': parent_id,
                'larp': larp,
                'heading': 'New',                       }   )





#Plot Pice Inline

def save_formset(formset): #Is this needed?
    for form in formset:
        form.save()           


def plots(request, Class, id, ClassForm, InlineFormset, 
        template='plots/GM/plots.html'):

    class_instance = get_object_or_404(Class, pk=id)
    larp = class_instance.larp

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()

        inline_formset = InlineFormset(request.POST, instance=class_instance)
        if inline_formset.is_valid():
            save_formset(inline_formset)

    class_form = ClassForm(instance=class_instance)
    inline_formset = InlineFormset(instance=class_instance)

    return render(request, template,
           {'class_form': class_form,
            'class_instance': class_instance ,
            'plot_pice_forms': inline_formset,
            'larp':larp                         }   ) 


#Plot Thread

def larp_plot_thread(request, id): 
    return plots(   request, 
                    LarpPlotThread, id, LarpPlotThreadForm, PlotPartForms, 
                    template='plots/GM/plot_thread.html'        )


def new_larp_plot_thread(request, larp_id):
    larp = get_object_or_404(Larp, pk=larp_id)
    
    if request.method != 'POST':
        return render(  request, 'plots/GM/basic_form.html',
                       {'class_form': PlotThreadForm_noLarps(),
                        'class_name': 'plot thread',    
                        'larp':larp,                     }  )

    form = PlotThreadForm_noLarps(request.POST)
    if form.is_valid():
        form.save()

        larp_plot_thread = LarpPlotThread(  larp=larp, 
                                            plot_thread=form.instance   )
        larp_plot_thread.save()
        return HttpResponseRedirect( 
                    reverse(    'GM:larp_plot_thread',
                                args=(larp_plot_thread.id, )     ))



# Group Plot

def group_plot(request, larp_id, id): 
    return plots(   request, larp_id,   
                    Group, id, GroupPlotForm, GroupPlotPiceForms, 
                    template='plots/GM/plots.html'        )


# Personal Plot

def personal_plot(request, larp_id, id): 
    return plots(   request, larp_id, 
                    Character, id, PersonalPlotForm, PersonalPlotPiceForms, 
                    template='plots/GM/personal_plot.html'        )



# Group

def save_group(request, larp_id):
    # import pdb; pdb.set_trace()
    print request.POST
    return HttpResponse('saved')

def group_old(request, larp_id, id): 
    group = get_object_or_404(Group, pk=id)
    half = ( Character.objects.count()+1 )/2
    return render(request, 'plots/GM/group.html',
            {   'group': group, 
                'members': group.character_set.all(),
                'characters_fist_half': Character.objects.all()[:half],
                'characters_second_half': Character.objects.all()[half:],
            }   )

def new_group(request, larp_id): 
    return new( request, larp_id, Group, GroupForm,  url='GM:group' )

def group(request, larp_id, id):
    return edit( request, larp_id, Group, id, GroupForm )

def members_old(request, larp_id, id, back): 
    return edit( request, larp_id, Group, id, MembersForm, template='plots/GM/members.html'  )

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
    return edit( request, larp_id, Character, id, CharacterForm, 
                                template='plots/GM/character.html'   )


def new_character(request, larp_id): 
    return new(  request, larp_id, Character, CharacterForm, 
                                url='GM:character',
                                template='plots/GM/character.html'  )

#Delete


def delete(request, larp_id, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    class_instance.delete()
    return HttpResponseRedirect( reverse('GM:larp_plots', args=(larp_id) ) )
        

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


