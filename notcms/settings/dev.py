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

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

STORAGES = {
    # "default": {
    #     "BACKEND": "django.core.files.storage.FileSystemStorage",
    # },
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME"),
            "region_name": os.getenv("AWS_S3_REGION_NAME"),
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "querystring_auth": False,
            "custom_domain": os.getenv("AWS_S3_CUSTOM_DOMAIN"),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WAGTAILADMIN_BASE_URL = "http://localhost:8080"
