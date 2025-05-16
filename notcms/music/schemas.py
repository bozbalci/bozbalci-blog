from datetime import datetime

from ninja import ModelSchema, Schema
from pydantic import Field
from wagtail.images.models import AbstractRendition

from notcms.blog.schemas import RenditionSchema
from notcms.music.models import AlbumPage


class LastfmTrack(Schema):
    artist: str
    title: str
    lastfm_url: str
    image_url: str
    scrobbled_at: datetime | None
    now_playing: bool


class AlbumSchema(ModelSchema):
    url: str = Field(default=None, alias="get_full_url")
    cover_image: RenditionSchema | None

    @staticmethod
    def resolve_cover_image(page: AlbumPage) -> AbstractRendition | None:
        if image := page.cover_image:
            return image.get_rendition("original")
        return None

    class Config:
        model = AlbumPage
        model_fields = [
            "slug",
            "title",
            "artist",
            "year",
            "openscrobbler_url",
            "discogs_url",
            "rating",
            "review",
        ]
