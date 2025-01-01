from django.contrib import admin
from django.utils.html import format_html

from notcms.music.models import Album


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "thumbnail_preview", "artist", "title", "year", "rating")

    def thumbnail_preview(self, obj: Album):
        if obj.cover_image and obj.cover_image.original:
            return format_html(
                '<img src="{0}" style="max-width: 100px; max-height: 100px;" />',
                obj.cover_image.original.url,
            )
        return "-"


admin.site.register(Album, AlbumAdmin)
