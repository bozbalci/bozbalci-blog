from typing import List

from ninja import Router

from photo.models import Photo
from photo.schemas import PhotoSchema

router = Router()


@router.get("/", response=List[PhotoSchema])
def photos(request):
    return Photo.objects.all()


@router.get("/{photo_id}", response=PhotoSchema)
def photo_details(request, photo_id: int):
    photo = Photo.objects.get(id=photo_id)
    return photo
