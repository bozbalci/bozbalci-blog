from django.urls import path

from . import views

app_name = "music"

urlpatterns = [
    path("", views.index, name="index"),
    path("all-time/", views.all_time_favourites, name="all-time"),
    path("2024/", views.year_2024, name="year-2024"),
    path("shuffled/", views.shuffled, name="shuffled"),
    path("album/<slug>/", views.single_album_details, name="album"),
]
