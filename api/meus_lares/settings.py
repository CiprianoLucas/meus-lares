"""
Django settings for meus_lares project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ
import os
from pathlib import Path
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

try:
    DB_HOST = env('DB_HOST')
    DB_PORT = env('DB_PORT')
except:
    environ.Env.read_env(os.path.join(BASE_DIR, 'venv', '.env'))
    DB_HOST = env('DB_HOST_DOCKER')
    DB_PORT = env('DB_PORT_DOCKER')

SECRET_KEY = (env("SECRET_KEY"),)

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    'storages',
    'corsheaders',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UserConfig',
    'places.apps.PlacesConfig',
    'requests.apps.RequestsConfig',
    'invoices.apps.InvoicesConfig',
    'ai.apps.AiConfig',
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'meus_lares.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'meus_lares.wsgi.application'

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

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

APPEND_SLASH=False

USE_I18N = True

USE_TZ = True

if env("ENV") == "production":

    DEBUG = False

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
    
    SITE = "meuslares.com.br"

    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_STATIC_LOCATION = "static"
    AWS_MEDIA_LOCATION = "media"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

    STATICFILES_STORAGE = "null"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "null"
    
else:

    DEBUG = True

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
    interface_port = env("INTERFACE_PORT")
    
    CSRF_TRUSTED_ORIGINS = [
        f'http://localhost:{interface_port}',
        f'http://127.0.0.1:{interface_port}',
        'https://meuslares.com.br',
    ]

    MEDIA_URL = "/media/"
    
    SITE = f"localhost:{interface_port}"

    STATIC_URL = "statics/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    
    CORS_ALLOWED_ORIGINS = [
        f"http://localhost:{interface_port}",
        f"http://127.0.0.1:{interface_port}",
        'https://meuslares.com.br',
    ]

    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    CSRF_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://127.0.0.1:6379/1',  # Endereço do Redis
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                # Opcional: compactação dos dados
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            },
            'TIMEOUT': 60 * 15,  # Tempo de expiração do cache (15 minutos)
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
