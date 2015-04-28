"""
Django settings for declarations_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from os.path import abspath, dirname, join

# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ko&yhvm&@5d(qm6#!s#725r-&37@s8gq60evfsm*odv#s9@2+z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',

    'pipeline',
    'django_jinja',
    'django_jinja.contrib._humanize',
    'catalog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'declarations_site.urls'
WSGI_APPLICATION = 'declarations_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# SQLite (simplest install)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

# PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'declarations',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }



# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'compressor.finders.CompressorFinder',
)

PIPELINE_CSS = {
    'css_all': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/material.css',
            'css/ripples.css',
            'css/animate.css',
            'css/style.css',
            'css/decls.css',
        ),
        'output_filename': 'css/merged.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'js_all': {
        'source_filenames': (
            "js/jquery-1.11.2.js",
            "js/bootstrap.js",
            "js/bootstrap3-typeahead.js",
            "js/ripples.js",
            "js/material.js",
            "js/main.js"
        ),
        'output_filename': 'js/merged.js',
    }
}

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "catalog.context_processors.stats_processor"
)

# Wagtail settings

LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

WAGTAIL_SITE_NAME = "declarations_site"

# Use Elasticsearch as the search backend for extra performance and better search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/search/backends.html#elasticsearch-backend
#
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'URLS': ['http://localhost:9200'],
        'INDEX': 'wagtail',
    },
}

# Setup Elasticsearch default connection
# ELASTICSEARCH_CONNECTIONS = {
#     'default': {
#         'hosts': 'localhost',
#         'timeout': 20
#     }
# }

# Whether to use face/feature detection to improve image cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False
