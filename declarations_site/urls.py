import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailsearch import urls as wagtailsearch_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

urlpatterns = patterns(
    '',
    url(r'^$', 'catalog.views.home', name='home'),
    url(r'^ajax/suggest$', 'catalog.views.suggest', name='suggest'),
    url(r'^about$', TemplateView.as_view(template_name='about.jinja'),
        name="about"),
    url(r'^api$', TemplateView.as_view(template_name='api_doc.jinja'),
        name="api_doc"),

    url(r'^search$', 'catalog.views.search', name='search'),
    url(r'^declaration/(?P<declaration_id>\d+)$', 'catalog.views.details',
        name='details'),

    url(r'^region$', 'catalog.views.regions_home', name='regions_home',),

    # Please maintain that order
    url(r'^region/(?P<region_name>[^\/]+)/(?P<office_name>.+)$',
        'catalog.views.region_office', name='region_office'),
    url(r'^region/(?P<region_name>.+)$', 'catalog.views.region',
        name='region'),

    url(r'^office/(?P<office_name>.+)$', 'catalog.views.office',
        name='office'),

    url(r'^sitemap.xml$', 'catalog.views.sitemap',
        name='sitemap'),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
