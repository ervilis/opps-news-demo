# -*- coding: utf-8 -*-

import os
import djcelery

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'news.db'),
    }
}

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'ec_ghvlo7l7xo@8fbx+kii+43tb#l)9hbmwie(@&^5d+38b-o@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    'opps.channels.context_processors.channel_context',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    # Used in Multi-Site
    'opps.contrib.multisite.middleware.DynamicSiteMiddleware',
    # Used in Mobile Detection
    'opps.contrib.mobile.middleware.MobileDetectionMiddleware',
)

TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'templates'),)
TEMPLATE_DIRS_WEB = TEMPLATE_DIRS
TEMPLATE_DIRS_MOBILE = (os.path.join(PROJECT_PATH, 'templates', 'mobile'),)

INSTALLED_APPS = [
    # Django core
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',

    # Admin
    'opps.contrib.admin',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',

    # Opps core
    'opps.core',
    'opps.core.tags',
    'opps.containers',
    'opps.boxes',
    'opps.channels',
    'opps.containers',
    'opps.articles',
    'opps.archives',
    'opps.images',
    'opps.sitemaps',
    'opps.flatpages',
    'opps.archives',
    'opps.fields',
    'opps.api',

    # Opps contrib
    'opps.contrib.fileupload',

    # Dependence
    'south',
    'appconf',
    'haystack',
    'mptt',
    'googl',
    'djcelery',
    'endless_pagination',

    'news',
    'opps.comments',
]

djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

OPPS_CHECK_MOBILE = True

MEDIA_URL = '/media/'

THUMBOR_ENABLED = False
# THUMBOR_MEDIA_URL = 'http://localhost:8000/media/'

TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

CACHES = {'default': {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}

HAYSTACK_CONNECTIONS = {
    "default": {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'public', 'static')
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'public', '_static'),)

URL_TINYMCE = STATIC_URL + "tinymce"
PATH_TINYMCE = STATIC_URL + "tinymce"

ROOT_URLCONF = 'news.urls'

OPPS_COMMENTS = {
    "disqus": {
        "shortname": "oppsnewsdemo",
    }
}

try:
    from local_settings import *
except ImportError:
    pass
