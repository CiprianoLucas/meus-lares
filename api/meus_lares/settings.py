"""
Django settings for meus_lares project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

import environ
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))

IS_DOCKER = env("IS_DOCKER") == "True"

if IS_DOCKER:
    environ.Env.read_env(os.path.join(BASE_DIR, "venv", ".env"))
    DB_HOST = env("DB_HOST_DOCKER")
    DB_PORT = env("DB_PORT_DOCKER")
else:
    DB_HOST = env("DB_HOST")
    DB_PORT = env("DB_PORT")


SECRET_KEY = (env("SECRET_KEY"),)

INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "users.apps.UserConfig",
    "places.apps.PlacesConfig",
    "relations.apps.RelationsConfig",
    "condo_files.apps.CondoFilesConfig",
    "bills.apps.BillsConfig",
    "notifications.apps.NotificationsConfig",
    # 'condo_requests.apps.CondoRequestsConfig',
    # 'invoices.apps.InvoicesConfig',
    # 'ai.apps.AiConfig',
    "storages",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]


ROOT_URLCONF = "meus_lares.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "meus_lares.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

APPEND_SLASH = False

USE_I18N = True

USE_TZ = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{"redis" if IS_DOCKER else env("REDIS_IP")}:{env("REDIS_PORT")}/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
        "TIMEOUT": 60 * 60 * 24,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True

GOOGLE_CLIENT_ID = env("VITE_GOOGLE_CLIENT_ID")
SITE_ID = 1
LOGIN_REDIRECT_URL = env("URL_FRONT")
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL + "/login"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGOUT_REDIRECT_URL

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}"

AWS_STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/"

AWS_MEDIA_LOCATION = "media/public"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/"

AWS_PRIVATE_MEDIA_LOCATION = "media/private"
PRIVATE_MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_PRIVATE_MEDIA_LOCATION}/"

if env("ENV") == "production":
    DEBUG = False

    ALLOWED_HOSTS = ["meuslares.com.br", "api.meuslares.com.br"]

    SITE = "api.meuslares.com.br"

    CSRF_TRUSTED_ORIGINS = [
        "https://meuslares.com.br",
        "https://api.meuslares.com.br",
    ]

    CORS_ALLOWED_ORIGINS = ["https://meuslares.com.br", "https://api.meuslares.com.br"]

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "default_acl": AWS_DEFAULT_ACL,
                "object_parameters": AWS_S3_OBJECT_PARAMETERS,
                "location": AWS_MEDIA_LOCATION,
            },
        },
        "private": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "default_acl": "private",
                "location": PRIVATE_MEDIA_URL,
                "object_parameters": {
                    "CacheControl": "max-age=86400",
                },
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "default_acl": AWS_DEFAULT_ACL,
                "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            },
        },
    }

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


else:

    interface_port = env("INTERFACE_PORT")

    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

    DEBUG = True
    SITE = f"localhost:{env('API_PORT')}"
    CSRF_TRUSTED_ORIGINS = [
        f"http://localhost:{interface_port}",
        f"http://127.0.0.1:{interface_port}",
    ]

    CORS_ALLOWED_ORIGINS = [
        f"http://localhost:{interface_port}",
        f"http://127.0.0.1:{interface_port}",
    ]

    MEDIA_URL = "/media/"
    STATIC_URL = "static/"

    STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
