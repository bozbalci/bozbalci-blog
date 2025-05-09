import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

import notcms.blog.views as blog_views

api = NinjaAPI()

api.add_router("/photos/", "notcms.photo.api.router")
api.add_router("/music/", "notcms.music.api.router")

urlpatterns = [
    path("tapen/", admin.site.urls),
    path("api/", api.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    # TODO debug
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = blog_views.handler400
handler403 = blog_views.handler403
handler404 = blog_views.handler404
handler500 = blog_views.handler500
