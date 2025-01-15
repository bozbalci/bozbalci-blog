from datetime import datetime

from ninja import ModelSchema, Schema

from notcms.music.models import Album


class LastfmTrack(Schema):
    artist: str
    title: str
    lastfm_url: str
    image_url: str
    scrobbled_at: datetime | None
    now_playing: bool


class AlbumSchema(ModelSchema):
    cover_image_url: str | None = None

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
