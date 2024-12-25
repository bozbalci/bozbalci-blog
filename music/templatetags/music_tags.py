import math

from django import template
from django.utils.safestring import mark_safe

# SVG templates
FULL_STAR_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
  <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z" clip-rule="evenodd" />
</svg>
"""

HALF_STAR_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" class="size-6" viewBox="0 0 24 24">
  <path d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
  <path fill="currentColor" d="M11.5 3.5h0L9.4 8.6c0 .2-.3.3-.5.3l-5.5.4c-.1 0-.3 0-.4.2-.2.2-.2.6 0 .8l4.2 3.6c.2.1.2.4.2.6l-1.3 5.4v.4c.2.3.5.3.8.2l4.7-2.9h.3V3.2c-.2 0-.4.1-.5.3Z" />
</svg>
"""

EMPTY_STAR_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
</svg>
"""

register = template.Library()


@register.filter
def stars(value: int):
    scaled_value = round(value / 2, 1)
    total_stars = 5
    full_stars = math.floor(scaled_value)
    has_half_star = (scaled_value % 1) != 0
    empty_stars = total_stars - full_stars - has_half_star

    html = '<div class="stars">'
    html += FULL_STAR_SVG * full_stars
    if has_half_star:
        html += HALF_STAR_SVG
    html += EMPTY_STAR_SVG * empty_stars
    html += "</div>"
    return mark_safe(html)
