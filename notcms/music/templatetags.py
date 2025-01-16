import math

from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from notcms.core.constants import SiteFeature
from notcms.core.helpers import is_feature_enabled

register = template.Library()


@register.filter
def stars(value: int):
    scaled_value = round(value / 2, 1)
    total_stars = 5
    full_stars = math.floor(scaled_value)
    has_half_star = (scaled_value % 1) != 0
    empty_stars = total_stars - full_stars - has_half_star

    return mark_safe(
        render_to_string(
            "music/partials/stars.html",
            {
                "full_stars": range(full_stars),
                "has_half_star": has_half_star,
                "empty_stars": range(empty_stars),
                "scaled_value": scaled_value,
                "total_stars": total_stars,
            },
        )
    )


def get_last_played(request):
    from .lastfm import lastfm_api

    if is_feature_enabled(SiteFeature.LAST_PLAYED):
        return lastfm_api.get_last_played()
    return None
