from datetime import datetime, timedelta

from django.core.cache import cache

from notcms.blog.models import FooterText, Menu
from notcms.core.helpers import cache_response


@cache_response("is_naked_day", timeout=3600)
def is_naked_day(month=4, day=9):
    current_year = datetime.now().year
    base_time = datetime(current_year, month, day)
    start = (base_time + timedelta(hours=-14)).timestamp()
    end = (base_time + timedelta(hours=36)).timestamp()
    now = datetime.now().timestamp()
    return start <= now <= end


def naked_css(request):
    """
    https://css-naked-day.github.io/

    April 9 is CSS Naked Day. This context processor sets a flag
    that can be used in templates to disable loading CSS.
    """

    if "nocss" in request.GET:
        request.session["nocss"] = True
    elif "css" in request.GET:
        request.session.pop("nocss", None)

    no_css = request.session.get("nocss", False) or is_naked_day()
    return no_css


def get_menu(key):
    cache_key = f"blog_menu:{key}"
    menu = cache.get(cache_key)
    if not menu:
        try:
            menu = Menu.objects.prefetch_related("items").get(key=key)
            cache.set(cache_key, menu, timeout=3600)
        except Menu.DoesNotExist:
            return None
    return menu.items.all()


def get_footer_text():
    instance = FooterText.objects.filter(live=True).first()

    return instance.body if instance else ""
