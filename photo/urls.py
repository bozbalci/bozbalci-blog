from django.urls import path

from . import views

app_name = "photo"

urlpatterns = [
    path("", views.gallery_index, name="index"),
    path("album/<slug>/", views.gallery_album, name="album"),
    path("photo/<int:pk>/", views.gallery_photo_details, name="details"),
]
