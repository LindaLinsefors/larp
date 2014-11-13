from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from plots.models import Group


def groups(request):
    open_groups = Group.objects.filter(is_open=True)
    if open_groups.count() == 0: 
        open_groups = False
    closed_groups = Group.objects.filter(is_open=False) 
    if closed_groups.count() == 0: 
        closed_groups = False
    return render(request, 
                  'plots/groups.html', 
                  {'open_groups': open_groups, 
                   'closed_groups': closed_groups,} )



def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    return render(request, 'plots/group.html', {'group': group} )


