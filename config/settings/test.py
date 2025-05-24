from .base import *  # noqa: F403
from .base import STORAGES, TEMPLATES, env

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="!!!SET DJANGO_SECRET_KEY!!!",
)

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

STORAGES["default"] = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
}

DJANGO_VITE = {
    "default": {
        "dev_mode": True,
    }
}
