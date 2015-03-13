from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from pages.models import Page, Home

import floppyforms.__future__  as forms


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [  'title',
                    'top_page',
                    'sort_under',
                    'html',         ]

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = [  'title',
                    'html',  ]


def nav_list():
    return Page.objects.filter(top_page=1).exclude(title='home')

def get_home():
    try:
        home = Home.objects.get()
    except(Home.DoesNotExist):
        home = Home()
        home.save()
    return home

def top_logo():
    return get_home().title


initial_html = u'''<p>
Fist paragraph... 
</p>

<p>
Second paragraph...
</p>

<h2> Sub-title </h2>
<p>
Evem more text...
</p>'''
            



def home(request):
    return render( request, 'pages/page.html', 
               {'nav_list': nav_list(),'top_logo': top_logo(),
                'page': get_home(),
                'edit': True    } )

def edit_home(request):

    if request.method != 'POST':
        return render( request, 'pages/edit_page.html',
                               {'nav_list': nav_list(),'top_logo': top_logo(),
                                'page_form': HomeForm (instance=get_home() ),   })

    home_form = HomeForm(request.POST, instance=get_home() )
    if not home_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen!',
                        'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': home_form,      })

    home_form.save()
    return HttpResponseRedirect( reverse('home') ) 
    

def page(request, id):
    page = get_object_or_404(Page,pk=id)
    return render( request, 'pages/page.html', 
               {'nav_list': nav_list(),'top_logo': top_logo(),
                'page': page,            
                'edit': True,           } )


def edit_page(request, id):
    page = get_object_or_404(Page, pk=id)

    if request.method != 'POST':
        return render( request, 'pages/edit_page.html',
                       {'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': PageForm(instance=page),
                        'id': id,   
                        'delete': True,                       })

    page_form = PageForm(request.POST, instance=page)
    if not page_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen.',
                        'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': page_form,
                        'id': id,
                        'delete': True,                       })

    page_form.save()
    return HttpResponseRedirect( reverse('page', args=(id,)) ) 


def delete_page(request, id):
    get_object_or_404(Page, pk=id).delete()
    return HttpResponseRedirect( reverse('home') ) 

def new_top_page(request):
    if request.method != 'POST':
        return render( request, 'pages/edit_page.html',
                       {'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': PageForm({ 'top_page':True,
                                                'html': initial_html }), })

    page_form = PageForm(request.POST)
    if not page_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen.',
                        'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': page_form,      })

    page_form.save()
    return HttpResponseRedirect( reverse('page', args=(page_form.instance.id,)) ) 
    

def new_subpage(request, id):
    if request.method != 'POST':
        page = get_object_or_404(Page, pk=id)
        return render( request, 'pages/edit_page.html',
                       {'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': PageForm({ 'top_page': False,
                                                'sort_under': page,
                                                'html': initial_html  }),
                        'id': id                    })

    page_form = PageForm(request.POST)
    if not page_form.is_valid():
        return render( request, 'pages/edit_page.html',
                       {'my_error_message': 'What?! Form is not valid? This should not happen.',
                        'nav_list': nav_list(),'top_logo': top_logo(),
                        'page_form': page_form,
                        'id': id                    })

    page_form.save()
    return HttpResponseRedirect( reverse('page', args=(page_form.instance.id,)) ) 

