from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from plots.models import Group


def groups(request):
    open_groups = Group.objects.filter(is_open=True),
    closed_groups = Group.objects.filter(is_open=True) 
    return render(request, 
                  'plots/groups.html', 
                  {'open_groups': open_groups, 
                   'closed_groups': closed_groups,} )



#def group(request, group_id):
#    group = get_object_or_404(Group, pk=group_id)
#    return render(request, 'plots/grupe.html', {'group': groups} )


def group(pryl):
    return HttpResponse(repr(pryl))
