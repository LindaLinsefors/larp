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

    url(r'^larp_plots/(?P<larp_id>\d+)/plot_thread/new/$', views.new_larp_plot_thread, name='new_larp_plot_thread' ),

    url(r'^larp_plots/(?P<larp_id>\d+)/(?P<class_name>\w+)/new/$', views.new_plot_resiver, name='new_plot_resiver' ),
    url(r'^larp_plots/(?P<larp_id>\d+)/(?P<class_name>\w+)/(?P<id>\d+)/$', views.edit_plot_resiver, name='plot_resiver' ),
    url(r'^larp_plots/(?P<larp_id>\d+)/(?P<class_name>\w+)/(?P<id>\d+)/$', views.delete_plot_resiver, name='delete_plot_resiver' ),



    # LarpPlotThread
    url(r'^larp/(?P<larp_id>\d+)/new_plot_thread/new/$', 
            views.new_larp_plot_thread, name='new_larp_plot_thread'),


    # Plot categories

    url(r'^(?P<larp_id>[0-9]+)/group_plot/(?P<id>[0-9]+)/$', 
            views.group_plot, name='group_plot'),

    url(r'^(?P<larp_id>[0-9]+)/personal_plot/(?P<id>[0-9]+)/$', 
            views.personal_plot, name='personal_plot'),
    
    # Plot pice    
    url(r'^(?P<larp_id>[0-9]+)/(?P<parent_type>\w+)/(?P<parent_id>[0-9]+)/plot_pice/(?P<id>[0-9]+)/$', 
            views.plot_pice, name='plot_pice'),

    url(r'^(?P<larp_id>[0-9]+)/(?P<parent_type>\w+)/(?P<parent_id>[0-9]+)/plot_pice/new/$', 
            views.new_plot_pice, name='new_plot_pice'),

    url(r'^(?P<larp_id>[0-9]+)/plot_pice/(?P<id>[0-9]+)/$', 
            views.plot_pice_no_parent, name='plot_pice'),

    # Edit groups and characters
    url(r'^(?P<larp_id>[0-9]+)/group/(?P<id>[0-9]+)/$', 
            views.group, name='group'),

    url(r'^(?P<larp_id>[0-9]+)/character/(?P<id>[0-9]+)/$', 
            views.character, name='character'),

    # New

    url(r'^(?P<larp_id>[0-9]+)/group/new/$', 
            views.new_group, name='new_group'),      

    url(r'^(?P<larp_id>[0-9]+)/character/new/$', 
            views.new_character, name='new_character'),

    # Delete
    url(r'^(?P<larp_id>[0-9]+)/(?P<class_name>\w+)/(?P<id>[0-9]+)/delete$', 
            views.delete, name='delete'),

    url(r'^(?P<larp_id>[0-9]+)/(?P<parent_type>\w+)/(?P<parent_id>[0-9]+)/plot_pice/(?P<id>[0-9]+)/delete$', 
            views.delete_plot_pice, name='delete'),

    # Members
    url(r'^(?P<larp_id>[0-9]+)/group_members/(?P<id>[0-9]+)$', 
            views.members_from_index, name='members'),

    url(r'^(?P<larp_id>[0-9]+)/(?P<parent_type>\w+)/(?P<id>[0-9]+)/members$', 
            views.members_from_parent, name='members'),

    # Save Group
    url(r'^(?P<larp_id>[0-9]+)/save_group/$', views.save_group, name='save_group')
]
