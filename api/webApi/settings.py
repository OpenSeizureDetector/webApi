import os
from .settings.credentials import load_credentials

creds = load_credentials()

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

SECRET_KEY = creds['secret_key']

# ... rest of your Django settings ...
