from django import template
from wagtail.models import Locale

from notcms.blog.models import FooterText, NowPostPreamble

register = template.Library()


@register.simple_tag
def get_footer_text():
    # TODO Cache this per-locale
    instance = (
        FooterText.objects.filter(live=True).filter(locale=Locale.get_active()).get()
    )

    return instance.body if instance else ""


@register.simple_tag
def get_now_post_preamble():
    # TODO Cache this per-locale
    instance = NowPostPreamble.objects.filter(locale=Locale.get_active()).get()

    return instance.body if instance else ""
