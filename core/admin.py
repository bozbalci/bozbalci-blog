from django.contrib import admin
from django.utils.html import format_html

from core.models import ImageUpload, Tag, Category


class ImageUploadAdmin(admin.ModelAdmin):
    @admin.action(description="Remove files from S3")
    def remove_from_s3(self, request, queryset):
        for image in queryset:
            image.remove_from_s3()

    actions = [remove_from_s3]

    list_display = ("id", "thumbnail_preview", "uploaded_at", "removed_from_s3")
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj: ImageUpload):
        # Choose which image source to use for thumbnail
        if obj.thumbnail:
            thumbnail_src = obj.thumbnail.url
        elif obj.original:
            thumbnail_src = obj.original.url
        else:
            thumbnail_src = None

        if thumbnail_src:
            return format_html(
                '<img src="{0}" style="max-width: 200px; max-height: 200px;" />',
                thumbnail_src
            )
        return "-"

    thumbnail_preview.short_description = "Thumbnail preview"

admin.site.register(ImageUpload, ImageUploadAdmin)

admin.site.register(Category)
admin.site.register(Tag)