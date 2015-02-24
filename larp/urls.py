from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'larp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^groups/', include('plots.groups.urls', namespace="groups")),

    url(r'^personal/your_characters/', 
            include('plots.your_characters.urls', namespace="your_characters")),

    url(r'^GM/', include('plots.GM.urls', namespace='GM'))
)
    

