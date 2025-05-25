from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from notcms.blog.models import FooterText, Menu, MenuItem, NowPostPreamble


@receiver([post_save, post_delete], sender=Menu)
def clear_menu_cache(sender, instance: Menu, **kwargs):
    cache_key = f"blog_menu-{instance.key}-{instance.locale.language_code}"
    cache.delete(cache_key)


@receiver([post_save, post_delete], sender=MenuItem)
def clear_menu_item_cache(sender, instance: MenuItem, **kwargs):
    if instance.menu:
        cache_key = (
            f"blog_menu-{instance.menu.key}-{instance.menu.locale.language_code}"
        )
        cache.delete(cache_key)


@receiver([post_save, post_delete], sender=FooterText)
def clear_footer_text_cache(sender, instance: FooterText, **kwargs):
    cache_key = f"blog_footer_text-{instance.locale.language_code}"
    cache.delete(cache_key)


@receiver([post_save, post_delete], sender=NowPostPreamble)
def clear_now_post_preamble_cache(sender, instance: NowPostPreamble, **kwargs):
    cache_key = f"blog_now_post_preamble-{instance.locale.language_code}"
    cache.delete(cache_key)
