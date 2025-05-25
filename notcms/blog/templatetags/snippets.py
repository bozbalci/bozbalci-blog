from django import template
from django.core.cache import cache

from notcms.blog.models import FooterText, NowPostPreamble

register = template.Library()


@register.simple_tag(takes_context=True)
def get_footer_text(context):
    request = context["request"]
    locale = request.locale
    cache_key = f"blog_footer_text-{locale.language_code}"

    def fetch_footer_text():
        instance = FooterText.objects.filter(live=True).filter(locale=locale).first()
        return instance.body if instance else ""

    return cache.get_or_set(cache_key, fetch_footer_text, timeout=60 * 10)


@register.simple_tag(takes_context=True)
def get_now_post_preamble(context):
    request = context["request"]
    locale = request.locale
    cache_key = f"blog_now_post_preamble-{locale.language_code}"

    def fetch_now_post_preamble():
        instance = NowPostPreamble.objects.filter(locale=request.locale).first()
        return instance.body if instance else ""

    return cache.get_or_set(cache_key, fetch_now_post_preamble, timeout=60 * 10)
