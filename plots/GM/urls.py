from django.conf.urls import patterns, url

from plots.GM import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)/$', views.plot_thread, name='plot_line') 
]
