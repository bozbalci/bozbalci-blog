from django.conf import settings
from django.contrib.flatpages.views import render_flatpage
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404

from notcms.blog.models import CustomFlatPage, Post
from notcms.core.models import Category

POSTS_ON_HOMEPAGE = 5


def handler400(request, exception):
    return render(request, "400.html", status=400)


def handler403(request, exception):
    return render(request, "403.html", status=403)


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)


def home(request):
    posts = list(
        Post.objects.filter(is_draft=False)
        .exclude(categories__slug="now")
        .order_by("-created")[:POSTS_ON_HOMEPAGE]
    )
    return render(
        request,
        "blog/home.html",
        {
            "posts": posts,
        },
    )


def post(request, year, slug):
    post = get_object_or_404(Post, created__year=year, slug=slug)
    return render(request, "blog/post.html", {"post": post})


def custom_flatpage(request, url):
    if not url.startswith("/"):
        url = "/" + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(CustomFlatPage, url=url, sites=site_id)
    except Http404:
        if not url.endswith("/") and settings.APPEND_SLASH:
            url += "/"
            f = get_object_or_404(CustomFlatPage, url=url, sites=site_id)
            return HttpResponsePermanentRedirect("%s/" % request.path)
        else:
            raise
    return render_flatpage(request, f)


def then(request):
    category = Category.objects.get(slug="now")

    posts = Post.objects.filter(
        is_draft=False, categories__slug=category.slug
    ).order_by("-created")
    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "posts": posts,
        },
    )


def now(request):
    post = (
        Post.objects.filter(is_draft=False, categories__slug="now")
        .order_by("-created")
        .first()
    )
    return render(request, "blog/post.html", {"post": post})


def index(request):
    posts = (
        Post.objects.filter(is_draft=False)
        .exclude(categories__slug="now")
        .order_by("-created")
    )
    return render(request, "blog/archive.html", {"posts": posts})
