from django.conf.urls import patterns, url

from plots.GM import views

urlpatterns = [

    # Index
    url(r'^$', views.index, name='index'),

    # Larp
    url(r'^$(?P<larp_id>[0-9]+)/$', views.index, name='larp'),
    url(r'^$(?P<larp_id>[0-9]+)/plots/$', views.index, name='larp_plots'),

    # Plot categories
    url(r'^(?P<larp_id>[0-9]+)/plot_thread/(?P<id>[0-9]+)/$', 
            views.plot_thread, name='plot_thread'),

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
    url(r'^(?P<larp_id>[0-9]+)/plot_thread/new/$', 
            views.new_plot_thread, name='new_plot_thread'),

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
