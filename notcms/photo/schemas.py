from ninja import ModelSchema

from notcms.photo.models import Photo, PhotoAlbum


class PhotoAlbumSchema(ModelSchema):
    class Meta:
        model = PhotoAlbum
        fields = [
            "name",
            "slug",
        ]


class PhotoSchema(ModelSchema):
    image_url: str | None = None
    thumbnail_url: str | None = None
    albums: list[PhotoAlbumSchema] | None = []

    @staticmethod
    def resolve_image_url(obj: Photo):
        return obj.image_url

    @staticmethod
    def resolve_thumbnail_url(obj: Photo):
        return obj.thumbnail_url

    @staticmethod
    def resolve_albums(obj: Photo):
        return obj.albums.all()

    class Meta:
        model = Photo
        fields = [
            "id",
            "title",
            "exif",
            "uploaded_at",
        ]
