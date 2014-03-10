import re
import itertools

from django.forms import ValidationError
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.views.generic import TemplateView

from voca.models import Device, Software, Vocabulary, Supplier

#Create your views here.

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomeView, self).get_context_data(**kwargs)
        context['device_list'] = Device.objects.order_by('name')
        context['software_list'] = Software.objects.order_by('name')
        context['vocabulary_list'] = Vocabulary.objects.order_by('name')
        context['supplier_list'] = Supplier.objects.order_by('name')
        return context


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid 
        of unecessary spaces and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That 
        combination aims to search keywords within a model by 
        testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    query_string = ''
    results = []
    if ('q' in request.GET) and request.GET['q'].strip():
        search_terms = normalize_query(request.GET['q'])
        query_string = request.GET['q']
                                
        name_query = get_query(query_string, ['name', ])
        entry_query = get_query(query_string, ['short_description','long_description', ])
                                                
        device_found_names = Device.objects.filter(name_query).order_by('-date_uk_release')
        software_found_names = Software.objects.filter(name_query).order_by('-date_uk_release')
        vocabulary_found_names = Vocabulary.objects.filter(name_query).order_by('-date_uk_release')

        device_found_entries = Device.objects.filter(entry_query).order_by('-date_uk_release')
        software_found_entries = Software.objects.filter(entry_query).order_by('-date_uk_release')
        vocabulary_found_entries = Vocabulary.objects.filter(entry_query).order_by('-date_uk_release')

        results = [i for i in itertools.chain(
            device_found_names,
            software_found_names,
            vocabulary_found_names,
            device_found_entries,
            software_found_entries,
            vocabulary_found_entries,
        )]

    number_results = len(results)

    return render_to_response(
        'search/search_results.html', { 
            'query_string': query_string, 
            'search_terms': search_terms, 
            'results': results, 
            'number_results': number_results, 
        },
        context_instance=RequestContext(request)
    )


def help_search(request):
    query_string = request.GET.get('q', "")

    if search_terms:
        query = Q()
        for term in search_terms:
            query &= Q(content__icontains=term) | Q(title__icontains=term)
            results = results.filter(query)

    return render_to_response("flatpages/search.html", 
        {'query': query_string, 'terms': search_terms, 'results': results}
    ) 


