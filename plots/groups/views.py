from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from plots.models import Group


def groups(request):
    open_groups = Group.objects.filter(is_open=True).exclude(secret=True)
    if open_groups.count() == 0: 
        open_groups = False
    closed_groups = Group.objects.filter(is_open=False).exclude(secret=True)
    if closed_groups.count() == 0: 
        closed_groups = False
    return render(request, 
                  'plots/groups.html', 
                  {'open_groups': open_groups, 
                   'closed_groups': closed_groups} )



def group(request, url):
    name = ''
    for char in url:
        if char == '_': name += ' '
        else:           name += char

    group = get_object_or_404(Group, name=name)
    if group.secret == True: raise Http404
    return render(request, 'plots/group.html', {'group': group} )


