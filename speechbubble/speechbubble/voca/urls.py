from django.conf.urls import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from speechbubble.voca.models import Device, Software, Vocabulary, SymbolLibrary, Supplier
from speechbubble.voca import views


class DeviceInfo(DetailView):
    queryset = Device.objects.all()
    context_object_name = 'device'

    def get_context_data(self, *args, **kwargs):
        ctxt = super(DeviceInfo, self).get_context_data(*args, **kwargs)
        ctxt['device_list'] = Device.objects.order_by('name')
        return ctxt


class SoftwareInfo(DetailView):
    queryset = Software.objects.all()
    context_object_name = 'software'

    def get_context_data(self, *args, **kwargs):
        ctxt = super(SoftwareInfo, self).get_context_data(*args, **kwargs)
        ctxt['software_list'] = Software.objects.order_by('name')
        return ctxt


class VocabularyInfo(DetailView):
    queryset = Vocabulary.objects.all()
    context_object_name = 'vocabulary'

    def get_extra_context(self, *args, **kwargs):
        ctxt = super(VocabularyInfo, self).get_context_data(*args, **kwargs)
        ctxt['vocabulary_list'] = Vocabulary.objects.order_by('name')
        return ctxt


class SymbolLibraryList(ListView):
    queryset = SymbolLibrary.objects.all()
    context_object_name = 'symbol_library'


class SymbolLibraryInfo(DetailView):
    queryset = SymbolLibrary.objects.all()
    context_object_name = 'symbol_library'


class SupplierList(ListView):
    queryset = Supplier.objects.all()
    context_object_name = 'supplier'

    def get_context_data(self, *args, **kwargs):
        ctxt = super(SupplierList, self).get_context_data(*args, **kwargs)
        ctxt['supplier_list'] = Supplier.objects.order_by('name')
        return ctxt


class SupplierInfo(DetailView):
    queryset = Supplier.objects.all()
    context_object_name = 'supplier'


urlpatterns = patterns('django.views.generic.simple',
#    (r'^devices/$', list_detail.object_list, device_info),
#    (r'^devices/$', views.device_search_form),
    (r'^devices/$', views.device_search, {"letter": ""}),
    (r'^devices/(?P<letter>\w)/$', views.device_search),
    (r'^devices/search/$', views.device_search_form),
    (r'^devices/compare/$', views.device_compare), 
    (r'^device/(?P<object_id>\d+)/$', DeviceInfo.as_view()),
    (r'^device/(?P<slug>[\w-]+)/$', DeviceInfo.as_view()),

#    (r'^software/$', list_detail.object_list, software_info),
    (r'^software/$', views.software_search, {"letter": ""}),
    (r'^software/(?P<letter>\w)/$', views.software_search),
    (r'^software/search/$', views.software_search_form),
    (r'^software/compare/$', views.software_compare),
    (r'^software/(?P<object_id>\d+)/$', SoftwareInfo.as_view()),
    (r'^software/(?P<slug>[\w-]+)/$', SoftwareInfo.as_view()),

#    (r'^vocabularies/$', list_detail.object_list, vocabulary_info),
    (r'^vocabularies/$', views.vocabulary_search, {"letter": ""}),
    (r'^vocabularies/(?P<letter>\w)/$', views.vocabulary_search),
    (r'^vocabularies/search/$', views.vocabulary_search_form),
    (r'^vocabularies/compare/$', views.vocabulary_compare),
    (r'^vocabulary/(?P<object_id>\d+)/$', VocabularyInfo.as_view()),
    (r'^vocabulary/(?P<slug>[\w-]+)/$', VocabularyInfo.as_view()),

    (r'^symbollibraries/$', SymbolLibraryList.as_view()),
    (r'^symbollibrary/(?P<object_id>\d+)/$', SymbolLibraryInfo.as_view()),

    (r'^suppliers/$', SupplierList.as_view()),
    (r'^supplier/(?P<object_id>\d+)/$', SupplierInfo.as_view()),
    (r'^supplier/(?P<slug>[\w-]+)/$', SupplierInfo.as_view()),
    url(r'^voca/external_link_list.js$', views.link_list),
)

