from django.conf.urls import patterns, include, url
from django.contrib import admin
from game import views as game_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'abstract_caving.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', game_views.game_home, name="game_home"),
)
