from functools import wraps

import httpx
from django.conf import settings
from django.core.cache import cache

API_URL = "https://ws.audioscrobbler.com/2.0/"


def cache_response(cache_key, timeout):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper

    return decorator


class LastfmAPI:
    def __init__(self):
        self.api_key = settings.LASTFM["api_key"]
        self.api_secret = settings.LASTFM["secret"]
        self.username = settings.LASTFM["username"]

    @cache_response("lastfm_recent_tracks", timeout=180)
    def get_recent_tracks(self):
        params = {
            "method": "user.getrecenttracks",
            "user": self.username,
            "limit": 1,
            "api_key": self.api_key,
            "format": "json",
        }

        r = httpx.get(API_URL, params=params)
        return r.json()
