from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.rich_text import RichText

from notcms.photo.models import PhotoPage

register = template.Library()


@register.simple_tag
@mark_safe
def lg_caption(photo: PhotoPage):
    """
    Converts a `PhotoPage` into the appropriate `data-sub-html=` attribute
    to be used within a lightGallery thumbnail.
    """
    if not photo:
        return ""

    rendered_html = render_to_string(
        "photo/partials/lightgallery_caption_sub.html", {"photo": photo}
    )
    translation_table = str.maketrans({'"': "'", "\n": ""})
    return rendered_html.translate(translation_table)


@register.filter
@mark_safe
def double_to_single_quotes(richtext: RichText) -> str:
    """
    Example: data-sub-html={{ caption|richtext|double_to_single_quotes }}
    """
    html = str(richtext)
    translation_table = str.maketrans({'"': "'", "\n": ""})
    return html.translate(translation_table)
