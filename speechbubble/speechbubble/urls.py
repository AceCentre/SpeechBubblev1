from django.conf.urls import include, patterns, url
from django.views.generic import list
from django.conf import settings
from django.conf.urls.static import static

from filebrowser.sites import site

from speechbubble.views import HomeView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from moderation import helpers
helpers.auto_discover()

urlpatterns = patterns('speechbubble.views',
    (r'^$', HomeView.as_view()),
    (r'^search/$', 'search'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('django.views.generic.simple',
    # Example:
    # (r'^speechbubble/', include('speechbubble.foo.urls')),

    # (r'^$', 'direct_to_template', {'template': 'index.html'}),

    (r'^', include('voca.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^newsletter/', include('campaign.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', admin.site.urls),
    # url(r'^', include('cms.urls')),
)
