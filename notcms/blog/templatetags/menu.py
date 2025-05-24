from django import template
from django.db.models import Prefetch
from wagtail.models import Locale

from notcms.blog.models import Menu, MenuItem

register = template.Library()


@register.simple_tag
def get_menu(key):
    # cache_key = f"blog_menu_{key}"

    def fetch_menu_items():
        try:
            menu = Menu.objects.prefetch_related(
                Prefetch(
                    "items",
                    queryset=MenuItem.objects.select_related("link_page").order_by(
                        "sort_order"
                    ),
                )
            ).get(key=key, locale=Locale.get_active())
            return list(menu.items.all())
        except Menu.DoesNotExist:
            return None

    # return cache.get_or_set(cache_key, fetch_menu_items, timeout=60 * 10)

    return fetch_menu_items()


@register.inclusion_tag("partials/footer_menu.html")
def render_footer_menu(key):
    return {
        "menu": get_menu(key),
    }
