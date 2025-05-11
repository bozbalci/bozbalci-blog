from datetime import datetime

import exifread
from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.images.models import Image
from wagtail.models import Page


def get_fractional_value(formatted: str) -> float:
    if "/" in formatted:
        numerator, denominator = map(float, formatted.split("/"))
        return numerator / denominator
    return float(formatted)


def get_sidebar_navigation_context():
    return {
        "gallery_index": PhotoGalleryIndexPage.objects.first(),
        "albums": PhotoAlbumPage.objects.order_by("title"),
    }


class PhotoGalleryIndexPage(RoutablePageMixin, Page):
    subpage_types = ["PhotoPage", "PhotoAlbumPage"]
    template = "photo/gallery.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "photos": PhotoPage.objects.live()
            .select_related("image")
            .order_by("-first_published_at"),
            **get_sidebar_navigation_context(),
        }


class PhotoPage(Page):
    caption = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    albums = ParentalManyToManyField(
        "photo.PhotoAlbumPage", related_name="photos", blank=True
    )
    exif_make = models.CharField(max_length=255, blank=True)
    exif_model = models.CharField(max_length=255, blank=True)
    exif_lens = models.CharField(max_length=255, blank=True)
    exif_focal_length = models.CharField(max_length=255, blank=True)
    exif_aperture = models.CharField(max_length=255, blank=True)
    exif_shutter_speed = models.CharField(max_length=255, blank=True)
    exif_iso = models.CharField(max_length=255, blank=True)
    exif_shot_at = models.DateTimeField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("image"),
        FieldPanel("albums", widget=forms.CheckboxSelectMultiple),
    ]

    parent_page_types = ["PhotoGalleryIndexPage"]
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {**context, **get_sidebar_navigation_context()}

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


class PhotoAlbumPage(Page):
    description = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    parent_page_types = ["PhotoGalleryIndexPage"]
    subpage_types = []
    template = "photo/gallery.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "photos": PhotoPage.objects.live()
            .select_related("image")
            .filter(albums=self)
            .order_by("-first_published_at"),
            **get_sidebar_navigation_context(),
        }
