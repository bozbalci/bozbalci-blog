from threading import local

from django import template
from django.utils.safestring import mark_safe
from django_vite.templatetags.django_vite import (
    vite_asset,
    vite_asset_url,
    vite_hmr_client,
)

register = template.Library()


_script_state = local()
_script_state.enqueued = set()


@register.simple_tag
@mark_safe
def enqueue_style(path):
    asset_url = vite_asset_url(f"notcms/static/css/{path}")
    return f'<link rel="stylesheet" type="text/css" href="{asset_url}">'


@register.simple_tag
def enqueue_script(script_name):
    if not hasattr(_script_state, "enqueued"):
        _script_state.enqueued = set()
    _script_state.enqueued.add(script_name)
    return ""


@register.simple_tag
def enqueue_hmr_client():
    return vite_hmr_client()


@register.simple_tag
def render_enqueued_scripts():
    if not hasattr(_script_state, "enqueued"):
        return ""
    tags = []
    for name in _script_state.enqueued:
        tags.append(vite_asset(f"notcms/static/js/{name}/app.js"))
    _script_state.enqueued.clear()
    return mark_safe("\n".join(tags))
