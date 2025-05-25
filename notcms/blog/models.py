from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, PublishingPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    DraftStateMixin,
    Locale,
    Orderable,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from notcms.blog.blocks import CommonPostBodyBlock


class HomePage(Page):
    MAX_ENTRIES_IN_HOME_PAGE = 5

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["body"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        posts = (
            BlogPostPage.objects.live()
            .filter(locale=Locale.get_active())
            .order_by("-date")[: self.MAX_ENTRIES_IN_HOME_PAGE]
        )

        return {
            **context,
            "posts": posts,
        }


class BlogIndexPage(RoutablePageMixin, Page):
    subpage_types = ["BlogPostPage"]
    template = "blog/archive.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "archive_title": _("Writing"),
            "posts": BlogPostPage.objects.live()
            .filter(locale=Locale.get_active())
            .order_by("-date"),
        }

    @path(r"<int:year>/<int:month>/<slug:slug>/")
    def blog_post_by_slug(self, request, year, month, slug):
        post = get_object_or_404(
            BlogPostPage.objects.live(),
            locale=Locale.get_active(),
            date__year=year,
            date__month=month,
            slug=slug,
        )
        return post.specific.serve(request)


class BlogPostPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(CommonPostBodyBlock(), null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        "date",
        "intro",
        "body",
        InlinePanel("footnotes", label="Footnotes"),
    ]

    subpage_types = []
    parent_page_types = ["BlogIndexPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        return {
            **context,
            "post": self,
        }

    def get_url_parts(self, request=None):
        site_id, site_root_url, relative_page_url = super().get_url_parts(request)

        original_url = relative_page_url.rstrip("/")  # remove trailing slash
        *prefix, slug = original_url.split("/")
        parts = [*prefix, f"{self.date:%Y/%m}", slug]
        new_url = "/".join(parts)
        new_url += (
            "/" if relative_page_url.endswith("/") else ""
        )  # append trailing slash if needed

        return site_id, site_root_url, new_url


class FlatPage(Page):
    body = StreamField(CommonPostBodyBlock(), null=True, blank=True)

    subpage_types = []

    content_panels = Page.content_panels + [
        "body",
        InlinePanel("footnotes", label="Footnotes"),
    ]


class NowIndexPage(Page):
    subpage_types = []
    template = "blog/blog_post_page.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        post = (
            NowPostPage.objects.live()
            .filter(locale=Locale.get_active())
            .order_by("-date")
            .first()
        )

        return {
            **context,
            "page": post,
            "is_now_post": True,
        }


class ThenIndexPage(Page):
    subpage_types = ["NowPostPage"]
    template = "blog/archive.html"
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        return {
            **context,
            "archive_title": _("Then"),
            "posts": NowPostPage.objects.live()
            .filter(locale=Locale.get_active())
            .order_by("-date"),
        }


class NowPostPage(Page):
    date = models.DateField("Post date")
    body = StreamField(CommonPostBodyBlock(), null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        "date",
        "body",
        InlinePanel("footnotes", label="Footnotes"),
    ]

    subpage_types = []
    parent_page_types = ["ThenIndexPage"]

    template = "blog/blog_post_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        return {
            **context,
            "is_now_post": True,
        }


@register_snippet
class Menu(TranslatableMixin, ClusterableModel):
    key = models.SlugField()
    label = models.CharField(max_length=255)

    panels = [
        FieldPanel("key"),
        FieldPanel("label"),
        InlinePanel("items", label="Menu items"),
    ]

    def __str__(self):
        return self.label


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


@register_snippet
class NowPostPreamble(TranslatableMixin, models.Model):
    body = RichTextField(blank=True)

    panels = [FieldPanel("body")]

    def __str__(self):
        return "Now post preamble"

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Now post preambles"
