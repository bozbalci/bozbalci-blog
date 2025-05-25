from datetime import date, datetime

from django import template
from django.utils.formats import date_format

ISO_DATE_FMT = "c"


register = template.Library()


def coerce_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    if isinstance(obj, date):
        return datetime.combine(obj, datetime.min.time())
    elif isinstance(obj, str):
        # Assume ISO format
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return None
    return None


@register.filter
def format_date(obj):
    obj = coerce_datetime(obj)
    if not obj:
        return ""
    return date_format(obj, format="DATE_FORMAT", use_l10n=True)


@register.filter
def format_iso_date(obj):
    obj = coerce_datetime(obj)
    if not obj:
        return ""
    return date_format(obj, format=ISO_DATE_FMT)
