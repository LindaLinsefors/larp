from django.conf.urls import patterns, include, url
#from django.contrib import admin

from pages import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'larp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^groups/', include('plots.groups.urls', namespace="groups")),

    url(r'^personal/your_characters/', 
            include('plots.your_characters.urls', namespace="your_characters")),

    url(r'^GM/', include('plots.GM.urls', namespace='GM')),

    url(r'^$', views.home, name='home'),
    url(r'^page/(?P<id>\d+)/$', views.page, name='page'),
    url(r'^page/(?P<id>\d+)/edit/$', views.edit_page, name='edit_page'),
    url(r'^page/(?P<id>\d+)/edit/delete$', views.delete_page, name='delete_page'),

    #url(r'^/', include('pages.urls', namespace='pages')),
    
)
    

