from django.urls import path

from notcms.music.api.views import GetLastPlayedTrackView

urlpatterns = [
    path("last-played/", GetLastPlayedTrackView.as_view(), name="last-played"),
]
