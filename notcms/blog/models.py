from django.contrib.flatpages.models import FlatPage as DjangoFlatPage
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, PublishingPanel
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    Orderable,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from notcms.core.helpers import markdown
from notcms.core.models import Category, Tag


# Deprecated
class CustomFlatPage(DjangoFlatPage):
    is_draft = models.BooleanField(default=True, help_text="Mark this page as draft.")
    published_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = "Flatpage"
        verbose_name_plural = "Flatpages"


# Deprecated
class Post(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    summary = models.TextField(null=True, blank=True)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    categories = models.ManyToManyField(Category, blank=True, related_name="posts")
    is_draft = models.BooleanField(
        default=False,
        help_text="Draft entries do not show in index pages but can be visited directly"
        " if you know the URL.",
    )

    @property
    def has_now_category(self):
        return self.categories.filter(slug="now").exists()

    def body_rendered(self):
        return mark_safe(markdown(self.body))

    def get_absolute_url(self):
        return f"/blog/{self.created.year}/{self.slug}"

    def __str__(self):
        return self.title


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["body"]


class BlogIndexPage(Page):
    pass


class BlogPostPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + ["date", "intro", "body"]


class FlatPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["body"]


@register_snippet
class Menu(ClusterableModel):
    key = models.SlugField(unique=True)
    label = models.CharField(max_length=255)

    panels = [
        FieldPanel("key"),
        FieldPanel("label"),
        InlinePanel("items", label="Menu items"),
    ]

    def __str__(self):
        return self.label


@register_snippet
class MenuItem(Orderable):
    menu = ParentalKey("Menu", on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255)
    link_page = models.ForeignKey(
        Page, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    external_url = models.URLField(blank=True)
    rel = models.CharField(
        max_length=255, blank=True, help_text="Optional rel attribute, e.g. 'me'"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("link_page"),
        FieldPanel("external_url"),
        FieldPanel("rel"),
    ]

    @property
    def url(self):
        return self.link_page.url if self.link_page else self.external_url

    def __str__(self):
        return self.title


@register_snippet
class FooterText(
    DraftStateMixin, RevisionMixin, PreviewableMixin, TranslatableMixin, models.Model
):
    body = RichTextField(blank=True)

    panels = [FieldPanel("body"), PublishingPanel()]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"
