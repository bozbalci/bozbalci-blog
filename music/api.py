from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from music.lastfm import lastfm_api
from music.models import Album
from music.schemas import AlbumSchema

router = Router()


@router.get("/last-played")
def get_last_played(request):
    return lastfm_api.get_last_played()


@router.get("/albums", response=List[AlbumSchema])
def get_albums(request, year: int = 0, rating: int = None, shuffled: bool = False):
    queryset = Album.objects.all()

    if year:
        queryset = queryset.filter(year=year)
    if rating is not None:
        queryset = queryset.filter(rating=rating)
    if shuffled:
        queryset = queryset.shuffled()

    return queryset


@router.get("/album/{slug}", response=AlbumSchema)
def get_album_details(request, slug: str):
    return get_object_or_404(Album, slug=slug)
