from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from music.lastfm import LastfmAPI
from music.models import Album
from music.schemas import AlbumSchema

router = Router()
lastfm_api = LastfmAPI()


@router.get("/last-played")
def get_last_played(request):
    return lastfm_api.get_recent_tracks()


@router.get("/albums", response=List[AlbumSchema])
def get_albums(request, year: int = 0):
    queryset = Album.objects.all()

    if year:
        queryset = queryset.filter(year=year)

    return queryset


@router.get("/albums/rated-10", response=List[AlbumSchema])
def get_albums_with_rating_10(request):
    return Album.objects.perfect_tens()


@router.get("/albums/shuffled", response=List[AlbumSchema])
def get_albums_shuffled(request):
    return Album.objects.shuffled()


@router.get("/album/{slug}", response=AlbumSchema)
def get_album_details(request, slug: str):
    return get_object_or_404(Album, slug=slug)
