from datetime import datetime

import httpx
from django.core.cache import cache
from django.utils.timezone import make_aware

from notcms.music.models import LastfmSettings
from notcms.music.schemas import LastfmTrack

GET_LAST_PLAYED_CACHE_KEY = "music_lastfm_get_last_played"


class LastfmAPI:
    @property
    def settings(self):
        return LastfmSettings.load()

    @property
    def api_url(self):
        return "https://ws.audioscrobbler.com/2.0/"

    @property
    def api_key(self):
        return self.settings.api_key

    @property
    def api_secret(self):
        return self.settings.api_secret

    @property
    def username(self):
        return self.settings.username

    def get_last_played_cached(self):
        data = cache.get(GET_LAST_PLAYED_CACHE_KEY)
        if data is None:
            return None
        return LastfmTrack(**data)

    def get_last_played(self):
        # Get the recent tracks from Last.fm API
        params = {
            "method": "user.getrecenttracks",
            "user": self.username,
            "limit": 1,
            "api_key": self.api_key,
            "format": "json",
        }

        try:
            r = httpx.get(self.api_url, params=params)
        except Exception:
            # TODO log the error here maybe
            return None

        # Returning None doesn't put the response in the cache
        if r.status_code != 200:
            return None

        data = r.json()
        track = data["recenttracks"]["track"][0]

        # Extract necessary info
        now_playing = False
        if track.get("@attr", {}).get("nowplaying", "") == "true":
            now_playing = True
        scrobbled_at = None
        if not now_playing:
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
            now_playing=now_playing,
        )


lastfm_api = LastfmAPI()
