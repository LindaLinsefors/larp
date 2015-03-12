from django.shortcuts import get_object_or_404, render
from pages.models import Page

def nav_list():
    Page.objects.filter(in_nav=1).exclude(name='home')


def home(request):
    try:
        home = Page.objects.get(name='home')
    except(Page.DoesNotExist):
        home = Page(name='home')
        home.save()
    except(Page.MultipleObjectsReturned):
        return render(  request, 'pages/page.html',
               {'nav_list': nav_list(),
                'error message': '''
You have more than one page named "home".
Ahrgh, the confusion! I can't stand it. Fix this problem now!!
'''}   ) 

    return render( request, 'pages/page.html', 
               {'nav_list': nav_list(),
                'page':home} )
    

def page(request, id):
    page = get_object_or_404(Page,pk=id)

    return render( request, 'pages/page.html', {'page':page} )
