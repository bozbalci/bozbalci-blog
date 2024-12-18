import exifread
from django.contrib import admin
from django import forms
from django.utils.html import format_html

from core.models import ImageUpload
from photo.helpers import filter_exif, AdminExifMixin
from photo.models import Photo


class PhotoAdminForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False, help_text="Upload an image from your computer."
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
        fields = ("title",)

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

        if image_file:
            # Generate the thumbnail
            thumbnail = ImageUpload.generate_thumbnail(image_file)

            # Create and save the ImageUpload object first
            image_upload = ImageUpload(
                original=image_file,
                thumbnail=thumbnail
            )
            image_upload.save()  # Save the related object to the database

            # Assign the saved ImageUpload object to the instance
            instance.image = image_upload
            instance.exif = self.cleaned_data["exif"]

        if commit:
            # Save the main instance
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
