from datetime import datetime

from django.db import models
from django.db.models.functions import Random
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.models import Page

from notcms.core.models import ImageUpload, Tag


# Deprecated
class AlbumQuerySet(models.QuerySet):
    def get_by_slug(self, slug):
        return self.get(slug=slug)

    def perfect_tens(self):
        return self.filter(rating__isnull=False, rating=10)

    def shuffled(self):
        return self.order_by(Random())


# Deprecated
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


class MusicCollectionIndexPage(RoutablePageMixin, Page):
    subpage_types = ["AlbumPage"]
    template = "music/index.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        return {
            "music_index": self,
            "albums": AlbumPage.objects.all(),
        }

    @path("year/<int:year>/")
    @path("year/current/")
    def albums_for_year(self, request, year=None):
        if year is None:
            year = datetime.now().year

        albums = AlbumPage.objects.filter(year=year)

        return self.render(
            request,
            context_overrides={
                "albums": albums,
            },
        )

    @path("rated/<int:rating>/")
    @path("rated/perfect/")
    def albums_for_rating(self, request, rating=None):
        if rating is None:
            rating = 10

        albums = AlbumPage.objects.filter(rating=rating)

        return self.render(
            request,
            context_overrides={
                "albums": albums,
            },
        )

    @path("shuffled/")
    def shuffled(self, request):
        albums = AlbumPage.objects.order_by(Random())

        return self.render(
            request,
            context_overrides={
                "albums": albums,
            },
        )


class AlbumPage(Page):
    MAX_RELATED_ALBUMS_SHOWN = 4

    artist = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    cover_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    openscrobbler_url = models.URLField(null=True, blank=True)
    discogs_url = models.URLField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    review = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("artist"),
        FieldPanel("year"),
        FieldPanel("cover_image"),
        FieldPanel("openscrobbler_url"),
        FieldPanel("discogs_url"),
        FieldPanel("rating"),
        FieldPanel("review"),
    ]

    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        return {
            **context,
            "album": self,
            "music_index": self.get_parent().specific,
            "related_albums": AlbumPage.objects.live()
            .filter(artist=self.artist)
            .exclude(id=self.id)
            .order_by("-first_published_at")[: self.MAX_RELATED_ALBUMS_SHOWN],
        }

    def __str__(self):
        return f"{self.artist} - {self.title} ({self.year})"


@register_setting
class LastfmSettings(BaseGenericSetting):
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    show_widget_in_footer = models.BooleanField(default=False)
