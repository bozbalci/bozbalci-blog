from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_footnotes import urls as footnotes_urls

from notcms.blog.feeds import BlogFeed
from notcms.toys import urls as toys_urls

from .api import api

urlpatterns = (
    [
        path("toys/", include(toys_urls)),
        path("blog/feed/", BlogFeed(), name="feed"),
        path("api/v2/", api.urls),
        path(settings.ADMIN_URL, admin.site.urls),
        path("cms/", include(wagtailadmin_urls)),
        path("documents/", include(wagtaildocs_urls)),
        # Admin-only URL, required for wagtail_footnotes
        path("footnotes/", include(footnotes_urls)),
        path("sitemap.xml", sitemap),
        path(
            "robots.txt",
            TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
    + [
        # All other URLs route to Wagtail
        re_path(r"^", include(wagtail_urls)),
    ]
)
