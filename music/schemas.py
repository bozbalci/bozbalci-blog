from datetime import datetime
from typing import Optional

from ninja import ModelSchema, Schema

from music.models import Album


class LastfmTrack(Schema):
    artist: str
    title: str
    lastfm_url: str
    image_url: str
    scrobbled_at: Optional[datetime]
    now_playing: bool


class AlbumSchema(ModelSchema):
    cover_image_url: Optional[str] = None

    @staticmethod
    def resolve_cover_image_url(obj):
        return obj.cover_image.original.url

    class Meta:
        model = Album
        fields = [
            "id",
            "title",
            "artist",
            "slug",
            "year",
            "rating",
            "openscrobbler_url",
            "discogs_url",
            "review",
            "tags",
        ]
