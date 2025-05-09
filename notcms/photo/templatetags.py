from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from notcms.photo.models import Photo


def lg_caption(photo: Photo):
    """
    Converts a `Photo` into the appropriate `data-sub-html=` attribute
    to be used within a lightGallery thumbnail.
    """
    if not photo:
        return ""

    rendered_html = render_to_string(
        "photo/partials/lightgallery_caption_sub.html", {"photo": photo}
    )
    translation_table = str.maketrans({'"': "'", "\n": ""})
    rendered_html = rendered_html.translate(translation_table)
    return mark_safe(rendered_html)
