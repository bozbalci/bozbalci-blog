import io
import os
from datetime import datetime

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.core.files.storage import default_storage

def year_month_directory(instance, filename):
    """
    Function to generate upload path in the format /year/month/filename
    """
    current_date = datetime.now()
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    return os.path.join(year, month, filename)


class ImageUpload(models.Model):
    original = models.ImageField(upload_to=year_month_directory, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=year_month_directory, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    removed_from_s3 = models.BooleanField(default=False)

    def remove_from_s3(self):
        if self.original:
            default_storage.delete(self.original.name)
            self.original = None
        if self.thumbnail:
            default_storage.delete(self.thumbnail.name)
            self.thumbnail = None
        self.removed_from_s3 = True
        self.save()

    def delete(self, *args, **kwargs):
        self.remove_from_s3()
        super().delete(*args, **kwargs)

    @staticmethod
    def generate_thumbnail(image_file):
        max_width = 600
        img = Image.open(image_file)
        img_format = img.format if img.format else "JPEG"

        original_width, original_height = img.size
        aspect_ratio = original_height / original_width
        new_height = int(max_width * aspect_ratio)
        new_size = (max_width, new_height)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        thumbnail_io = io.BytesIO()
        img.save(thumbnail_io, format=img_format)
        return ContentFile(thumbnail_io.getvalue(), name=f"thumb_{image_file.name}")

    def __str__(self):
        if self.original:
            return self.original.name
        elif self.thumbnail:
            return self.thumbnail.name
        else:
            return f"deleted ImageUpload with id={self.id}"


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
