from datetime import datetime

from ninja import ModelSchema, Schema
from pydantic import Field
from wagtail.images.models import AbstractRendition

from notcms.blog.schemas import RenditionSchema
from notcms.photo.models import PhotoAlbumPage, PhotoPage


class PhotoAlbumSchema(ModelSchema):
    class Config:
        model = PhotoAlbumPage
        model_fields = ["slug", "title", "description"]

    url: str = Field(default=None, alias="get_full_url")


class ExifSchema(Schema):
    make: str
    model: str
    lens: str
    focal_length: str
    aperture: str
    shutter_speed: str
    iso: str
    shot_at: datetime


class PhotoSchema(ModelSchema):
    class Config:
        model = PhotoPage
        model_fields = ["slug", "title", "caption"]

    uploaded_at: datetime = Field(None, alias="first_published_at")
    albums: list[str]
    exif: ExifSchema | None
    url: str = Field(default=None, alias="get_full_url")
    images: list[RenditionSchema] = []

    @staticmethod
    def resolve_images(photo: PhotoPage) -> list[AbstractRendition]:
        filters = ["original", "fill-600x600"]
        if image := photo.image:
            return image.get_renditions(*filters).values()

    @staticmethod
    def resolve_exif(photo: PhotoPage):
        if photo.exif_make:
            return ExifSchema(
                make=photo.exif_make,
                model=photo.exif_model,
                lens=photo.exif_lens,
                focal_length=photo.exif_focal_length,
                aperture=photo.exif_aperture,
                shutter_speed=photo.exif_shutter_speed,
                iso=photo.exif_iso,
                shot_at=photo.exif_shot_at,
            )
        return None

    @staticmethod
    def resolve_albums(photo: PhotoPage):
        return photo.albums.values_list("slug", flat=True)
