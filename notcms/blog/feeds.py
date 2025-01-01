from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from notcms.blog.models import Post


class BlogFeed(Feed):
    title = "Berk Özbalcı"
    link = "/blog/"
    feed_type = Atom1Feed

    def items(self):
        return Post.objects.filter(is_draft=False).order_by("-created")[:5]

    def item_title(self, item: Post):
        return item.title

    def item_description(self, item: Post):
        return item.summary + "\n" + item.body_rendered()

    def item_link(self, item: Post):
        return item.get_absolute_url()

    def get_feed(self, obj, request):
        feedgen = super().get_feed(obj, request)
        feedgen.content_type = "application/xml; charset=utf-8"
        return feedgen
