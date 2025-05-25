from django import template
from django.core.cache import cache
from django.db.models import Prefetch

from notcms.blog.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def get_menu(context, key):
    request = context["request"]
    locale = request.locale
    cache_key = f"blog_menu-{key}-{locale.language_code}"

    def fetch_menu_items():
        try:
            menu = Menu.objects.prefetch_related(
                Prefetch(
                    "items",
                    queryset=MenuItem.objects.select_related("link_page").order_by(
                        "sort_order"
                    ),
                )
            ).get(key=key, locale=locale)
            return list(menu.items.all())
        except Menu.DoesNotExist:
            return None

    return cache.get_or_set(cache_key, fetch_menu_items, timeout=60 * 10)


@register.inclusion_tag("partials/footer_menu.html", takes_context=True)
def render_footer_menu(context, key):
    return {
        "menu": get_menu(context, key),
    }
