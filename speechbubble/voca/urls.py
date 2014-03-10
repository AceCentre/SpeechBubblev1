from django.conf.urls.defaults import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from voca.models import Device, Software, Vocabulary, SymbolLibrary, Supplier
from voca.views import DeviceSearch, DeviceList, DeviceDetail
from voca import views

device_info = {
    'queryset': Device.objects.all(),
    'template_object_name': 'device',
    'extra_context': {'device_list': Device.objects.order_by('name')},
}

software_info = {
    'queryset': Software.objects.all(),
    'template_object_name': 'software',
    'extra_context': {'software_list': Software.objects.order_by('name')},
}

vocabulary_info = {
    'queryset': Vocabulary.objects.all(),
    'template_object_name': 'vocabulary',
    'extra_context': {'vocabulary_list': Vocabulary.objects.order_by('name')},
}

symbol_library_info = {
    'queryset': SymbolLibrary.objects.all(),
    'template_object_name': 'symbol_library',
}

supplier_info = {
    'queryset': Supplier.objects.all(),
    'template_object_name': 'supplier',
}

urlpatterns = patterns('django.views.generic.simple',
#    (r'^devices/$', ListView.as_view(), device_info),
#    (r'^devices/$', views.device_search_form),
    (r'^devices/$', DeviceList.as_view()),
    (r'^devices/$', views.device_search, {"letter": ""}),
    (r'^devices/(?P<letter>\w)/$', views.device_search),
    (r'^devices/search/$', DeviceSearch.as_view()),
    (r'^devices/compare/$', views.device_compare), 
    (r'^device/(?P<object_id>\d+)/$', DeviceDetail.as_view()),
    (r'^device/(?P<slug>[\w-]+)/$', DeviceDetail.as_view()),

#    (r'^software/$', ListView.as_view(), software_info),
    (r'^software/$', views.software_search, {"letter": ""}),
    (r'^software/(?P<letter>\w)/$', views.software_search),
    (r'^software/search/$', views.software_search_form),
    (r'^software/compare/$', views.software_compare),
    (r'^software/(?P<object_id>\d+)/$', DetailView.as_view(), software_info),
    (r'^software/(?P<slug>[\w-]+)/$', DetailView.as_view(), software_info),

#    (r'^vocabularies/$', ListView.as_view(), vocabulary_info),
    (r'^vocabularies/$', views.vocabulary_search, {"letter": ""}),
    (r'^vocabularies/(?P<letter>\w)/$', views.vocabulary_search),
    (r'^vocabularies/search/$', views.vocabulary_search_form),
    (r'^vocabularies/compare/$', views.vocabulary_compare),
    (r'^vocabulary/(?P<object_id>\d+)/$', DetailView.as_view(), vocabulary_info),
    (r'^vocabulary/(?P<slug>[\w-]+)/$', DetailView.as_view(), vocabulary_info),

    (r'^symbollibraries/$', ListView.as_view(), symbol_library_info),
    (r'^symbollibrary/(?P<object_id>\d+)/$', DetailView.as_view(), symbol_library_info),

    (r'^suppliers/$', ListView.as_view(), supplier_info),
    (r'^supplier/(?P<object_id>\d+)/$', DetailView.as_view(), supplier_info),
    (r'^supplier/(?P<slug>[\w-]+)/$', DetailView.as_view(), supplier_info),
    url(r'^voca/external_link_list.js$', views.link_list),
)

