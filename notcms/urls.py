from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/photos/", "photo.api.router")
api.add_router("/music/", "music.api.router")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
