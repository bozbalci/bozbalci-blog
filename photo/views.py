from django.shortcuts import render, get_object_or_404

from photo.models import Photo, PhotoAlbum


def gallery_index(request):
    return render(request, "photo/gallery.html", {"photos": Photo.objects.all()})


def gallery_album(request, slug):
    album = get_object_or_404(PhotoAlbum, slug=slug)
    return render(
        request,
        "photo/gallery.html",
        {"photos": Photo.objects.filter(albums__in=[album])},
    )


def gallery_photo_details(request, pk: int):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, "photo/single_photo_details.html", {"photo": photo})
