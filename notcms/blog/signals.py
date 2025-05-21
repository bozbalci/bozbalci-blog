from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from notcms.blog.models import Menu, MenuItem


@receiver([post_save, post_delete], sender=Menu)
def clear_menu_cache(sender, instance: Menu, **kwargs):
    cache_key = f"blog_menu_{instance.key}"
    cache.delete(cache_key)


@receiver([post_save, post_delete], sender=MenuItem)
def clear_menu_item_cache(sender, instance: MenuItem, **kwargs):
    if instance.menu:
        cache_key = f"blog_menu_${instance.menu.key}"
        cache.delete(cache_key)
