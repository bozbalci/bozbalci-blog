from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from notcms.blog.models import CustomFlatPage, Post


class CustomFlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {"fields": ("url", "title", "content", "template_name", "sites")}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("is_draft",),
            },
        ),
    )
    list_display = (
        "url",
        "title",
        "is_draft",
        "published_at",
        "modified_at",
        "template_name",
    )
    list_filter = ("is_draft", "published_at", "modified_at")
    search_fields = ("url", "title", "content")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["template_name"].initial = "flatpages/markdown_content.html"
        return form


admin.site.register(CustomFlatPage, CustomFlatPageAdmin)
admin.site.unregister(FlatPage)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "title",
        "summary",
        "created",
        "modified",
        "get_tags",
        "get_categories",
        "is_draft",
    )

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    get_tags.short_description = "Tags"

    def get_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

    get_categories.short_description = "Categories"


admin.site.register(Post, PostAdmin)
