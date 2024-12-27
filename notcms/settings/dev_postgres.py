from .dev import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": "localhost",
        "PORT": "",
        "NAME": "notcms",
        "USER": "django_notcms_owner",
        "PASSWORD": "password",
        "CONN_MAX_AGE": 600,
    }
}
