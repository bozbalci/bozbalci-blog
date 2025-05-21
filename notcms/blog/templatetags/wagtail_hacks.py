import re

from django import template
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from wagtail.models import Page

register = template.Library()


# See: https://stackoverflow.com/a/76953774
@register.simple_tag(takes_context=True)
@mark_safe
def unfuck_footnotes(context, html):
    footnote_tag_regex = re.compile(r'<footnote id="(.*?)">.*?</footnote>')

    if not isinstance(context.get("page"), Page):
        return html

    page = context["page"]
    if not hasattr(page, "footnotes_list"):
        page.footnotes_list = []

    footnotes = {str(footnote.uuid): footnote for footnote in page.footnotes.all()}

    def replace_tag(match):
        try:
            index = process_footnote(match.group(1), page)
        except (KeyError, ValidationError):
            return ""
        else:
            href = f"#footnote-{index}"
            id_ = f"footnote-source-{index}"
            return f'<sup><a href="{href}" id="{id_}">{index}</a></sup>'

    def process_footnote(footnote_id, page):
        footnote = footnotes[footnote_id]
        if footnote not in page.footnotes_list:
            page.footnotes_list.append(footnote)
        # Add 1 to the index as footnotes are indexed starting at 1 not 0.
        return page.footnotes_list.index(footnote) + 1

    return footnote_tag_regex.sub(replace_tag, str(html))


@register.filter
@mark_safe
def strip_outer_p(html):
    return re.sub(r"^<p[^>]*>(.*?)</p>$", r"\1", html.strip(), flags=re.DOTALL)
