from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail_footnotes import urls as footnotes_urls

from notcms.blog.feeds import BlogFeed
from notcms.toys import urls as toys_urls

from .api import api

urlpatterns = [
    path("blog/feed/", BlogFeed(), name="feed"),
    path("api/v2/", api.urls),
    path(settings.ADMIN_URL, admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("footnotes/", include(footnotes_urls)),  # Admin-only
    path("i18n/", include("django.conf.urls.i18n")),
    path("sitemap.xml", sitemap),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad request")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Not found")},
        ),
        path("500/", default_views.server_error),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns = [*debug_toolbar_urls(), *urlpatterns]


def get_jsi18n_version():
    return "20250524-v2"


urlpatterns += i18n_patterns(
    path("toys/", include(toys_urls)),
    path(
        "jsi18n/",
        cache_page(86400, key_prefix=f"jsi18n-{get_jsi18n_version()}")(
            JavaScriptCatalog.as_view()
        ),
        name="javascript-catalog",
    ),
    re_path(r"^", include(wagtail_urls)),
    prefix_default_language=False,
)
