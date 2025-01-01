from datetime import datetime

import httpx
from django.conf import settings
from django.utils.timezone import make_aware

from notcms.core.helpers import cache_response
from notcms.music.schemas import LastfmTrack

API_URL = "https://ws.audioscrobbler.com/2.0/"


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
