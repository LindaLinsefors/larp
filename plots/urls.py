from django.conf.urls import patterns, url

from plots import views

urlpatterns = [

    url(r'^$', views.groups, name='groups'),

    #Groups with odd characters in their names may crach. This should be fixed.
    url(r'^(?P<url>\w+)/$', views.group, name='group') 
]

