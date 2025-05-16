from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.timezone import make_aware

from notcms.blog.models import BlogPostPage


class BlogFeed(Feed):
    title = "bozbalci"
    link = "/blog/"
    feed_type = Atom1Feed

    def items(self):
        return BlogPostPage.objects.live().order_by("-date")[:10]

    def item_title(self, item: BlogPostPage):
        return item.title

    def item_description(self, item: BlogPostPage):
        return item.intro

    def item_link(self, item: BlogPostPage):
        return item.permalink

    def item_pubdate(self, item: BlogPostPage):
        return make_aware(datetime.combine(item.date, time.min))

    def item_updateddate(self, item: BlogPostPage):
        return item.last_published_at

    def get_feed(self, obj, request):
        feedgen = super().get_feed(obj, request)
        feedgen.content_type = "application/xml; charset=utf-8"
        return feedgen
