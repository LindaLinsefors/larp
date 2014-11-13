from django.conf.urls import patterns, url

from plots import views

urlpatterns = [
    # ex: /groups/
    url(r'^$', views.groups, name='groups'),
    # ex: /group/5/
    url(r'^(?P<group_id>[0-9]+)/$', views.group, name='group') 
]

