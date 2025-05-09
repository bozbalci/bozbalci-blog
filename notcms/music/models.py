from django.db import models
from django.db.models.functions import Random
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting

from notcms.core.models import ImageUpload, Tag


class AlbumQuerySet(models.QuerySet):
    def get_by_slug(self, slug):
        return self.get(slug=slug)

    def perfect_tens(self):
        return self.filter(rating__isnull=False, rating=10)

    def shuffled(self):
        return self.order_by(Random())


class Album(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.OneToOneField(
        ImageUpload, on_delete=models.CASCADE, null=True, blank=True
    )
    year = models.IntegerField(null=True, blank=True)
    openscrobbler_url = models.URLField(null=True, blank=True)
    discogs_url = models.URLField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = AlbumQuerySet.as_manager()

    def __str__(self):
        return f"{self.artist} - {self.title}"

    class Meta:
        indexes = [
            models.Index(fields=["rating"]),
            models.Index(fields=["slug"]),
        ]


@register_setting
class LastfmSettings(BaseGenericSetting):
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    show_widget_in_footer = models.BooleanField(default=False)
