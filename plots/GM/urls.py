from django.conf.urls import patterns, url

from plots.GM import views

urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^plot_thread/(?P<id>[0-9]+)/$', views.plot_thread, name='plot_thread'),
    url(r'^group_plot/(?P<id>[0-9]+)/$', views.group_plot, name='group_plot'),
    url(r'^personal_plot/(?P<id>[0-9]+)/$', views.personal_plot, name='personal_plot'),

    url(r'^(?P<parent_type>\w+)/(?P<parent_id>[0-9]+)/plot_pice/(?P<id>[0-9]+)/$', 
            views.plot_pice, name='plot_pice') 
]
