from django.urls import path

from notcms.blog import views, feeds

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/<slug>/", views.post, name="post"),
    path("feed/", feeds.BlogFeed(), name="feed"),
]
