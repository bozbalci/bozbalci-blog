from django import forms
from django.contrib import admin
from django.utils.html import format_html

from notcms.core.images import compress_image, generate_thumbnail
from notcms.core.models import Category, Feature, ImageUpload, Tag

admin.site.register(Category)
admin.site.register(Tag)


class ImageUploadForm(forms.ModelForm):
    compress_upload = forms.BooleanField(
        required=False,
        initial=True,
        help_text="Should the uploaded image be compressed and resized on server?",
    )
    resize_width = forms.IntegerField(
        required=False,
        initial=1600,
        help_text="Width of the resized image (in px). Default is 1600.",
    )
    compression_format = forms.ChoiceField(
        choices=[("JPEG", "JPEG"), ("WEBP", "WEBP")],
        required=False,
        help_text="Choose a format for compression.",
        initial="JPEG",
    )
    compression_quality = forms.IntegerField(
        required=False,
        initial=80,
        min_value=1,
        max_value=100,
        help_text="Compression quality (1-100). Default is 80.",
    )
    generate_thumbnail = forms.BooleanField(
        required=False, initial=True, help_text="Should a thumbnail be generated?"
    )
    thumbnail_width = forms.IntegerField(
        required=False,
        initial=600,
        help_text="Width of the thumbnail (in px). Default is 600.",
    )

    def save(self, commit=True):
        instance = super().save(commit=False)

        image_file = self.cleaned_data["original"]
        resize_width = self.cleaned_data.get("resize_width", 1600)
        compress_upload = self.cleaned_data.get("compress_upload", True)
        should_generate_thumbnail = self.cleaned_data.get("generate_thumbnail", True)
        compression_format = self.cleaned_data.get("compression_format", "JPEG")
        compression_quality = self.cleaned_data.get("compression_quality", 80)
        thumbnail_width = self.cleaned_data.get("thumbnail_width", 600)

        if compress_upload:
            compressed_image = compress_image(
                image_file,
                max_width=resize_width,
                quality=compression_quality,
                file_format=compression_format,
            )
            instance.original = compressed_image
        if should_generate_thumbnail:
            thumbnail = generate_thumbnail(image_file, max_width=thumbnail_width)
            instance.thumbnail = thumbnail
        if commit:
            instance.save()

        return instance

    class Meta:
        model = ImageUpload
        fields = ("original",)


class ImageUploadAdmin(admin.ModelAdmin):
    form = ImageUploadForm

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
                thumbnail_src,
            )
        return "-"

    thumbnail_preview.short_description = "Thumbnail preview"


admin.site.register(ImageUpload, ImageUploadAdmin)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description", "enabled")


admin.site.register(Feature, FeatureAdmin)
