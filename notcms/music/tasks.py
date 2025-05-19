from celery import shared_task
from django.core.cache import cache

from notcms.music.lastfm import GET_LAST_PLAYED_CACHE_KEY, lastfm_api


@shared_task
def update_last_played_track():
    track = lastfm_api.get_last_played()

    if track is not None:
        cache.set(GET_LAST_PLAYED_CACHE_KEY, track.dict(), timeout=None)
