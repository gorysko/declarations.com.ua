# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import JsonResponse, Http404

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl.filter import Term, Not

from catalog.elastic_models import Declaration
from catalog.paginator import paginated_search
from catalog.api import hybrid_response


def home(request):
    return render(request, "home.jinja", {})


def suggest(request):
    search = Declaration.search()\
        .suggest(
            'name',
            request.GET.get('q', ''),
            completion={
                'field': 'general.full_name_suggest',
                'size': 10,
                'fuzzy': {
                    'fuzziness': 3,
                    'unicode_aware': 1
                }
            }
    )

    res = search.execute()

    if res.success():
        return JsonResponse(
            [val['text'] for val in res.suggest['name'][0]['options']],
            safe=False
        )
    else:
        return JsonResponse([], safe=False)


@hybrid_response('results.jinja')
def search(request):
    query = request.GET.get("q", "")
    search = Declaration.search()
    if query:
        search = search.query("match", _all=query)
    else:
        search = search.query('match_all')

    return {
        "query": query,
        "results": paginated_search(request, search)
    }


@hybrid_response('declaration.jinja')
def details(request, declaration_id):
    try:
        declaration = Declaration.get(id=int(declaration_id))
    except (ValueError, NotFoundError):
        raise Http404("Таких не знаємо!")

    return {
        "declaration": declaration
    }


@hybrid_response('regions.jinja')
def regions_home(request):
    search = Declaration.search().params(search_type="count")
    search.aggs.bucket(
        'per_region', 'terms', field='general.post.region', size=0)

    res = search.execute()

    return {
        'facets': res.aggregations.per_region.buckets
    }


@hybrid_response('region_offices.jinja')
def region(request, region_name):
    search = Declaration.search()\
        .filter(
            Term(general__post__region=region_name) &
            Not(Term(general__post__office='')))\
        .params(search_type="count")

    search.aggs.bucket(
        'per_office', 'terms', field='general.post.office', size=0)
    res = search.execute()

    return {
        'facets': res.aggregations.per_office.buckets,
        'region_name': region_name
    }


@hybrid_response('results.jinja')
def region_office(request, region_name, office_name):
    search = Declaration.search()\
        .filter('term', general__post__region=region_name)\
        .filter('term', general__post__office=office_name)

    return {
        'query': office_name,
        'results': paginated_search(request, search),
    }


@hybrid_response('results.jinja')
def office(request, office_name):
    search = Declaration.search()\
        .filter('term', general__post__office=office_name)

    return {
        'query': office_name,
        'results': paginated_search(request, search)
    }


def sitemap(request):
    # TODO: REFACTOR ME?
    urls = [
        reverse("home"),
        reverse("about"),
        reverse("regions_home"),
    ]

    search = Declaration.search().params(search_type="count")
    search.aggs.bucket(
        'per_region', 'terms', field='general.post.region', size=0)

    for r in search.execute().aggregations.per_region.buckets:
        urls.append(reverse("region", kwargs={"region_name": r.key}))

        subsearch = Declaration.search()\
            .filter(
                Term(general__post__region=r.key) &
                Not(Term(general__post__office='')))\
            .params(search_type="count")

        subsearch.aggs.bucket(
            'per_office', 'terms', field='general.post.office', size=0)

        for subr in subsearch.execute().aggregations.per_office.buckets:
            urls.append(reverse(
                "region_office",
                kwargs={"region_name": r.key, "office_name": subr.key}))

    search = Declaration.search().params(search_type="count")
    search.aggs.bucket(
        'per_office', 'terms', field='general.post.office', size=0)

    for r in search.execute().aggregations.per_office.buckets:
        urls.append(reverse("office", kwargs={"office_name": r.key}))

    search = Declaration.search().extra(fields=[], size=100000)
    for r in search.execute():
        urls.append(reverse("details", kwargs={"declaration_id": r._id}))

    return render(request, "sitemap.jinja",
                  {"urls": urls}, content_type="application/xml")
