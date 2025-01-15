import io
import os

from django.core.files.base import ContentFile
from PIL import Image


def resize_image_to_width(image: Image, max_width: int = 1600):
    original_width, original_height = image.size

    # Don't resize anything if we're already smaller than max width
    if original_width <= max_width:
        return image

    aspect_ratio = original_height / original_width
    new_height = int(max_width * aspect_ratio)
    return image.resize((max_width, new_height), Image.Resampling.LANCZOS)


def get_file_extension(format: str):
    """Get the appropriate file extension for a given format."""
    format_extension_map = {
        "JPEG": "jpg",
        "JPG": "jpg",
        "PNG": "png",
        "WEBP": "webp",
        "GIF": "gif",
    }
    return format_extension_map.get(format.upper(), "jpg")  # Default to 'jpg'


def image_to_django_file(
    image: Image, format: str, filename: str, save_params: dict = None
):
    if save_params is None:
        save_params = {}

    # Get the new file extension based on format
    new_extension = get_file_extension(format)
    base_name, _ = os.path.splitext(filename)  # Split original filename and extension
    new_filename = f"{base_name}.{new_extension}"

    buffer = io.BytesIO()
    image.save(buffer, format=format, **save_params)
    return ContentFile(buffer.getvalue(), name=new_filename)


def generate_thumbnail(image_file: ContentFile, max_width: int = 600):
    img = Image.open(image_file)
    img = img.convert("RGB")  # Ensure compatibility for WEBP
    img_format = "WEBP" if img.format == "WEBP" else "JPEG"

    img = resize_image_to_width(img, max_width)
    return image_to_django_file(
        img, img_format, image_file.name, save_params={"quality": 80}
    )


def compress_image(
    image_file: ContentFile,
    max_width: int = 1600,
    quality: int = 85,
    file_format: str = "JPEG",
):
    img = Image.open(image_file)
    img = img.convert("RGB")  # Ensure compatibility for WEBP
    img = resize_image_to_width(img, max_width)
    return image_to_django_file(
        img, file_format, image_file.name, save_params={"quality": quality}
    )
