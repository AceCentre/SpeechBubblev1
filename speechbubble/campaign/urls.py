from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^subscribe/$', 'speechbubble.campaign.views.subscribe', {}, name="campaign_subscribe"),
    url(r'^subscribe/outcome/$', 'speechbubble.campaign.views.subscribe_outcome', {}, name="campaign_subscribe"),
    url(r'^unsubscribe/$', 'speechbubble.campaign.views.unsubscribe', {}, name="campaign_unsubscribe"),
    url(r'^unsubscribe/outcome/$', 'speechbubble.campaign.views.unsubscribe_outcome', {}, name="campaign_unsubscribe"),
    url(r'^(?P<object_id>[\d]+)/$', 'speechbubble.campaign.views.view_online', {}, name="campaign_view_online"),
)

