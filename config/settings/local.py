# ruff: noqa: F405
from .base import *  # noqa: F403

# -----------------------------------------------------------------------------
# GENERAL
# -----------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="ueRDZfmjHYBfht1zFr8kzDBgLrxuBk0oMIxiGOOv2ctQqg7SdjDzNbpBrStBqa63",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# -----------------------------------------------------------------------------
# Storages
# -----------------------------------------------------------------------------
STORAGES["default"] = {
    "BACKEND": "django.core.files.storage.FileSystemStorage",
}

# -----------------------------------------------------------------------------
# django-debug-toolbar
# -----------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # Disable the profiling panel due to an issue with Python 3.12:
        # https://github.com/jazzband/django-debug-toolbar/issues/1875
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1"]
if env.bool("USE_DOCKER", default=False):
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
    try:
        _, _, ips = socket.gethostbyname_ex("node")
        INTERNAL_IPS.extend(ips)
    except socket.gaierror:
        # The node container isn't started (yet?)
        pass


# -----------------------------------------------------------------------------
# Wagtail
# -----------------------------------------------------------------------------
WAGTAILADMIN_BASE_URL = "http://localhost:8080"

# -----------------------------------------------------------------------------
# Whitenoise
# -----------------------------------------------------------------------------
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------
CELERY_TASK_EAGER_PROPAGATES = True

# -----------------------------------------------------------------------------
# Vite
# -----------------------------------------------------------------------------
DJANGO_VITE = {
    "default": {
        "dev_mode": True,
        "dev_server_host": "localhost",
    }
}
