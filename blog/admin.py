from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from blog.models import CustomFlatPage


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
    list_display = ("url", "title", "is_draft", "published_at", "modified_at")
    list_filter = ("is_draft", "published_at", "modified_at")
    search_fields = ("url", "title", "content")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["template_name"].initial = "templates/markdown_content.html"
        return form


admin.site.register(CustomFlatPage, CustomFlatPageAdmin)
admin.site.unregister(FlatPage)
