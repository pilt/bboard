# -*- coding: utf-8 -*-
from urllib import urlencode
import hashlib

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core.serializers.json import simplejson as json
from haystack.forms import ModelSearchForm
from haystack.query import EmptySearchQuerySet

from board.models import Entry, Search

def hash(s):
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

LIU_SEARCH_BASE = 'http://www.student.liu.se/anslagstavlan/sokning'
LIU_SEARCH_ARGS = {
    'px-charset': 'iso-8859-1',
    'px_action': 'perform_search',
    'px-url': 'http://www2.student.liu.se/cgi-bin/anslagstavlan/index.pl'
}


class SearchView(object):
    __name__ = 'SearchView'
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE
    
    def __init__(self, template=None, load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset
        
        if not results_per_page is None:
            self.results_per_page = results_per_page
        
        if template:
            self.template = template
    
    def __call__(self, request):
        """
        Generates the actual response to the search.
        
        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        if request.is_ajax():
            return self.create_ajax_response()
        
        self.form = self.build_form()
        self.query = self.get_query()

        # Cache results.
        key = hash(self.query)
        res = cache.get(key)
        if res is None:
            res = self.get_results().order_by('-submitted')
            cache.set(key, res)
        self.results = res

        query = self.query.strip()
        if query:
            db_search, db_search_created = Search.objects.get_or_create(
                term=query,
            )
            db_search.hit_count = self.results.count()
            db_search.save()
        
        return self.create_response()

    def create_ajax_response(self):
        completes = []
        try:
            term = self.request.GET['term']
            searches = Search.objects.filter(
                term__icontains=term
            ).exclude(
                hit_count=0
            ).order_by('-hit_count')
            completes = [s.term for s in searches]
        except KeyError:
            pass
        return HttpResponse(json.dumps(completes), mimetype='text/plain')
    
    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)
        
        if len(self.request.GET):
            data = self.request.GET
        
        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset
        
        return self.form_class(data, **kwargs)
    
    def get_query(self):
        """
        Returns the query provided by the user.
        
        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']
        
        return ''
    
    def get_results(self):
        """
        Fetches the results via the form.
        
        Returns an empty list if there's no query to search with.
        """
        return self.form.search()
    
    def build_page(self):
        """
        Paginates the results appropriately.
        
        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        paginator = Paginator(self.results, self.results_per_page)
        
        try:
            page = paginator.page(self.request.GET.get('page', 1))
        except InvalidPage:
            raise Http404
        
        return (paginator, page)

    def build_latest_searches(self):
        limit = 60 
        return Search.objects.exclude(hit_count=0).order_by('-when')[:limit]
    
    def extra_context(self):
        """
        Allows the addition of more context variables as needed.
        
        Must return a dictionary.
        """
        return {
            'alternatives': self.build_alternatives(self.query),
            'entries': Entry.objects.all(),
            'latest_searches': self.build_latest_searches(),
        }

    def build_alternatives(self, arg):
        categories = [
            (_('books'), [
                (
                    _('search adlibris'), 
                    u'http://www.adlibris.com/se/searchresult.aspx',
                    lambda a: urlencode({'title': a.encode('utf-8')}),
                ),
                (
                    _('search bokus'), 
                    u'http://www.bokus.com/cgi-bin/product_search.cgi',
                    lambda a: urlencode({'search_word': a.encode('latin-1')}),
                ),
            ]),
            (_('other'), [
                (
                    _('search at LiU'), 
                    LIU_SEARCH_BASE,
                    lambda a: urlencode(dict(
                        LIU_SEARCH_ARGS.items() + [
                            ('px_string', a.encode('utf-8')),
                        ]
                    )),
                ),
            ]),
        ]

        built = []
        for category, links in categories:
            cat = {
                'name': category,
                'links': [],
            }
            for text, base, linker in links:
                cat['links'].append({
                    'text': text,
                    'url': u"%s?%s" % (base, linker(arg)),
                })
            built.append(cat)
        return built
    
    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }
        
        if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            context['suggestion'] = self.form.get_suggestion()
        
        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))


def search_view_factory(view_class=SearchView, *args, **kwargs):
    def search_view(request):
        return view_class(*args, **kwargs)(request)
    return search_view


class FacetedSearchView(SearchView):
    __name__ = 'FacetedSearchView'
    
    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['facets'] = self.results.facet_counts()
        return extra


def basic_search(request, template='search/search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, extra_context=None, results_per_page=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.
    
    Useful as an example of for basing heavily custom views off of.
    
    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.
    
    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()
    
    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)
        
        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)
    
    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)
    
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")
    
    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }
    
    if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
        context['suggestion'] = form.get_suggestion()
    
    if extra_context:
        context.update(extra_context)
    
    return render_to_response(template, context, context_instance=context_class(request))

