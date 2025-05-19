from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .lastfm import GET_LAST_PLAYED_CACHE_KEY
from .models import LastfmSettings


@receiver(post_save, sender=LastfmSettings)
def clear_lastfm_cache_on_settings_update(sender, instance, **kwargs):
    cache.delete(GET_LAST_PLAYED_CACHE_KEY)
