from django.shortcuts import render, get_object_or_404

from notcms.photo.models import Photo, PhotoAlbum


def gallery_index(request):
    return gallery_from_queryset(request, Photo.objects.all())


def gallery_album(request, slug):
    album = get_object_or_404(PhotoAlbum, slug=slug)
    return gallery_from_queryset(request, Photo.objects.filter(albums__in=[album]))


def gallery_photo_details(request, pk: int):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, "photo/single_photo_details.html", {"photo": photo})


def gallery_from_queryset(request, queryset):
    return render(
        request,
        "photo/gallery.html",
        {
            "photos": queryset.prefetch_related("image"),
        },
    )
