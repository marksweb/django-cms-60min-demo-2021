import os
import logging
import sys
import traceback
from typing import List
from enum import Enum
from typing import Optional

import sentry_sdk
from djangocms_helpers.sentry_500_error_handler.ignore_io_error import ignore_io_error
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from env_settings import env
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv('.env-local'))


################################################################################
## === divio === ##
################################################################################


INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-django-cms',
    'django-filer',
    # </INSTALLED_ADDONS>
]


import aldryn_addons.settings

aldryn_addons.settings.load(locals())


################################################################################
## === django === ##
################################################################################


INSTALLED_APPS: List[str] = locals()['INSTALLED_APPS']
MIDDLEWARE: List[str] = locals()['MIDDLEWARE']
BASE_DIR: str = locals()['BASE_DIR']
STATIC_URL: str = locals()['STATIC_URL']
TEMPLATES: List[dict] = locals()['TEMPLATES']
SITE_ID: int = locals()['SITE_ID']


DATE_FORMAT = 'F j, Y'


class DivioEnv(Enum):
    LOCAL = 'local'
    TEST = 'test'
    LIVE = 'live'


DIVIO_ENV_ENUM = DivioEnv
DIVIO_ENV = DivioEnv(env.get('STAGE', 'local'))


installed_apps_first = [
    # for USERNAME_FIELD = 'email', before `cms` since it has a User model
    'backend.auth',

    # must be before `cms`
    'djangocms_modules',

    # tempaltes override
    'backend.blog',
]
INSTALLED_APPS = installed_apps_first + INSTALLED_APPS

INSTALLED_APPS.extend([
    # django

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cuser',  # for USERNAME_FIELD = 'email' in backend.auth
    'gtm',
    'solo',
    'rest_framework',
    'import_export',
    'adminsortable2',
    'admin_reorder',
    'django_extensions',
    'widget_tweaks',
    'django_countries',
    'logentry_admin',
    'hijack_admin',

    # django cms

    'aldryn_apphooks_config',
    'djangocms_blog',
        'taggit',
        'taggit_autosuggest',
        'sortedm2m',
    'djangocms_icon',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_googlemap',
    'djangocms_video',
    'djangocms_history',
    'djangocms_picture',
    'djangocms_snippet',
    'djangocms_helpers',
    'djangocms_helpers.sentry_500_error_handler',
    'djangocms_page_meta',
        'meta',
    'aldryn_forms_bs4_templates',
    'aldryn_forms',
        'aldryn_forms_recaptcha_plugin',
            'snowpenguin.django.recaptcha3',
        'absolute',
        'aldryn_forms.contrib.email_notifications',
        'emailit',
    'djangocms_redirect',
    'light_gallery',
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',

    # project

    'backend.plugins.default.toc',
    'backend.plugins.default.bs4_hiding',
    'backend.plugins.default.bs4_spacer',
    'backend.plugins.default.heading_element',
    'backend.plugins.default.section_element',
    'backend.plugins.default.horizontal_line',
    'backend.plugins.default.section_with_image_background',
    'backend.plugins.default.person_list',
])

MIDDLEWARE.extend([
    # django
    'admin_reorder.middleware.ModelAdminReorder',

    # django cms optional
    'djangocms_redirect.middleware.RedirectMiddleware',
])

# removes frustrating validations, eg `too similar to your email`
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

AUTH_USER_MODEL = 'backend_auth.User'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/'),
]

default_template_engine: dict = TEMPLATES[0]
default_template_engine['DIRS'].extend([
    os.path.join(BASE_DIR, 'backend/templates/'),
])
default_template_engine['OPTIONS']['context_processors'].extend([
    'django_settings_export.settings_export',
])

if DIVIO_ENV == DivioEnv.LOCAL:
    email_backend_default = 'django.core.mail.backends.console.EmailBackend'
else:
    email_backend_default = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = env.get('EMAIL_BACKEND', default=email_backend_default)

DEFAULT_FROM_EMAIL = 'Project Name <info@example.com>'


if DIVIO_ENV == DivioEnv.LOCAL:
    ssl_redirect_default = False
else:
    ssl_redirect_default = True

SECURE_SSL_REDIRECT = env.get_bool('SECURE_SSL_REDIRECT', default=ssl_redirect_default)


HTTP_PROTOCOL = 'http' if DIVIO_ENV == DivioEnv.LOCAL else 'https'


LANGUAGES = [
    ('en', "English"),
    ('nl', "Netherlands"),
]

CMS_LANGUAGES = {
    SITE_ID: [
        {
            'code': 'en',
            'name': 'English',
        },
        {
            'code': 'nl',
            'name': 'Dutch',
        },
    ],
    'default': {
        'fallbacks': ['en', 'nl'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    }
}

PARLER_LANGUAGES = CMS_LANGUAGES

################################################################################
## === django === ##
################################################################################


# allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = HTTP_PROTOCOL
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False  # otherwise admins can't access the login view
LOGIN_REDIRECT_URL = '/'
CONFIRM_EMAIL_ON_GET = True

GTM_CONTAINER_ID = env.get('GTM_CONTAINER_ID', 'GTM-1234')

WEBPACK_DEV_URL = env.get('WEBPACK_DEV_URL', default=f'http://localhost:8090/assets/')

# the default doesn't support names hashing
STATICFILES_STORAGE = 'aldryn_django.storage.ManifestGZippedStaticFilesStorage'
# the default is 5m
STATICFILES_DEFAULT_MAX_AGE = 60 * 60 * 24 * 365

SETTINGS_EXPORT = [
    'WEBPACK_DEV_URL',
    'DIVIO_ENV',
    'DIVIO_ENV_ENUM',
    'IS_SENTRY_ENABLED',
    'SENTRY_DSN',
    'GTM_CONTAINER_ID',
    'DEBUG',
]

IS_SENTRY_ENABLED = env.get_bool('IS_SENTRY_ENABLED', False)
SENTRY_DSN = env.get('SENTRY_DSN')
if IS_SENTRY_ENABLED:
    # noinspection PyTypeChecker
    sentry_sdk.init(
        before_send=ignore_io_error,
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=None,  # Send no events from log messages
            )
        ],
        environment=DIVIO_ENV.value,
        send_default_pii=True,
    )


HIJACK_REGISTER_ADMIN = False
HIJACK_ALLOW_GET_REQUESTS = True


ADMIN_REORDER = [
    {
        'label': 'Users',
        'app': 'auth',
        'models': [
            'backend_auth.User',
            'auth.Group',
        ],
    },
    {
        'label': 'CMS',
        'app': 'cms',
        'models': [
            'cms.Page',
            {'model': 'filer.Folder', 'label': 'Media'},
            'djangocms_redirect.Redirect',
            {'model': 'aldryn_forms.FormSubmission', 'label': 'Dynamic forms submissions'},
        ],
    },
    {
        'app': 'djangocms_blog'
    },
    {
        'label': 'System Administration',
        'app': 'cms',
        'models': [
            {'model': 'sites.Site', 'label': 'Websites'},
            {'model': 'djangocms_modules.Category', 'label': 'Plugin modules categories'},
            {'model': 'djangocms_snippet.Snippet', 'label': 'HTML snippets'},
            
            # removed because it doesn't work on cms 3.7.1
            # 'cms.GlobalPagePermission',
            # 'cms.PageUserGroup',
            # 'cms.PageUser',
        ],
    },
    {
        'label': 'SEO',
        'app': 'cms',
        'models': [
            {'model': 'robots.Rule', 'label': 'Access rules for robots.txt'},
            {'model': 'robots.Url', 'label': 'Urls patterns for robots.txt'},
        ],
    },
]


RECAPTCHA_PUBLIC_KEY = env.get('RECAPTCHA_PUBLIC_KEY', '6LcI2-YUAAAAALOlCkObFFtMkOYj1mhiArPyupgj')
RECAPTCHA_PRIVATE_KEY = env.get('RECAPTCHA_PRIVATE_KEY', '6LcI2-YUAAAAADHRo9w9nVNtPW2tPx9MS4yqEvD6')
RECAPTCHA_SCORE_THRESHOLD = 0.85


################################################################################
## === django-cms core === ##
################################################################################


CMS_TEMPLATES = [
    ('full-width.html', 'full width'),
    ('one-column.html', 'content width'),
    ('two-columns-main-left.html', 'content width - two columns'),
]


X_FRAME_OPTIONS = 'SAMEORIGIN'


################################################################################
## === django-cms optional === ##
################################################################################


BLOG_PERMALINK_URLS = {
    'full_date': r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',
    'short_date': r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>\w[-\w]*)/$',
    'category': r'^(?P<category>\w[-\w]*)/(?P<slug>\w[-\w]*)/$',
    'slug': r'^(?P<slug>\w[-\w]*)/$',
}


DJANGOCMS_BOOTSTRAP4_GRID_SIZE = 24


DJANGOCMS_GOOGLEMAP_API_KEY = env.get('DJANGOCMS_GOOGLEMAP_API_KEY', '123')

CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar': 'CUSTOM',
    'toolbar_CUSTOM': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles', 'FontSize'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord', 'RemoveFormat'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', ],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        # remove 'Link' since we have bootstrap4 link/button plugin
        ['Unlink'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
    'stylesSet': f'default:{STATIC_URL}global/ts/ckeditor-config.js',
    'contentsCss': [
        f'{WEBPACK_DEV_URL}/vendor.css' if DIVIO_ENV == DivioEnv.LOCAL else f'{STATIC_URL}/dist/vendor.css',
        f'{WEBPACK_DEV_URL}/global.css' if DIVIO_ENV == DivioEnv.LOCAL else f'{STATIC_URL}/dist/global.css',
        f'{STATIC_URL}/djangocms_text_ckeditor/ckeditor/contents.css',
    ],
    'config': {
        'allowedContent': True,
        'fillEmptyBlocks': False, # doesn't seem to be doing anything, but was part of the old config
    }
}

# for djangocms-helpers send_email
META_SITE_PROTOCOL = HTTP_PROTOCOL
META_USE_SITES = True
