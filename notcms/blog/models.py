from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from notcms.core.helpers import markdown
from notcms.core.models import Category, Tag


# Create your models here.
class CustomFlatPage(FlatPage):
    is_draft = models.BooleanField(default=True, help_text="Mark this page as draft.")
    published_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = "Flatpage"
        verbose_name_plural = "Flatpages"


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
        "if you know the URL.",
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
