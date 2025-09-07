import os
from .credentials import load_credentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load credentials
creds = load_credentials()

print("Loaded credentials:", creds)  # Debugging line

SECRET_KEY = creds['secret_key']
DEBUG = True

ALLOWED_HOSTS = ['api.osd.dynu.net', 'localhost', '127.0.0.1', 'isaac', '185.237.98.234', 'osdapi.ddns.net', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

WSGI_APPLICATION = 'webApi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': creds['db_name'],
        'USER': creds['db_user'],
        'PASSWORD': creds['db_password'],
        'HOST': creds['db_host'],
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend', 
        'rest_framework.filters.OrderingFilter', 
        'rest_framework.filters.SearchFilter', 
    ), 
}

REST_REGISTRATION = {
    'RESET_PASSWORD_VERIFICATION_URL': 'http://localhost:8000/static/reset_password.html',
    'REGISTER_VERIFICATION_URL': 'http://localhost:8000/static/confirm.html',
    'REGISTER_EMAIL_VERIFICATION_URL': 'http://localhost:8000/static/verify-user.html',
    'VERIFICATION_FROM_EMAIL': 'donotreply@localhost',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WARNING: The directory 'static2' in STATICFILES_DIRS does not exist.
# Either create it or remove it from STATICFILES_DIRS if not needed for development.

# Add any other custom settings from your main branch as needed

# Email configuration (loaded from credentials.json)
EMAIL_HOST = creds.get('email_host', 'localhost')
EMAIL_PORT = creds.get('email_port', 25)
EMAIL_HOST_USER = creds.get('email_host_user', '')
EMAIL_HOST_PASSWORD = creds.get('email_host_passwd', '')
EMAIL_USE_TLS = creds.get('email_use_tls', True)
