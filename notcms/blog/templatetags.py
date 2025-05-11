import re
from datetime import date as dt_date
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.template.defaultfilters import date
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.timezone import get_current_timezone
from jinja2 import pass_context
from wagtail.models import Page, Site

from notcms.blog.helpers import cache_response
from notcms.blog.models import FooterText, Menu, MenuItem

DATE_FMT = "F j, Y"
ISO_DATE_FMT = "c"


def coerce_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    if isinstance(obj, dt_date):
        return datetime.combine(obj, datetime.min.time())
    elif isinstance(obj, str):
        # Assume ISO format
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return None
    else:
        return None


def format_date(obj):
    obj = coerce_datetime(obj)
    return date(obj, DATE_FMT)


def format_iso_date(obj):
    obj = coerce_datetime(obj)
    return date(obj, ISO_DATE_FMT)


def now(format_string):
    tzinfo = get_current_timezone() if settings.USE_TZ else None
    cur_datetime = datetime.now(tz=tzinfo)
    return date_format(cur_datetime, format_string)


@pass_context
def routablepageurl(context, page, url_name, *args, **kwargs):
    """
    Adapted from: https://github.com/wagtail/wagtail/blob/main/wagtail/contrib/routable_page/templatetags/wagtailroutablepage_tags.py
    """
    request = context["request"]
    site = Site.find_for_request(request)
    base_url = page.relative_url(site, request)
    routed_url = page.reverse_subpage(url_name, args=args, kwargs=kwargs)
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url + routed_url


@cache_response("is_naked_day", timeout=60 * 10)
def is_naked_day(month=4, day=9):
    current_year = datetime.now().year
    base_time = datetime(current_year, month, day)
    start = (base_time + timedelta(hours=-14)).timestamp()
    end = (base_time + timedelta(hours=36)).timestamp()
    now = datetime.now().timestamp()
    return start <= now <= end


def naked_css(request):
    """
    https://css-naked-day.github.io/

    April 9 is CSS Naked Day. This context processor sets a flag
    that can be used in templates to disable loading CSS.
    """

    if "nocss" in request.GET:
        request.session["nocss"] = True
    elif "css" in request.GET:
        request.session.pop("nocss", None)

    no_css = request.session.get("nocss", False) or is_naked_day()
    return no_css


def get_menu(key):
    cache_key = f"blog_menu_{key}"

    def fetch_menu_items():
        try:
            menu = Menu.objects.prefetch_related(
                Prefetch(
                    "items",
                    queryset=MenuItem.objects.select_related("link_page").order_by(
                        "sort_order"
                    ),
                )
            ).get(key=key)
            return list(menu.items.all())
        except Menu.DoesNotExist:
            return None

    return cache.get_or_set(cache_key, fetch_menu_items, timeout=60 * 10)


@cache_response("blog_footer_text", timeout=60 * 10)
def get_footer_text():
    instance = FooterText.objects.filter(live=True).first()

    return instance.body if instance else ""


# See: https://stackoverflow.com/a/76953774
@pass_context
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

    return mark_safe(footnote_tag_regex.sub(replace_tag, str(html)))


def strip_outer_p(html):
    stripped = re.sub(r"^<p[^>]*>(.*?)</p>$", r"\1", html.strip(), flags=re.DOTALL)
    res = mark_safe(stripped)
    return res
