from datetime import datetime, timedelta

from django.core.cache import cache

from notcms.blog.models import HomePage


def is_naked_day(month=4, day=9):
    cached = cache.get("is_naked_day", None)
    if cached is not None:
        return cached
    current_time = datetime.now()
    base = datetime(current_time.year, month, day)
    start = base - timedelta(hours=14)
    end = base + timedelta(hours=36)
    result = start <= current_time <= end
    cache.set("is_naked_day", result, timeout=60 * 10)
    return result


def is_naked_css(request):
    """
    https://css-naked-day.github.io/

    April 9 is CSS Naked Day. This context processor sets a flag
    that can be used in templates to disable loading CSS.
    """
    if not request:
        return False

    if "css" in request.GET:
        request.session["nocss"] = False
    elif "nocss" in request.GET:
        request.session["nocss"] = True

    if "nocss" in request.session:
        return request.session["nocss"]
    else:
        return is_naked_day()


def notcms_globals(request):
    return {
        "home": HomePage.objects.live().filter(locale=request.locale).first(),
        "no_css": is_naked_css(request),
    }
