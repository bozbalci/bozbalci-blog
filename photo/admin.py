import exifread
from django.contrib import admin
from django import forms
from django.utils.html import format_html

from core.images import generate_thumbnail, compress_image
from core.models import ImageUpload
from photo.helpers import filter_exif, AdminExifMixin
from photo.models import Photo, PhotoAlbum


class PhotoAdminForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False, help_text="Upload an image from your computer."
    )

    # TODO -- This violates DRY
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["image_file"].required = False
        else:
            # New object - image field is required
            self.fields["image_file"].required = True

    class Meta:
        model = Photo
        fields = ("title", "albums")

    def clean(self):
        cleaned_data = super().clean()
        image_file = cleaned_data.get("image_file")

        if (
            not self.instance.pk and not image_file
        ):  # If it's a new object, require the file
            raise forms.ValidationError("Please upload an image.")

        # Extract EXIF data
        if image_file:
            image_file.seek(0)
            exif_data = exifread.process_file(image_file)
            cleaned_data["exif"] = filter_exif(
                {k: str(v) for k, v in exif_data.items()}
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        image_file = self.cleaned_data["image_file"]
        resize_width = self.cleaned_data.get("resize_width", 1600)
        compress_upload = self.cleaned_data.get("compress_upload", True)
        should_generate_thumbnail = self.cleaned_data.get("generate_thumbnail", True)
        compression_format = self.cleaned_data.get("compression_format", "JPEG")
        compression_quality = self.cleaned_data.get("compression_quality", 80)
        thumbnail_width = self.cleaned_data.get("thumbnail_width", 600)

        if image_file:
            image_upload = ImageUpload()

            if compress_upload:
                compressed_image = compress_image(
                    image_file,
                    max_width=resize_width,
                    quality=compression_quality,
                    file_format=compression_format,
                )
                image_upload.original = compressed_image
            if should_generate_thumbnail:
                thumbnail = generate_thumbnail(image_file, max_width=thumbnail_width)
                image_upload.thumbnail = thumbnail

            # Create and save the ImageUpload object first
            image_upload.save()

            # Assign the saved ImageUpload object to the instance
            instance.image = image_upload
            instance.exif = self.cleaned_data["exif"]

        if commit:
            instance.save()
        return instance


class PhotoAdmin(AdminExifMixin, admin.ModelAdmin):
    form = PhotoAdminForm
    list_display = (
        "id",
        "title",
        "thumbnail_preview",
        "uploaded_at",
    )
    readonly_fields = (
        "thumbnail_preview",
        "uploaded_at",
    )

    def thumbnail_preview(self, obj: Photo):
        if obj.image and obj.image.thumbnail:
            return format_html(
                '<img src="{0}" style="max-width: 200px; max-height: 200px;" />',
                obj.thumbnail_url,
            )
        return "-"

    thumbnail_preview.short_description = "Thumbnail preview"


admin.site.register(Photo, PhotoAdmin)


class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")


admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
