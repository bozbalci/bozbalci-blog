from .base import *  # noqa: F403

# ruff: noqa: F405

SECRET_KEY = "django-insecure-3ef#by+9v1wpn^m)-3nxou2pfr5b$iz#jz7+qw+on@$nfg$89%"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

CORS_ALLOW_ALL_ORIGINS = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

DJANGO_VITE = {
    "default": {
        "dev_mode": True,
        "dev_server_host": os.getenv("VITE_DEV_SERVER_HOST") or "localhost",
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WAGTAILADMIN_BASE_URL = "http://localhost:8080"
