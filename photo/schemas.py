from typing import Optional

from ninja import ModelSchema

from photo.models import Photo


class PhotoSchema(ModelSchema):
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    @staticmethod
    def resolve_image_url(obj: Photo):
        return obj.image_url

    @staticmethod
    def resolve_thumbnail_url(obj: Photo):
        return obj.thumbnail_url

    class Meta:
        model = Photo
        fields = [
            "id",
            "title",
            "exif",
            "uploaded_at",
        ]
