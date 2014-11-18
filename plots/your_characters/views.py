from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


from plots.models import Character




def index(request): 
    return render(request, 'plots/your_characters_index.html',
            { 'character_list':Character.objects.filter(user=request.user) }
    )

def character(request,id):
    character = get_object_or_404(Character, pk=id)
    if character.user == request.user:
        return HttpResponse('Here should be a character form')
    raise Http404
