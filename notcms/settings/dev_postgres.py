from .base import *

SECRET_KEY = "django-insecure-3ef#by+9v1wpn^m)-3nxou2pfr5b$iz#jz7+qw+on@$nfg$89%"

DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

CORS_ALLOW_ALL_ORIGINS = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

DJANGO_VITE = {"default": {"dev_mode": True}}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "notcms",
        "USER": "bozbalci",
        "PASSWORD": "my_psql_password",
        "CONN_MAX_AGE": 600,
    }
}
