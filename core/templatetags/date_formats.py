from datetime import datetime

from django import template
from django.template.defaultfilters import date

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
