"""
Django settings for webApi project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured
baseDir = os.path.dirname(os.path.realpath(__file__))
#print("settings.py: baseDir="+baseDir)
with open(os.path.join(baseDir, 'credentials.json')) as credentials_file:
    credentials = json.load(credentials_file)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = ')%pkb@=**!kg-l_bd(t3z45ija($4ch6_f*=-cfhqc9h1l$se#'
SECRET_KEY = credentials['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['api.osd.dynu.net', '127.0.0.1', 'isaac', '185.237.98.234', 'osdapi.ddns.net', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_registration',
    'django_filters',
    'datapoints',
    'events',
    'userdata',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'webApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static/dist'),
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#print("TEMPLATES[0]:DIRS=",TEMPLATES[0]['DIRS'])

WSGI_APPLICATION = 'webApi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': credentials['db_name'],
        'USER': credentials['db_user'],
        'PASSWORD': credentials['db_password'],
        'HOST': credentials['db_host'],
        'PORT': credentials['db_port'],
    }
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static2/'),)
print("static_root="+STATIC_ROOT)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ],
#    'DEFAULT_PERMISSION_CLASSES': (
#        'rest_framework.permissions.IsAuthenticated', ),
    
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    #'PAGE_SIZE' : 100,
    'DEFAULT_PAGINATION_CLASS': None,
    'PAGE_SIZE' : None,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend', 
        'rest_framework.filters.OrderingFilter', 
        'rest_framework.filters.SearchFilter', 
    ), 
}


REST_REGISTRATION = {
    'REGISTER_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_ENABLED': True,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
    
    'REGISTER_VERIFICATION_URL': 'https://osdapi.ddns.net/static/confirm.html',
    'RESET_PASSWORD_VERIFICATION_URL': 'https://osdapi.ddns.net/static/reset_password.html',
    'REGISTER_EMAIL_VERIFICATION_URL': 'https://osdapi.ddns.net/static/verify-email.html',
    'VERIFICATION_FROM_EMAIL': 'donotreply@openseizuredetector.org.uk',
    'REGISTER_EMAIL_VERIFICATION_EMAIL_TEMPLATES': {
        'body': 'register_email_templates/body.txt',
        'subject': 'register_email_templates/subject.txt'
    },
    'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
        'body': 'register_verification_templates/body.txt',
        'subject': 'register_verification_templates/subject.txt'
    },
    'RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES': {
        'body': 'reset_password_verification_templates/body.txt',
        'subject': 'reset_password_verification_templates/subject.txt'
    }
}
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

#print("settings.py: REGISTER_EMAIL_VERIFICATION_EMAIL_TEMPLATES=")
#print(REST_REGISTRATION['REGISTER_EMAIL_VERIFICATION_EMAIL_TEMPLATES'])

EMAIL_HOST = credentials['email_host']
EMAIL_PORT = credentials['email_port']
EMAIL_HOST_USER = credentials['email_host_user']
EMAIL_HOST_PASSWORD = credentials['email_host_passwd']
#EMAIL_USE_TLS = True
EMAIL_USE_SSL = True


CORS_ORIGIN_WHITELIST = [
    "https://osd.dynu.net",
    "https://api.osd.dynu.net",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://192.168.0.10:3000"
]


#print(TEMPLATES)
