from django.db import models

from notcms.core.models import Category, ImageUpload, Tag


class PhotoAlbum(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.OneToOneField(
        ImageUpload, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(
        max_length=255, blank=True, help_text="Optional title for the photo."
    )
    exif = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(PhotoAlbum, blank=True)

    def __str__(self):
        return self.title or f"Photo {self.id}"

    @property
    def image_url(self):
        return self.image.original.url

    @property
    def thumbnail_url(self):
        return self.image.thumbnail.url
