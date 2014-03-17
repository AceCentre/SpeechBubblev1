from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('speechbubble.views',
                       (r'^$', 'home'),
                       (r'^search/$', 'search'),
)

urlpatterns += patterns('django.views.generic.simple',
                        # Example:
                        # (r'^speechbubble/', include('speechbubble.foo.urls')),

                        # (r'^$', 'direct_to_template', {'template': 'index.html'}),

                        (r'^', include('speechbubble.voca.urls')),

                        (r'^admin/filebrowser/', include(site.urls)),
                        (r'^tinymce/', include('tinymce.urls')),
                        #    (r'^news/', include('django_simple_news.urls')),
                        url(r'^pages/', include('pages.urls')),
                        (r'^newsletter/', include('speechbubble.campaign.urls')),

                        # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
                        # to INSTALLED_APPS to enable admin documentation:
                        # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                        # Uncomment the next line to enable the admin:
                        (r'^admin/', admin.site.urls),
                        # url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$',
                            'django.views.static.serve',
                            {'document_root': settings.MEDIA_ROOT})
                    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)