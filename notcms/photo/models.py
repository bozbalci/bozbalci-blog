import exifread
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.images.models import Image
from wagtail.models import Page

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


class PhotoGalleryIndexPage(RoutablePageMixin, Page):
    subpage_types = ["PhotoPage"]
    template = "photo/index.html"

    def get_context(self, request, *args, **kwargs):
        return {
            "gallery_index": self,
            "photos": PhotoPage.objects.all(),
        }


class PhotoPage(Page):
    caption = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=False)
    exif = models.JSONField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("image"),
    ]

    def extract_exif(self):
        image_file = self.image.file

        if not image_file:
            return

        image_file.seek(0)
        exif_data = exifread.process_file(image_file)
        from notcms.photo.helpers import filter_exif

        self.exif = filter_exif({k: str(v) for k, v in exif_data.items()})

    def save(self, *args, **kwargs):
        self.extract_exif()
        super().save(*args, **kwargs)
