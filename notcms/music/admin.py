from django.contrib import admin

from notcms.music.models import Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass
