# Django settings for speechbubble project.

import sys
import os

PROJECT_DIR =os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_DIR)

gettext = lambda s: s

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Main Name', 'email@email.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dbname'             # Or path to database file if using sqlite3.
DATABASE_USER = 'dbuser'             # Not used with sqlite3.
DATABASE_PASSWORD = 'pass'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s

# here is all the languages you want to be supported by the CMS
PAGE_LANGUAGES = (
    ('de', gettext_noop('German')),
    ('fr', gettext_noop('French')),
    ('en', gettext_noop('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_DIR+'/../public_html/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '97qp_w#)9i+hksoul$nm3@7^6ymt9d$4lj_&n3@c-6+y@^tgut'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.auth",
    "django.core.context_processors.media",
    "pages.context_processors.media",
#    "cms.context_processors.media",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'cms.middleware.page.CurrentPageMiddleware',
#    'cms.middleware.user.CurrentUserMiddleware',
#    'cms.middleware.multilingual.MultilingualURLMiddleware',
)

ROOT_URLCONF = 'speechbubble.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/speechbubble/speechbubble/templates',
)

CMS_TEMPLATES = (
    ('cms.htaggingtml', gettext('default')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.comments',
    'pagination',
    'tagging',
    'reversion',
    'sorl.thumbnail',
    'tinymce',
    'filebrowser',
    'mptt',
    'news',
    'events',
    'pages',
    'django_granular_permissions',
    'debug_toolbar',
    'speechbubble.voca',
    'speechbubble.campaign',
)

TINYMCE_DEFAULT_CONFIG = {
    'external_link_list_url' : "/voca/external_link_list.js",
    'height': "300",
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'relative_urls': False,
}

# django-page-cms settings
PAGE_USE_LANGUAGE_PREFIX = False
DEFAULT_PAGE_TEMPLATE = 'pages/index.html'
PAGE_USE_SITE_ID = True
PAGE_TINYMCE = True
PAGE_TAGGING = False

PAGE_TEMPLATES = (
    ('pages/help.html', 'Help page'),
)

# django-debug-toobar settings
def custom_show_toolbar(request):
    if DEBUG:
        return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': True,
}

# django-filebrowser settings
# A list of Images to generate in the format (prefix, image width).
FILEBROWSER_IMAGE_GENERATOR_LANDSCAPE = [
    ('thumbnail_',140),('small_',250),('medium_',460),('big_',500)
]

# A list of Images to generate in the format (prefix, image width).
FILEBROWSER_IMAGE_GENERATOR_PORTRAIT = [
    ('thumbnail_',140),('small_',250),('medium_',460),('big_',500)
]

# A list of Images to generate in the format (prefix, image width, image height). 
FILEBROWSER_IMAGE_CROP_GENERATOR = [
    ('cropped_',75,75),('croppedthumbnail_',60,60)
]

#django-paginate settings
PAGINATION_DEFAULT_WINDOW = 2

try:
    from local_settings import *
except ImportError, exp:
    pass
