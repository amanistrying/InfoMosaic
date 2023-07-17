"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

"""from storages.backends.azure_storage import AzureStorage
from google.cloud import storage"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i%n95i9y925_w=fw+gs*viuwwv-sf@#6fk-&ztpim@f@aqf*_#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'serviceprovider',
        'USER': 'root',
        'PASSWORD': 'firefrost',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py


"""DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = 'infomosaic'
AZURE_ACCOUNT_KEY = 'zIjEcIDuwYDzogSTSW4a1p9lsXYwS7zmDB+OGPQrzGA4dky5E0tGXkuQhVDKVgp8AH5r3QwJCpu8+AStbhMO4w=='
AZURE_CONTAINER = 'verificationdocument'
AZURE_STORAGE_CONNECTION_STRING = '<DefaultEndpointsProtocol=https;AccountName=infomosaic;AccountKey=zIjEcIDuwYDzogSTSW4a1p9lsXYwS7zmDB+OGPQrzGA4dky5E0tGXkuQhVDKVgp8AH5r3QwJCpu8+AStbhMO4w==;EndpointSuffix=core.windows.net>'


# Static files configuration
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
STATIC_URL = 'https://infomosaic.blob.core.windows.net/verificationdocument/'"""

# Use database for session storage
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Set session cookie as HTTP-only for better security
SESSION_COOKIE_HTTPONLY = True
# Use secure cookies for sessions (requires HTTPS)
SESSION_COOKIE_SECURE = True
