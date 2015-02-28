from django.conf.urls import patterns, url

from plots.GM import views

urlpatterns = [

    # Index
    url(r'^$', views.index, name='index'),

    # Larp/Group/Character
    url(r'^larp_plots/(?P<id>\d+)/$', views.larp_plots, name='larp_plots'),

    url(r'^(?P<class_name>\w+)/(?P<id>\d+)/$', views.edit_topp, name='edit_topp'),
    url(r'^(?P<class_name>\w+)/(?P<id>\d+)/delete/$', views.delete_topp, name='delete_topp'),
    url(r'^(?P<class_name>\w+)/new/$', views.new_topp, name='new_topp'),


    # Plots
    url(r'^larp_plots/(?P<class_name>\w+)/(?P<id>\d+)/$', views.edit_plots, name='plots' ),
    url(r'^larp_plots/(?P<class_name>\w+)/(?P<id>\d+)/delete/$', views.delete_plots, name='delete_plots' ),
    url(r'^larp_plots/(?P<larp_id>\d+)/(?P<class_name>\w+)/new/$', views.new_plot, name='new_plot' ),
    url(r'^larp_plots/(?P<larp_id>\d+)/(?P<class_name>\w+)/(?P<id>\d+)/$', views.edit_plot_resiver, name='plot_resiver' ),
    url(r'^larp_plots/(?P<larp_id>\d+)/(?P<class_name>\w+)/(?P<id>\d+)/delete$', views.delete_plot_resiver, name='delete_plot_resiver' ),


    
    # Plot pice    
    url(r'^(?P<larp_id>[0-9]+)/(?P<parent_type>\w+)/(?P<parent_id>[0-9]+)/plot_pice/(?P<id>[0-9]+)/$', 
            views.plot_pice, name='plot_pice'),

    url(r'^(?P<larp_id>[0-9]+)/(?P<parent_type>\w+)/(?P<parent_id>[0-9]+)/plot_pice/new/$', 
            views.new_plot_pice, name='new_plot_pice'),

    url(r'^(?P<larp_id>[0-9]+)/plot_pice/(?P<id>[0-9]+)/$', 
            views.plot_pice_no_parent, name='plot_pice'),

    ]
