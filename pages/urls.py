from django.conf.urls import patterns, url

from pages import views

urlpatterns = [

    url(r'^$/', views.home, name='home'),
    url(r'^page/(?P<id>\d+)/$', views.page, name='page'),
    url(r'^page/(?P<id>\d+)/edit/$', views.edit_page, name='edit_page'),

]
