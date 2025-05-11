from django.urls import include, path

from notcms.music.api import urls as music_api_urls

from .api import api_router

urlpatterns = [
    path("wagtail/", api_router.urls),
    path("music/", include(music_api_urls)),
]
