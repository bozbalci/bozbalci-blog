from django.contrib.flatpages.models import FlatPage
from django.db import models


# Create your models here.
class CustomFlatPage(FlatPage):
    is_draft = models.BooleanField(default=True, help_text="Mark this page as draft.")
    published_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = "Flatpage"
        verbose_name_plural = "Flatpages"
