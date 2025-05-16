from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from notcms.photo.models import PhotoAlbumPage, PhotoPage
from notcms.photo.schemas import PhotoAlbumSchema, PhotoSchema

router = Router()


@router.get("/photos", response=list[PhotoSchema])
@paginate
def get_all_photos(request):
    return PhotoPage.objects.live().order_by("-first_published_at")


@router.get("/photo/{slug}", response=PhotoSchema)
def get_photo_by_slug(request, slug: str):
    return get_object_or_404(PhotoPage.objects.live(), slug=slug)


@router.get("/albums", response=list[PhotoAlbumSchema])
@paginate
def get_all_photo_albums(request):
    return PhotoAlbumPage.objects.live().order_by("title")


@router.get("/album/{slug}", response=PhotoAlbumSchema)
def get_photo_album_by_slug(request, slug: str):
    return get_object_or_404(PhotoAlbumPage.objects.live(), slug=slug)
