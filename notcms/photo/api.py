from django.shortcuts import get_object_or_404
from ninja import Router

from notcms.photo.models import Photo, PhotoAlbum
from notcms.photo.schemas import PhotoSchema

router = Router()


@router.get("/", response=list[PhotoSchema])
def get_all_photos(request):
    return Photo.objects.all()


@router.get("/{photo_id}", response=PhotoSchema)
def get_photo_details(request, photo_id: int):
    return get_object_or_404(Photo, id=photo_id)


@router.get("/album/none", response=list[PhotoSchema])
def get_photos_without_album(request):
    return Photo.objects.filter(albums__isnull=True)


@router.get("/album/{slug}", response=list[PhotoSchema])
def get_photos_by_album(request, slug: str):
    album = get_object_or_404(PhotoAlbum, slug=slug)
    return Photo.objects.filter(albums__in=[album])
