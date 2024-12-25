from django.shortcuts import render, get_object_or_404

from music.models import Album


def index(request):
    return gallery_from_queryset(request, Album.objects.all())


def all_time_favourites(request):
    return gallery_from_queryset(request, Album.objects.filter(rating=10))


def year_2024(request):
    return gallery_from_queryset(request, Album.objects.filter(year=2024))


def shuffled(request):
    return gallery_from_queryset(request, Album.objects.shuffled())


def single_album_details(request, slug: str):
    album = get_object_or_404(Album, slug=slug)
    return render(request, "music/single_album_details.html", {"album": album})


def gallery_from_queryset(request, queryset):
    return render(
        request,
        "music/gallery.html",
        {
            "albums": queryset,
        },
    )
