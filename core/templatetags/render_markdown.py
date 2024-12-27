import mistune
from django import template

from core.helpers import markdown

register = template.Library()


@register.filter
def render_markdown(text):
    if not text:
        return ""
    return markdown(text)
