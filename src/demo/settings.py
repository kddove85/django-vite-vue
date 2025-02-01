"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import json
import dj_database_url
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# https://docs.djangoproject.com/en/2.2/ref/settings/#admins
ADMINS = config('ADMINS', cast=json.loads)

# Recommended Security + Deployment stuff
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', cast=int, default=0)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', cast=bool, default=False)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', cast=bool, default=False)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', cast=bool, default=False)
SECURE_PROXY_SSL_HEADER = config('SECURE_PROXY_SSL_HEADER', default=None,
                                 cast=lambda v: Csv(post_process=tuple)(v) if v else None)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', cast=bool, default=False)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool, default=False)
USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST', cast=bool, default=False)

# Email
# https://docs.djangoproject.com/en/3.0/topics/email/

SERVER_EMAIL = config('SERVER_EMAIL', default='root@localhost')

EMAIL_HOST = config('EMAIL_HOST', default='localhost')

EMAIL_SUBJECT_PREFIX = f"[{config('EMAIL_SUBJECT_PREFIX', default='localhost')}] "


# Application definition

# Add additional non-Django apps here for consistent logging behavior
EXTRA_APPS = [
    'demo_ui',
    'demo_auth',
    'demo_api',
]


INSTALLED_APPS = [
    *EXTRA_APPS,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_vite',
    'rest_framework',
]

if DEBUG:
    INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'demo_auth.context_processors.login_url',
                'demo_auth.context_processors.logout_url',
                'demo_auth.context_processors.register_url',
                'demo_ui.context_processors.spa_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'

# Google Analytics

GA_MEASUREMENT_ID = config('GA_MEASUREMENT_ID', default=None)


# Authentication

AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/accounts/login/'
REGISTER_URL = '/register/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', '/')


# Mozilla OIDC
# https://mozilla-django-oidc.readthedocs.io/en/stable/

# OIDC_RP_CLIENT_ID = config('OIDC_RP_CLIENT_ID', default=None)
# OIDC_RP_CLIENT_SECRET = config('OIDC_RP_CLIENT_SECRET', default=None)
# OIDC_OP_AUTHORIZATION_ENDPOINT = config('OIDC_OP_AUTHORIZATION_ENDPOINT', default=None)
# OIDC_OP_TOKEN_ENDPOINT = config('OIDC_OP_TOKEN_ENDPOINT', default=None)
# OIDC_OP_USER_ENDPOINT = config('OIDC_OP_USER_ENDPOINT', default=None)
# OIDC_RP_SIGN_ALGO = config('OIDC_RP_SIGN_ALGO', default='RS256')
# OIDC_OP_JWKS_ENDPOINT = config('OIDC_OP_JWKS_ENDPOINT', default=None)
# OIDC_USERNAME_ALGO = 'oidc_auth.auth.generate_username'
# OIDC_RP_SCOPES = 'openid email profile'
# OIDC_CREATE_USER = config('OIDC_CREATE_USER', default=True, cast=bool)
#
# if (OIDC_RP_CLIENT_ID and OIDC_RP_CLIENT_SECRET and OIDC_OP_AUTHORIZATION_ENDPOINT
#         and OIDC_OP_TOKEN_ENDPOINT and OIDC_OP_USER_ENDPOINT):
#     EXTRA_APPS += ['mozilla_django_oidc']
#     AUTHENTICATION_BACKENDS += ['oidc_auth.auth.UMichOIDCBackend']
#     LOGIN_URL = '/oidc/authenticate/'
# else:
#     print('Skipping OIDCAuthenticationBackend as OIDC variables were not set.')


# Django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}


# Django Vite settings
DJANGO_VITE = {
  "default": {
    "dev_mode": bool(int(config("DEBUG"))),
    "static_url_prefix": "vite",
    "manifest_path": os.path.join(BASE_DIR, "static", "vite", "manifest.json")
  }
}






# Database
# Default for Django tables
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3'),
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE', default='America/Detroit')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
            'filters': ['require_debug_false']
        }
    },
    'root': {
        'handlers': ['console'],
        'level': config('LOGGING_LEVEL', default='INFO'),
    },
    'loggers': {
        'django': {
            'level': config('LOGGING_LEVEL', default='INFO'),
            'handlers': ['console', 'mail_admins'],
            'propagate': False
        },
        **{
            app: {
                'level': config('LOGGING_LEVEL', default='INFO'),
                'handlers': ['console', 'mail_admins'],
                'propagate': False
            } for app in EXTRA_APPS
        }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    ("vite", os.path.join(BASE_DIR, "assets", "build"))
]

# Whitenoise

WHITENOISE_MAX_AGE = config('WHITENOISE_MAX_AGE', cast=int, default=86400 if not DEBUG else 0)

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
