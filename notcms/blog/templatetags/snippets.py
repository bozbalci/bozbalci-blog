from django import template

from notcms.blog.helpers import cache_response
from notcms.blog.models import FooterText

register = template.Library()


@register.simple_tag
@cache_response("blog_footer_text", timeout=60 * 10)
def get_footer_text():
    instance = FooterText.objects.filter(live=True).first()

    return instance.body if instance else ""
