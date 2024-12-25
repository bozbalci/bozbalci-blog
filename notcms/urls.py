from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, re_path, include
from ninja import NinjaAPI

import blog.views as blog_views
from blog.views import custom_flatpage

api = NinjaAPI()

api.add_router("/photos/", "photo.api.router")
api.add_router("/music/", "music.api.router")
urlpatterns = [
    re_path(r"^$", blog_views.index),
    path("about/", custom_flatpage, {"url": "/about/"}, name="about"),
    path("colophon/", custom_flatpage, {"url": "/colophon/"}, name="colophon"),
    path("contact/", custom_flatpage, {"url": "/contact/"}, name="contact"),
    path("now/", custom_flatpage, {"url": "/now/"}, name="now"),
    path("gallery/", include("photo.urls", namespace="photo")),
    path("music-collection/", include("music.urls", namespace="music")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + debug_toolbar_urls()
