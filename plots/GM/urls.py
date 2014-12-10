from django.conf.urls import patterns, url

from plots.GM import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^plott_hread/(?P<id>[0-9]+)/$', views.plot_thread, name='plot_thread'),
    url(r'^plot_pice/(?P<id>[0-9]+)/$', views.plot_pice, name='plot_pice') 
]
