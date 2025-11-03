from datetime import datetime

import exifread
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.models import Page


def get_fractional_value(formatted: str) -> float:
    if "/" in formatted:
        numerator, denominator = map(float, formatted.split("/"))
        return numerator / denominator
    return float(formatted)


def get_sidebar_navigation_context(request, current_album=None):
    return {
        "gallery_index": PhotoGalleryIndexPage.objects.live().get(
            locale=request.locale,
        ),
        "albums": PhotoAlbumPage.objects.live()
        .filter(locale=request.locale, view_restrictions__isnull=True)
        .order_by("title"),
        "current_album": current_album,
    }


class PhotoGalleryIndexPage(Page):
    subpage_types = ["PhotoPage", "PhotoAlbumsIndexPage"]
    template = "photo/gallery.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "photos": PhotoPage.objects.live()
            .filter(locale=request.locale, include_in_camera_roll=True)
            .select_related("image")
            .order_by("-first_published_at"),
            **get_sidebar_navigation_context(request),
        }


# This needs to exist for now because it's mentioned in a migration.
def limit_photo_page_album_choices():
    return models.Q(locale__id="1")


class PhotoPage(Page):
    caption = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    exif_make = models.CharField(max_length=255, blank=True)
    exif_model = models.CharField(max_length=255, blank=True)
    exif_lens = models.CharField(max_length=255, blank=True)
    exif_focal_length = models.CharField(max_length=255, blank=True)
    exif_aperture = models.CharField(max_length=255, blank=True)
    exif_shutter_speed = models.CharField(max_length=255, blank=True)
    exif_iso = models.CharField(max_length=255, blank=True)
    exif_shot_at = models.DateTimeField(blank=True, null=True)
    include_in_camera_roll = models.BooleanField(null=False, blank=False, default=True)

    content_panels = Page.content_panels + [
        FieldPanel("caption"),
        FieldPanel("image"),
        FieldPanel("include_in_camera_roll"),
    ]

    parent_page_types = ["PhotoGalleryIndexPage", "PhotoAlbumPage"]
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        if isinstance(self.get_parent().specific, PhotoAlbumPage):
            current_album = self.get_parent().specific
        else:
            current_album = None

        return {
            **context,
            **get_sidebar_navigation_context(request, current_album),
        }

    def extract_exif(self):
        image_file = self.image.file
        image_file.seek(0)
        exif = {
            key: str(value) for key, value in exifread.process_file(image_file).items()
        }

        # These fields don't need formatting:
        self.exif_make = exif.get("Image Make", "")
        self.exif_model = exif.get("Image Model", "")
        self.exif_lens = exif.get("EXIF LensModel", "")
        self.exif_iso = exif.get("EXIF ISOSpeedRatings", "")

        exif_focal_length = exif.get("EXIF FocalLength", "")
        if exif_focal_length:
            focal_length_value = get_fractional_value(exif_focal_length)
            self.exif_focal_length = f"{round(focal_length_value, 0)}mm"

        exif_aperture = exif.get("EXIF ApertureValue", "")
        if exif_aperture:
            aperture_value = get_fractional_value(exif_aperture)
            self.exif_aperture = f"{round(aperture_value, 1)}"

        exif_shutter_speed = exif.get("EXIF ExposureTime", "")
        if exif_shutter_speed:
            shutter_speed_value = get_fractional_value(exif_shutter_speed)
            if (1 / shutter_speed_value) > 1:
                self.exif_shutter_speed = f"1/{int(1 / shutter_speed_value)}"
            else:
                self.exif_shutter_speed = f"{shutter_speed_value:.2f} sec"

        exif_shot_at = exif.get("EXIF DateTimeOriginal", "")
        if exif_shot_at:
            self.exif_shot_at = datetime.strptime(exif_shot_at, "%Y:%m:%d %H:%M:%S")

    def save(self, *args, **kwargs):
        if self.image.file and not self.exif_make:
            self.extract_exif()
        super().save(*args, **kwargs)


class PhotoAlbumsIndexPage(Page):
    parent_page_types = ["PhotoGalleryIndexPage"]
    subpage_types = ["PhotoAlbumPage"]
    template = "photo/albums_index.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            **get_sidebar_navigation_context(request),
        }


class PhotoAlbumPage(Page):
    description = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    parent_page_types = ["PhotoAlbumsIndexPage"]
    subpage_types = ["PhotoPage"]
    template = "photo/gallery.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            **get_sidebar_navigation_context(request),
            "photos": self.get_children().live().select_related("image").specific,
        }

    @property
    def cover_image(self):
        children = self.get_children()
        if children:
            return children.first().specific.image
        else:
            return None
