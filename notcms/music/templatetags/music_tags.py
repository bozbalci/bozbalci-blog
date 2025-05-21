import math

from django import template

from notcms.music.lastfm import lastfm_api

register = template.Library()


@register.simple_tag
def get_last_played():
    return lastfm_api.get_last_played_cached()


@register.inclusion_tag("music/partials/stars.html")
def stars(value: int):
    scaled_value = round(value / 2, 1)
    total_stars = 5
    full_stars = math.floor(scaled_value)
    has_half_star = (scaled_value % 1) != 0
    empty_stars = total_stars - full_stars - has_half_star

    return {
        "full_stars": range(full_stars),
        "has_half_star": has_half_star,
        "empty_stars": range(empty_stars),
        "scaled_value": scaled_value,
        "total_stars": total_stars,
    }
