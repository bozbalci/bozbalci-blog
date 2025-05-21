from django import template
from django.utils.safestring import mark_safe
from django_vite.templatetags.django_vite import (
    vite_asset,
    vite_asset_url,
    vite_hmr_client,
)

register = template.Library()


@register.simple_tag
@mark_safe
def enqueue_style(path):
    asset_url = vite_asset_url(f"notcms/static/css/{path}")
    return f'<link rel="stylesheet" type="text/css" href="{asset_url}">'


@register.simple_tag
def enqueue_script(path):
    return vite_asset(f"notcms/static/js/{path}/app.js")


@register.simple_tag
def enqueue_hmr_client():
    return vite_hmr_client()
