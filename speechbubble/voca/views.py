import urllib
from django.shortcuts import render_to_response
from django.utils.http import urlencode
from django.http import HttpResponse
from django.template import Context, loader
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.views.generic.edit import FormMixin, FormView
from django.views.generic import TemplateView, ListView, DetailView

from voca.models import Device, Software, Vocabulary
from voca.forms import DeviceSearchForm, SoftwareSearchForm, VocabularySearchForm

# Create your views here.


class FormListView(FormMixin, ListView):
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class DeviceList(FormListView):
    form_class = DeviceSearchForm
    model = Device
    template_name = "voca/device_search_form.html"

    def get_queryset(self):
        try:
            searchdict = self.form_class(self.request.GET).data
        except:
            searchdict = {}
            # It's easier to store a dict of the possible lookups we
        # want, where the values are the keyword arguments for 
        # the actual query.
        qdict = {
            'access': 'access_methods__name__in',
            'device_type': 'device_type__name__in',
            'environmental_control': 'environmental_control',
            'install_own_software': 'install_own_software',
            'internet_capable': 'internet_capable',
            'keyguard': 'keyguards__in',
            'mobile_phone_capable': 'mobile_phone_capable',
            'number_messages': 'number_messages',
            'operating_system': 'operating_system__name',
            'scanning_feedback': 'scanning_indication__name__in',
            'speech_type': 'speech_type',
            'supplier': 'suppliers__slug',
            'touchscreen_size': 'touchscreen',
            'wheelchair_mount': 'wheelchair_mount',
        }
        # Then we can do this all in one step instead of needing
        # to call 'filter' and deal with intermediate data 
        # structures.
        q_objs = [Q(**{qdict[k]: searchdict[k]}) for k in qdict.keys() if searchdict.get(k, None)]

        if 'sort_by' in self.request.GET:
        #            assert False, self.request.GET['sort_by']
            if self.request.GET['sort_by'] == 'weight_high':
                ordering = '-weight_kg'
            elif self.request.GET['sort_by'] == 'weight_low':
                ordering = 'weight_kg'
            elif self.request.GET['sort_by'] == 'price_high':
                ordering = '-guide_price_gbp'
            elif self.request.GET['sort_by'] == 'price_low':
                ordering = 'guide_price_gbp'
            elif self.request.GET['sort_by'] == 'name':
                ordering = 'name'
            else:
                ordering = 'name'
        else:
            ordering = 'name'
        results = Device.objects.filter(*q_objs).order_by(ordering).distinct()

        if 'software' in self.request.GET:
            results = results.filter(
                Q(supplied_software__slug=(self.request.GET['software'])) |
                Q(compatible_software__slug=(self.request.GET['software']))
            )
        if 'vocabulary' in searchdict:
            results = results.filter(
                Q(supplied_software__supplied_vocabularies__slug=(
                    searchdict['vocabulary']
                )) |
                Q(supplied_software__compatible_vocabularies__slug=(
                    searchdict['vocabulary']
                )) |
                Q(compatible_software__supplied_vocabularies__slug=(
                    searchdict['vocabulary']
                )) |
                Q(compatible_software__compatible_vocabularies__slug=(
                    searchdict['vocabulary']
                ))
            )
        if 'weight' in searchdict and searchdict['weight']:
            results = results.filter(
                weight_kg__range=(float(searchdict['weight']) - 0.5, float(searchdict['weight']) + 0.5))
        return results

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeviceList, self).get_context_data(**kwargs)
        context['search_initiated'] = True
        return context


def device_search(request, letter):
    """
    Main device listing and
    also displays the search results.
    """
    search_form = DeviceSearchForm()
    search_initiated = True
    # Check to see if GET request has any data.
    if len(request.GET) > 0:
        search_form = DeviceSearchForm(request.GET)
        if search_form.is_valid():
            searchdict = search_form.cleaned_data
            # It's easier to store a dict of the possible lookups we
            # want, where the values are the keyword arguments for 
            # the actual query.
            qdict = {
                'access': 'access_methods__name__in',
                'device_type': 'device_type__name__in',
                'environmental_control': 'environmental_control',
                'install_own_software': 'install_own_software',
                'internet_capable': 'internet_capable',
                'keyguard': 'keyguards__in',
                'mobile_phone_capable': 'mobile_phone_capable',
                'number_messages': 'number_messages',
                'operating_system': 'operating_system__name',
                'scanning_feedback': 'scanning_indication__name__in',
                'speech_type': 'speech_type',
                'supplier': 'suppliers__slug',
                'touchscreen_size': 'touchscreen',
                'wheelchair_mount': 'wheelchair_mount',
            }
            # Then we can do this all in one step instead of needing
            # to call 'filter' and deal with intermediate data 
            # structures.
            q_objs = [Q(**{qdict[k]: searchdict[k]}) for k in qdict.keys() if searchdict.get(k, None)]

            if 'sort_by' in request.GET:
                if request.GET['sort_by'] == 'weight_high':
                    ordering = '-weight_kg'
                elif request.GET['sort_by'] == 'weight_low':
                    ordering = 'weight_kg'
                elif request.GET['sort_by'] == 'price_high':
                    ordering = '-guide_price_gbp'
                elif request.GET['sort_by'] == 'price_low':
                    ordering = 'guide_price_gbp'
                elif request.GET['sort_by'] == 'name':
                    ordering = 'name'
                else:
                    ordering = 'name'
            else:
                ordering = 'name'

            results = Device.objects.filter(*q_objs).order_by(ordering).distinct()
            if searchdict['software']:
                results = results.filter(
                    Q(supplied_software__slug=(searchdict['software'])) |
                    Q(compatible_software__slug=(searchdict['software']))
                )
            if searchdict['vocabulary']:
                results = results.filter(
                    Q(supplied_software__supplied_vocabularies__slug=(
                        searchdict['vocabulary']
                    )) |
                    Q(supplied_software__compatible_vocabularies__slug=(
                        searchdict['vocabulary']
                    )) |
                    Q(compatible_software__supplied_vocabularies__slug=(
                        searchdict['vocabulary']
                    )) |
                    Q(compatible_software__compatible_vocabularies__slug=(
                        searchdict['vocabulary']
                    ))
                )
            if searchdict['weight']:
                results = results.filter(weight_kg__range=(searchdict['weight'] - 0.5, searchdict['weight'] + 0.5))

            # Encode the GET data to a URL so we can append it to the
            # next and previous page links.
            # use a copy of searchdict excluding entries where the 
            # value is None. This avoids problems with validating the
            # form when building the new url
            urldict = {}
            urldict.update((k, v) for k, v in searchdict.iteritems() if v is not None)
            rawurl = urllib.urlencode(urldict, True)
            if len(rawurl):
                new_url = '&' + rawurl
            else:
                new_url = ''

    else:
        # Return a complete queryset.
        results = Device.objects.all().order_by('name')
        new_url = ''

    # filter by first letter of device name
    if letter:
        regex_filter = '^[' + letter.lower() + letter.upper() + ']'
        results = results.filter(
            name__regex=regex_filter
        )

    number_results = len(results)

    # generate a list of all devices for use in the 'Jump to:' form
    device_list = Device.objects.order_by('name')

    # check if the request asks to skip pagination
    if 'show' in request.GET and request.GET['show'] == 'all':
        paginate_by = 10000
    else:
        paginate_by = 5

    # only display the 'Show All' button if we actually paginate results
    if number_results > paginate_by:
        display_show_all_button = True
    else:
        display_show_all_button = False

    return object_list(
        request,
        results,
        template_name="voca/device_search_form.html",
        extra_context={
            'search_form': search_form,
            'new_url': new_url,
            'search_initiated': search_initiated,
            'number_results': number_results,
            'device_list': device_list,
            'paginate_by': paginate_by,
            'search_initiated': search_initiated,
            'display_show_all_button': display_show_all_button,
        }
    )


class DeviceSearch(FormView):
    form_class = DeviceSearchForm
    template_name = "voca/device_search_form.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeviceSearch, self).get_context_data(**kwargs)
        context['new_url'] = ''
        context['search_initiated'] = False
        context['number_results'] = len(Device.objects.none())
        context['device_list'] = Device.objects.none()
        return context


def device_search_form(request):
    search_form = DeviceSearchForm()
    search_initiated = False
    # Return an empty queryset.
    results = Device.objects.none()
    number_results = len(results)
    new_url = ''
    device_list = Device.objects.order_by('name')

    return object_list(
        request,
        results,
        template_name="voca/device_search_form.html",
        paginate_by=5,
        extra_context={
            'search_form': search_form,
            'new_url': new_url,
            'search_initiated': search_initiated,
            'number_results': number_results,
            'device_list': device_list,
        }
    )


class DeviceDetail(DetailView):
    model = Device

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DeviceDetail, self).get_context_data(**kwargs)
        context['device_list'] = Device.objects.order_by('name')
        return context


def device_compare(request):
    if 'device' in request.GET:
        devices = request.GET.getlist('device')
        device_list = Device.objects.search(devices)
    else:
        device_list = []

    number_results = len(device_list)
    t = loader.get_template('voca/device_compare.html')
    c = Context({
        'device_list': device_list,
        'number_results': number_results,
    })
    return HttpResponse(t.render(c))


def software_search(request, letter):
    """
    Main software listing and
    also displays the search results.
    """
    search_form = SoftwareSearchForm()
    search_initiated = True
    # Check to see if GET request has any data.
    if len(request.GET) > 0:
        search_form = SoftwareSearchForm(request.GET)
        if search_form.is_valid():
            searchdict = search_form.cleaned_data
            # It's easier to store a dict of the possible lookups we
            # want, where the values are the keyword arguments for 
            # the actual query.
            qdict = {
                'supplier': 'suppliers__slug',
                'access': 'access_methods__name__in',
                'auditory_scanning': 'auditory_scanning__name__in',
                'multiple_users': 'multiple_users',
                'second_language_support': 'second_language_support',
                'prediction_enhancement': 'prediction_enhancement__name__in',
                'editable_dictionary': 'editable_dictionary',
                'environmental_control': 'environmental_control',
                'cell_magnification': 'cell_magnification',
            }
            # Then we can do this all in one step instead of needing
            # to call 'filter' and deal with intermediate data 
            # structures.
            q_objs = [Q(**{qdict[k]: searchdict[k]}) for k in qdict.keys() if searchdict.get(k, None)]

            if 'sort_by' in request.GET:
                if request.GET['sort_by'] == 'price_high':
                    ordering = '-guide_price_gbp'
                elif request.GET['sort_by'] == 'price_low':
                    ordering = 'guide_price_gbp'
                elif request.GET['sort_by'] == 'name':
                    ordering = 'name'
                else:
                    ordering = 'name'
            else:
                ordering = 'name'

            results = Software.objects.filter(*q_objs).order_by(ordering).distinct()
            number_results = len(results)
            if searchdict['vocabulary']:
                results = results.filter(
                    Q(supplied_vocabularies__slug=(searchdict['vocabulary'])) |
                    Q(compatible_vocabularies__slug=(searchdict['vocabulary']))
                )

            # Encode the GET data to a URL so we can append it to the
            # next and previous page links.
            urldict = {}
            urldict.update((k, v) for k, v in searchdict.iteritems() if v is not None)
            rawurl = urllib.urlencode(urldict, True)
            if len(rawurl):
                new_url = '&' + rawurl
            else:
                new_url = ''

    else:
        # Return a complete queryset.
        results = Software.objects.all().order_by('name')
        new_url = ''

    # filter by first letter of device name
    if letter:
        regex_filter = '^[' + letter.lower() + letter.upper() + ']'
        results = results.filter(
            name__regex=regex_filter
        )

    paginator = Paginator(results, 5) # Show 5 results per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        search_results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        search_results = paginator.page(paginator.num_pages)

    number_results = len(results)

    software_list = Software.objects.order_by('name')

    return object_list(
        request,
        results,
        template_name="voca/software_search_form.html",
        extra_context={
            'search_form': search_form,
            'new_url': new_url,
            'search_initiated': search_initiated,
            'search_results': search_results,
            'search_results_list': results,
            'number_results': number_results,
            'current_page': page,
            'software_list': software_list,
        }
    )


def software_search_form(request):
    search_form = SoftwareSearchForm()
    search_initiated = False
    # Return an empty queryset.
    results = Software.objects.none()
    number_results = len(results)
    new_url = ''
    software_list = Software.objects.order_by('name')

    return object_list(
        request,
        results,
        template_name="voca/software_search_form.html",
        paginate_by=5,
        extra_context={
            'search_form': search_form,
            'new_url': new_url,
            'search_initiated': search_initiated,
            'number_results': number_results,
            'software_list': software_list,
        }
    )


def software_compare(request):
    if 'software' in request.GET:
        software = request.GET.getlist('software')
        software_list = Software.objects.search(software)
    else:
        software_list = []

    number_results = len(software_list)
    t = loader.get_template('voca/software_compare.html')
    c = Context({
        'software_list': software_list,
        'number_results': number_results,
    })
    return HttpResponse(t.render(c))


def vocabulary_search(request, letter):
    """
    Main software listing and
    also displays the search results.
    """
    search_form = VocabularySearchForm()
    search_initiated = True
    # Check to see if GET request has any data.
    if len(request.GET) > 0:
        search_form = VocabularySearchForm(request.GET)
        if search_form.is_valid():
            searchdict = search_form.cleaned_data
            # It's easier to store a dict of the possible lookups we
            # want, where the values are the keyword arguments for 
            # the actual query.
            qdict = {
                'supplier': 'suppliers__slug',
                'language_representation': 'language_representation',
                'type': 'type',
                'switch_access': 'switch_access',
                'on_screen_keyboard': 'on_screen_keyboard',
                'prediction': 'prediction',
                'software': 'software_supplied_vocabularies__slug',
            }
            # Then we can do this all in one step instead of needing
            # to call 'filter' and deal with intermediate data 
            # structures.
            q_objs = [Q(**{qdict[k]: searchdict[k]}) for k in qdict.keys() if searchdict.get(k, None)]

            if 'sort_by' in request.GET:
                if request.GET['sort_by'] == 'price_high':
                    ordering = '-guide_price_gbp'
                elif request.GET['sort_by'] == 'price_low':
                    ordering = 'guide_price_gbp'
                elif request.GET['sort_by'] == 'name':
                    ordering = 'name'
                else:
                    ordering = 'name'
            else:
                ordering = 'name'

            results = Vocabulary.objects.filter(*q_objs).order_by(ordering).distinct()
            if searchdict['software']:
                results = results.filter(
                    Q(software_supplied_vocabularies__slug=(searchdict['software'])) |
                    Q(software_compatible_vocabularies__slug=(searchdict['software']))
                )
            number_results = len(results)

            # Encode the GET data to a URL so we can append it to the
            # next and previous page links.
            urldict = {}
            urldict.update((k, v) for k, v in searchdict.iteritems() if v is not None)
            rawurl = urllib.urlencode(urldict, True)
            if len(rawurl):
                new_url = '&' + rawurl
            else:
                new_url = ''

    else:
        # Return a complete queryset.
        results = Vocabulary.objects.all().order_by('name')
        new_url = ''

    # filter by first letter of device name
    if letter:
        regex_filter = '^[' + letter.lower() + letter.upper() + ']'
        results = results.filter(
            name__regex=regex_filter
        )

    paginator = Paginator(results, 5) # Show 5 results per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        search_results = paginator.page(page)
    except (EmptyPage, InvalidPage):
        search_results = paginator.page(paginator.num_pages)

    number_results = len(results)

    vocabulary_list = Vocabulary.objects.order_by('name')

    return object_list(
        request,
        results,
        template_name="voca/vocabulary_search_form.html",
        extra_context={
            'search_form': search_form,
            'new_url': new_url,
            'search_initiated': search_initiated,
            'search_results': search_results,
            'search_results_list': results,
            'number_results': number_results,
            'current_page': page,
            'vocabulary_list': vocabulary_list,
        }
    )


def vocabulary_search_form(request):
    search_form = VocabularySearchForm()
    search_initiated = False
    # Return an empty queryset.
    results = Vocabulary.objects.none()
    number_results = len(results)
    new_url = ''
    vocabulary_list = Vocabulary.objects.order_by('name')

    return object_list(
        request,
        results,
        template_name="voca/vocabulary_search_form.html",
        paginate_by=5,
        extra_context={
            'search_form': search_form,
            'new_url': new_url,
            'search_initiated': search_initiated,
            'number_results': number_results,
            'vocabulary_list': vocabulary_list,
        }
    )


def vocabulary_compare(request):
    if 'vocabulary' in request.GET:
        vocabulary = request.GET.getlist('vocabulary')
        vocabulary_list = Vocabulary.objects.search(vocabulary)
    else:
        vocabulary_list = []

    number_results = len(vocabulary_list)
    t = loader.get_template('voca/vocabulary_compare.html')
    c = Context({
        'vocabulary_list': vocabulary_list,
        'number_results': number_results,
    })
    return HttpResponse(t.render(c))


def link_list(request):
    devices = Device.objects.all().order_by('name')
    softwares = Software.objects.all().order_by('name')
    vocabularies = Vocabulary.objects.all().order_by('name')

    t = loader.get_template('voca/link_list.js')
    c = Context({
        'devices': devices,
        'softwares': softwares,
        'vocabularies': vocabularies,
    })
    return HttpResponse(t.render(c))
