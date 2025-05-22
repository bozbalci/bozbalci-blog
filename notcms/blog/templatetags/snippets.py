from django import template
from wagtail.models import Locale

from notcms.blog.models import FooterText

register = template.Library()


@register.simple_tag
def get_footer_text():
    # TODO Cache this per-locale
    instance = (
        FooterText.objects.filter(live=True).filter(locale=Locale.get_active()).get()
    )

    return instance.body if instance else ""
