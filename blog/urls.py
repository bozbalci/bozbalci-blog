from django.urls import path

import blog.feeds
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/<slug>/", views.post, name="post"),
    path("feed/", blog.feeds.BlogFeed(), name="feed"),
]
