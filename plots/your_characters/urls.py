from django.conf.urls import patterns, url

from plots.your_characters import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)/$', views.character, name='character') 
]
