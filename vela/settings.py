"""
Django settings for asip project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#BASE_PATH = os.path.abspath(os.path.dirname('.'))
#if 'collectstatic' in sys.argv:
#    BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't$k!qevcjm$3^3vf83=umj+p13j67l66#f*g)na5=t&b#06q+x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Library
    'ckeditor',


    # Project
    'common',
    'account',
    'keyvela',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'common.middleware.RequestProvider',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'common.context_processors.helper'
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),

)

ROOT_URLCONF = 'vela.urls'

WSGI_APPLICATION = 'vela.wsgi.application'
ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# createdb vela
# psql vela
# CREATE USER vela WITH PASSWORD 'vela';
# GRANT ALL PRIVILEGES ON DATABASE vela to vela;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vela',
        'USER': 'vela',
        'PASSWORD': 'vela',
        'HOST': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'sitestatic/')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTH_USER_MODEL = 'account.User'

AUTHENTICATION_BACKENDS = (

    'account.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

SESSION_COOKIE_AGE = 60*60*24

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format'],
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['MediaEmbed']
        ],
        'width': 'auto',
        'height': '200',
        'format_tags': 'p;h3;h4;h5',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow,mediaembed',
        'forcePasteAsPlainText': True,
    },
    'minimal': {
        'toolbar': [
            ['Format'],
            ['Bold', 'Italic'],
            ['NumberedList', 'BulletedList'],
        ],
        'format_tags': 'p;h3;h4;h5',
        'width': 'auto',
        'height': '200',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow',
        'forcePasteAsPlainText': True,
    },
    'bold': {
        'toolbar': [
            ['Bold'],
        ],
        'width': 'auto',
        'height': '80',
        'autoGrow_minHeight': '80',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow',
        'forcePasteAsPlainText': True,
    },
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
        'SocialAuth': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'




# CUSTOM ASIP PROJECT #############################

SITE_NAME = 'Vela'
SITE_SLOGAN = 'Time Logging'
DEFAULT_FROM_EMAIL = 'Time <no-reply@time.opendram.co.th>'
SITE_URL = 'http://time.opendram.co.th'
SITE_LOGO_URL = '%simages/logo.png' % STATIC_URL
SITE_FAVICON_URL = '%simages/favicon.png' % STATIC_URL


GOOGLE_ANALYTICS_KEY = ''



LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/account/error/'


TASTYPIE_DEFAULT_FORMATS = ['json']

# OVERRIDE SETTINGS ###########################################################
try:
    from settings_local import *
except ImportError:
    pass


# TESTING #####################################################################
if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
    MEDIA_URL = '/test_media/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if 'runserver' in sys.argv:
    DEBUG = True


# DEBUG MODE ##################################################################

if DEBUG:
    #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    COMPRESS_ENABLED = False
    GOOGLE_ANALYTICS_KEY = ''
