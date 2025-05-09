from datetime import datetime

from django import template
from django.conf import settings
from django.template.defaultfilters import date
from django.utils.formats import date_format
from django.utils.timezone import get_current_timezone
from jinja2 import pass_context
from wagtail.models import Site

from notcms.core.helpers import markdown

register = template.Library()

DATE_FMT = "F j, Y"
ISO_DATE_FMT = "c"
SNIPPET_CACHE_TTL = 300  # 5 minutes


def coerce_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    elif isinstance(obj, str):
        # Assume ISO format
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return None


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


@pass_context
def routablepageurl(context, page, url_name, *args, **kwargs):
    """
    Adapted from: https://github.com/wagtail/wagtail/blob/main/wagtail/contrib/routable_page/templatetags/wagtailroutablepage_tags.py
    """
    request = context["request"]
    site = Site.find_for_request(request)
    base_url = page.relative_url(site, request)
    routed_url = page.reverse_subpage(url_name, args=args, kwargs=kwargs)
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url + routed_url
