import mistune
from django import template

register = template.Library()


@register.filter
def render_markdown(text):
    if not text:
        return ""
    markdown = mistune.create_markdown(plugins=["footnotes"], escape=False)
    return markdown(text)
