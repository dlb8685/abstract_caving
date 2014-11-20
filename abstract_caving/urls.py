from django.conf.urls import patterns, include, url
from django.contrib import admin
from game import views as game_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'abstract_caving.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', game_views.game_home, name="game_home"),
    url(r'^high-scores/$', game_views.game_high_scores, name="game_high_scores"),
    url(r'^save-high-score/$', game_views.game_save_high_score, name="game_save_high_score"),
)
