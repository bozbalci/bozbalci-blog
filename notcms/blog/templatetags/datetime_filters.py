from datetime import date as dt_date
from datetime import datetime

from django import template
from django.conf import settings
from django.template.defaultfilters import date
from django.utils.formats import date_format
from django.utils.timezone import get_current_timezone

DATE_FMT = "F j, Y"
ISO_DATE_FMT = "c"


register = template.Library()


def coerce_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    if isinstance(obj, dt_date):
        return datetime.combine(obj, datetime.min.time())
    elif isinstance(obj, str):
        # Assume ISO format
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return None
    else:
        return None


@register.filter
def format_date(obj):
    obj = coerce_datetime(obj)
    return date(obj, DATE_FMT)


@register.filter
def format_iso_date(obj):
    obj = coerce_datetime(obj)
    return date(obj, ISO_DATE_FMT)


@register.simple_tag
def now(format_string):
    tzinfo = get_current_timezone() if settings.USE_TZ else None
    cur_datetime = datetime.now(tz=tzinfo)
    return date_format(cur_datetime, format_string)
