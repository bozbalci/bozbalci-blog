from datetime import datetime

from django import template
from django.conf import settings
from django.core.cache import cache
from django.template import engines
from django.template.defaultfilters import date
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.timezone import get_current_timezone

from notcms.core.helpers import markdown
from notcms.core.models import MarkdownSnippet

register = template.Library()

DATE_FMT = "F j, Y"
ISO_DATE_FMT = "c"
SNIPPET_CACHE_TTL = 300  # 5 minutes


def coerce_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    elif isinstance(obj, str):
        # Assume ISO format
        return datetime.fromisoformat(obj)


@register.filter
def format_date(obj):
    obj = coerce_datetime(obj)
    return date(obj, DATE_FMT)


@register.filter
def format_iso_date(obj):
    obj = coerce_datetime(obj)
    return date(obj, ISO_DATE_FMT)


@register.filter
def render_markdown(text):
    if not text:
        return ""
    return markdown(text)


@register.tag
def now(format_string):
    tzinfo = get_current_timezone() if settings.USE_TZ else None
    cur_datetime = datetime.now(tz=tzinfo)
    return date_format(cur_datetime, format_string)


@register.simple_tag
def get_markdown_snippet(slug):
    """
    Retrieves a MarkdownSnippet, renders it as a Jinja2 template, then
    converts it to HTML. The final output is cached for 5 minutes.
    """
    cache_key = f"markdown_snippet_{slug}"
    cached_content = None  # cache.get(cache_key)

    if cached_content:
        return mark_safe(cached_content)
    try:
        snippet = MarkdownSnippet.objects.get(slug=slug)
        jinja_env = engines["jinja2"]
        rendered_jinja = jinja_env.from_string(snippet.content).render()
        rendered_markdown = markdown(rendered_jinja)
        cache.set(cache_key, rendered_markdown, SNIPPET_CACHE_TTL)
        return mark_safe(rendered_markdown)
    except MarkdownSnippet.DoesNotExist:
        return ""
