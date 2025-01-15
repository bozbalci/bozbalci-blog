import os
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SITE_ID = 1

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third-party apps
    "debug_toolbar",
    "corsheaders",
    "django_vite",
    # NotCMS apps
    "notcms.core",
    "notcms.blog",
    "notcms.photo",
    "notcms.music",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "notcms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notcms.blog.context_processors.naked_css",
                "notcms.music.context_processors.last_played",
            ],
        },
    },
]

WSGI_APPLICATION = "notcms.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LASTFM = {
    "api_key": os.getenv("LASTFM_API_KEY"),
    "secret": os.getenv("LASTFM_API_SECRET"),
    "username": os.getenv("LASTFM_USERNAME"),
}

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
STATICFILES_DIRS = (BASE_DIR / "static" / "assets", BASE_DIR / "static" / "dist")


# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_IMMUTABLE_FILE_TEST


def immutable_file_test(path, url):
    # Match vite (rollup)-generated hashes, à la, `some_file-CSliV9zW.js`
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
