from dataclasses import dataclass
from datetime import datetime
from functools import wraps

import httpx
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import make_aware

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


@dataclass
class LastfmTrack:
    artist: str
    title: str
    lastfm_url: str
    image_url: str
    scrobbled_at: datetime


class LastfmAPI:
    def __init__(self):
        self.api_key = settings.LASTFM["api_key"]
        self.api_secret = settings.LASTFM["secret"]
        self.username = settings.LASTFM["username"]

    @cache_response("lastfm_last_played", timeout=180)
    def get_last_played(self):
        # Get the recent tracks from Last.fm API
        params = {
            "method": "user.getrecenttracks",
            "user": self.username,
            "limit": 1,
            "api_key": self.api_key,
            "format": "json",
        }
        r = httpx.get(API_URL, params=params)
        data = r.json()
        track = data["recenttracks"]["track"][0]

        # Extract necessary info
        scrobble_timestamp = int(track["date"]["uts"])
        scrobbled_at = make_aware(datetime.fromtimestamp(scrobble_timestamp))
        image_url = None
        for item in track["image"]:
            if item.get("size") == "small":
                image_url = item.get("#text")
                break

        return LastfmTrack(
            artist=track["artist"]["#text"],
            title=track["name"],
            lastfm_url=track["url"],
            image_url=image_url,
            scrobbled_at=scrobbled_at,
        )


lastfm_api = LastfmAPI()
