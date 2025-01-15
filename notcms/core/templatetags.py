from datetime import datetime

from django import template
from django.conf import settings
from django.template.defaultfilters import date
from django.utils.formats import date_format
from django.utils.timezone import get_current_timezone

from notcms.core.helpers import markdown

register = template.Library()

DATE_FMT = "F j, Y"
ISO_DATE_FMT = "c"


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
