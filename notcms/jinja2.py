from django.contrib.humanize.templatetags.humanize import naturaltime
from django.templatetags.static import static
from django.urls import reverse


from django_vite.templatetags.django_vite import (
    vite_asset,
    vite_asset_url,
    vite_hmr_client,
    vite_legacy_asset,
    vite_legacy_polyfills,
    vite_preload_asset,
    vite_react_refresh,
)

from jinja2 import Environment

from notcms.core import templatetags as core_tags
from notcms.music import templatetags as music_tags
from notcms.photo import templatetags as photo_tags


def environment(**options):
    env = Environment(**options)

    env.globals.update(
        {
            "static": static,
            "url": reverse,
            # Vite
            "vite_asset": vite_asset,
            "vite_asset_url": vite_asset_url,
            "vite_hmr_client": vite_hmr_client,
            "vite_legacy_asset": vite_legacy_asset,
            "vite_legacy_polyfills": vite_legacy_polyfills,
            "vite_preload_asset": vite_preload_asset,
            "vite_react_refresh": vite_react_refresh,
            # Core
            "now": core_tags.now,
        }
    )

    env.filters.update(
        {
            "naturaltime": naturaltime,
            # Core
            "format_date": core_tags.format_date,
            "format_iso_date": core_tags.format_iso_date,
            "render_markdown": core_tags.render_markdown,
            # Music
            "stars": music_tags.stars,
            # Photo
            "lg_caption": photo_tags.lg_caption,
        }
    )

    return env
