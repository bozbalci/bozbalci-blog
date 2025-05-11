from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_footnotes import urls as footnotes_urls

# from notcms.blog.feeds import BlogFeed
from notcms.toys import urls as toys_urls

urlpatterns = (
    [
        # Public URLs
        path("toys/", include(toys_urls)),
        # path("feed/", BlogFeed(), name="feed"),
        # Misc. URLs
        path("tapen/", admin.site.urls),
        path("api/v2/", include("notcms.api_urls")),
        # Wagtail URLs
        path("cms/", include(wagtailadmin_urls)),
        path("documents/", include(wagtaildocs_urls)),
        # Admin-only URL, required for wagtail_footnotes
        path("footnotes/", include(footnotes_urls)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
    + [
        # All other URLs route to Wagtail
        re_path(r"^", include(wagtail_urls)),
    ]
)
