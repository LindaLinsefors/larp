from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from plots.models import PlotThread, PlotPart, PlotPice, Group, Character, GroupPlot, PersonalPlot, LarpPlotThread, GroupPlotPice, PersonalPlotPice, PlotPart, Membership, Larp

from plots.GM.forms import PlotPiceForm, PlotPartForms, GroupPlotForm, GroupPlotPiceForms, PersonalPlotForm, PersonalPlotPiceForms, GroupForm, MembersForm, CharacterForm, LarpForm, PlotThreadForm, PlotThreadFormLarp, LarpPlotThreadForm, GroupFormLarp, CharacterFormLarp

#Dicts

class_dict = {  'larp':Larp,
                'group':Group,
                'character':Character,
                'plot_pice':PlotPice,
                'plot_thread': PlotThread,
                'group_plot':GroupPlot,
                'personal_plot':PersonalPlot,
                'larp_plot_thread':LarpPlotThread,   }

form_dict = {   'larp':LarpForm,
                'group':GroupForm,
                'character':CharacterForm,
                'plot_pice':PlotPiceForm,
                'plot_thread': PlotThreadForm,
                'group_plot':GroupPlotForm,
                'personal_plot':PersonalPlotForm,
                'larp_plot_thread':LarpPlotThreadForm,   }


#Edit/New

def edit_form(request, id, Class, ClassForm):
    class_instance = get_object_or_404(Class, pk=id)

    if request.method != 'POST':
        return ClassForm(instance=class_instance)

    class_form = ClassForm(request.POST, instance=class_instance)
    print request.POST
    if class_form.is_valid():
        class_form.save()
    else: print 'Form is not valid'
    return ClassForm(instance=Class.objects.get(pk=id) )


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
                        args=(  class_name,
                                class_form.instance.id,)  ))  

def delete_topp(request, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    class_instance.delete()
    return HttpResponseRedirect( reverse('GM:index') )


   



#Index
def index(request):
    return render( request, 'plots/GM/index.html',
                {   'larps': Larp.objects.all(),
                    'groups': Group.objects.all(),
                    'characters': Character.objects.all(),
                    'plot_threads': PlotThread.objects.all(), }     )

#Larp



def larp_plots(request, id): 
    larp = get_object_or_404(Larp, pk=id)
    return render(request, 'plots/GM/larp_plots.html',
              { 'larp': larp,
                # There is probably a better way to do this with filter
                'plot_pices_without_character_or_group':
                   [plot_pice for plot_pice in larp.plotpice_set.all()
                    if (list( plot_pice.personal_plots.filter(larp=larp) )==[]
                        and list( plot_pice.group_plots.filter(larp=larp) )==[] ) ],   
                'plot_pices_without_plot_thread':
                   [plot_pice for plot_pice in larp.plotpice_set.all()
                    if list( plot_pice.larp_plot_threads.filter(larp=larp) )==[] ],       
                } )

#Plot Pice

def edit_plot_pice(request, plot_pice, back):
    if request.method == 'POST':
        plot_pice_form = PlotPiceForm(plot_pice.larp)(
                                request.POST, instance=plot_pice, )

        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect( back )

    plot_pice_form = PlotPiceForm(plot_pice.larp)(instance=plot_pice)
    
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'back': back,
                'larp': plot_pice.larp,
                'heading': 'Edit',                       }   )


def plot_pice(request, parent_type, parent_id, id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)
    back = reverse('GM:plots', args=(parent_type, parent_id,)   )
    return edit_plot_pice(request, plot_pice, back)

def delete_plot_pice(request, parent_type, parent_id, id):  
    get_object_or_404(PlotPice, pk=id).delete()
    back = reverse('GM:plots', args=(parent_type, parent_id,)   )
    return HttpResponseRedirect( back )


def plot_pice_no_parent(request,  id):  
    plot_pice = get_object_or_404(PlotPice, pk=id)
    back = reverse('GM:larp_plots', args=(plot_pice.larp.id,)    )
    return edit_plot_pice(request, plot_pice, back)


def new_plot_pice(request, parent_type, parent_id):  
    parent = get_object_or_404(class_dict[parent_type], pk=parent_id)
    back = reverse('GM:larp_plots', args=(parent.larp.id,)    )

    if request.method == 'POST':

        plot_pice_form = PlotPiceForm(parent.larp)(request.POST)
        if plot_pice_form.is_valid():
            plot_pice_form.save()
            return HttpResponseRedirect( back )

    plot_pice_form = PlotPiceForm(parent.larp)()
    return render(request, 'plots/GM/plot_pice.html',
            {   'plot_pice_form': plot_pice_form,
                'back': back,
                'larp': parent.larp,
                'heading': 'New',                   } )


   





#Plots

def save_formset(formset): #Is this needed?
    for form in formset:
        form.save()    

formset_dict = {    'group_plot': GroupPlotPiceForms,
                    'personal_plot': PersonalPlotPiceForms,
                    'larp_plot_thread': PlotPartForms,            }

template_dict = { 'group_plot': 'plots/GM/plots.html',
                  'personal_plot': 'plots/GM/plots.html',
                  'larp_plot_thread': 'plots/GM/plot_thread.html',  }


def edit_plots(request, class_name, id):

    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    larp = class_instance.larp
    ClassForm = form_dict[class_name]
    InlineFormset = formset_dict[class_name]

    if request.method == 'POST':
        class_form = ClassForm(request.POST, instance=class_instance)
        if class_form.is_valid():
            class_form.save()

        inline_formset = InlineFormset(request.POST, instance=class_instance)
        if inline_formset.is_valid():
            save_formset(inline_formset)

    class_form = ClassForm(instance=class_instance)
    inline_formset = InlineFormset(instance=class_instance)

    return render(request, template_dict[class_name],
           {'class_form': class_form,
            'class_instance': class_instance,
            'plot_pice_forms': inline_formset,
            'larp':larp,                         }   ) 


def delete_plots(request, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    larp_id = class_instance.larp.id

    if (class_name == 'larp_plot_thread' and
            class_instance.plot_thread.larpplotthread_set.count() == 1):
        class_instance.plot_thread.delete()
    elif (class_name == 'personal_plot' and
            class_instance.character.personalplot_set.count() == 1):
        class_instance.character.delete()
    elif (class_name == 'group_plot' and
            class_instance.group.groupplot_set.count() == 1):
        class_instance.group.delete()
    else:
        class_instance.delete()
    return HttpResponseRedirect( 
                reverse(    'GM:larp_plots', args=(larp_id, )    ) )



larpform_dict =  {  'group': GroupFormLarp, 
                    'character': CharacterFormLarp,
                    'plot_thread': PlotThreadFormLarp, }

plotname_dict = {   'group': 'group_plot',
                    'character': 'personal_plot', 
                    'plot_thread': 'larp_plot_thread' }


def new_plots(request, larp_id, class_name):
    larp = get_object_or_404(Larp, pk=larp_id)
    class_form = larpform_dict[class_name](larp)
    
    if request.method != 'POST':
        if class_name == 'plot_thread':
            class_name = 'plot thread'
        return render(  request, 'plots/GM/basic_form.html',
               {'class_form': class_form,
                'class_name': class_name,    
                'larp':larp,                     }  )

    form = class_form(request.POST)
    if form.is_valid():
        form.save()
        
        plot_class_name = plotname_dict[class_name]
        plot_instance = class_dict[plot_class_name](
                             **{'larp':larp, 
                                 class_name: form.instance} )
        plot_instance.save()

        return HttpResponseRedirect( 
                reverse(    'GM:plots',
                            args=(  plot_class_name,
                                    plot_instance.id ) ))


def edit_plot_resiver(request, larp_id, class_name, id):
    larp = get_object_or_404(Larp, pk=larp_id)
    class_form = edit_form( request, id,
                            class_dict[class_name],  
                            larpform_dict[class_name](larp)   )

    return render(  request, 'plots/GM/basic_form.html',
                   {'class_form': class_form,
                    'class_instance': class_form.instance,   
                    'larp': larp                            }   ) 

def delete_plot_resiver(request, larp_id, class_name, id):
    class_instance = get_object_or_404(class_dict[class_name], pk=id)
    larp = get_object_or_404(Larp, pk=larp_id)

    if class_name == 'character':
        if class_instance.personalplot_set.count() == 1:
            class_instance.delete()
        else:
            get_object_or_404(  GroupPlot, 
                                larp=larp, 
                                group=class_instance ).delete()

    elif class_name == 'group':
        if class_instance.groupplot_set.count() == 1:
            class_instance.delete()
        else:
            get_object_or_404(  PersonalPlot, 
                                larp=larp, 
                                character=class_instance ).delete()

    return HttpResponseRedirect( 
                reverse(    'GM:larp_plots', args=(larp_id, )    ) )
                    








# Memberst (verry old)




def edit(   request, larp_id, Class, id, ClassForm, 
            template='plots/GM/basic_form.html'     ):

    class_form = edit_save_if_POST(request, Class, id, ClassForm)
    larp = get_object_or_404(Larp, pk=larp_id)   

    return render(  request, template,
                   {'class_form': class_form, 
                    'class_instance': class_instance,
                    'larp': larp,                      }   )

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




