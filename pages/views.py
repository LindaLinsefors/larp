from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from pages.models import Page

import floppyforms.__future__  as forms


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [  'title',
                    'top_page',
                    'sort_under',
                    'html',         ]


def nav_list():
    return Page.objects.filter(top_page=1).exclude(title='home')


def home(request):
    try:
        home = Page.objects.get(title='home')
    except(Page.DoesNotExist):
        home = Page(title='home')
        home.save()
    except(Page.MultipleObjectsReturned):
        return render(  request, 'pages/page.html',
               {'nav_list': nav_list(),
                'my_error_message': '''
You have more than one page titled "home".
Ahrgh, the confusion! I can't stand it. Fix this problem now!!
'''}   ) 

    return render( request, 'pages/page.html', 
               {'nav_list': nav_list(),
                'page':home} )
    

def page(request, id):
    page = get_object_or_404(Page,pk=id)

    return render( request, 'pages/page.html', 
               {'nav_list': nav_list(),
                'page':page,            } )


def edit_page(request, id):
    page = get_object_or_404(Page, pk=id)

    if request.method != 'POST':
        return render( request, 'pages/edit_page.html',
                       {'nav_list': nav_list(),
                        'page_form': PageForm(instance=page),
                        'id': id,   
                        'delete':'delete',                       })

    page_form = PageForm(request.POST, instance=page)
    if not page_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen.',
                        'nav_list': nav_list(),
                        'page_form': page_form,
                        'id': id,
                        'delete':'delete',                       })

    page_form.save()
    return HttpResponseRedirect( reverse('page', args=(id,)) ) 


def delete_page(request, id):
    get_object_or_404(Page, pk=id).delete()
    return HttpResponseRedirect( reverse('home') ) 

def new_top_page(request):
    if request.method != 'POST':
        return render( request, 'pages/edit_page.html',
                       {'nav_list': nav_list(),
                        'page_form': PageForm(initial={'top_page':True}), })

    page_form = PageForm(request.POST)
    if not page_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen.',
                        'nav_list': nav_list(),
                        'page_form': page_form,      })

    page_form.save()
    return HttpResponseRedirect( reverse('page', args=(page_form.instance.id,)) ) 
    

def new_subpage(request, id):
    if request.method != 'POST':
        page = get_object_or_404(Page, pk=id)
        return render( request, 'pages/edit_page.html',
                       {'nav_list': nav_list(),
                        'page_form': PageForm({ 'top_page': False,
                                                'sort_under': page,  }),
                        'id': id                    })

    page_form = PageForm(request.POST)
    if not page_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen.',
                        'nav_list': nav_list(),
                        'page_form': page_form,
                        'id': id                    })

    page_form.save()
    return HttpResponseRedirect( reverse('page', args=(page_form.instance.id,)) ) 

