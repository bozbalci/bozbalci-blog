from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI

import notcms.blog.views as blog_views
from notcms.blog.views import custom_flatpage


api = NinjaAPI()

api.add_router("/photos/", "notcms.photo.api.router")
api.add_router("/music/", "notcms.music.api.router")

urlpatterns = (
    [
        path("", blog_views.home, name="home"),
        # Flat pages
        path("about/", custom_flatpage, {"url": "/about/"}, name="about"),
        path("colophon/", custom_flatpage, {"url": "/colophon/"}, name="colophon"),
        path("contact/", custom_flatpage, {"url": "/contact/"}, name="contact"),
        path("social/", custom_flatpage, {"url": "/social/"}, name="social"),
        # Special cases
        path("now/", blog_views.now, name="now"),
        path("then/", blog_views.then, name="then"),
        # Apps
        path("blog/", include("notcms.blog.urls", namespace="blog")),
        path("gallery/", include("notcms.photo.urls", namespace="photo")),
        path("music-collection/", include("notcms.music.urls", namespace="music")),
        # Uncomment to test error pages on local
        # path("400/", lambda r: blog_views.handler400(r, None)),
        # path("403/", lambda r: blog_views.handler403(r, None)),
        # path("404/", lambda r: blog_views.handler404(r, None)),
        # path("500/", blog_views.handler500),
        path("tapen/", admin.site.urls),
        path("api/", api.urls),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

handler400 = blog_views.handler400
handler403 = blog_views.handler403
handler404 = blog_views.handler404
handler500 = blog_views.handler500
