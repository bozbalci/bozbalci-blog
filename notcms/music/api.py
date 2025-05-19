from django.db.models.functions import Random
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from notcms.music.lastfm import LastfmTrack, lastfm_api
from notcms.music.models import AlbumPage
from notcms.music.schemas import AlbumSchema

router = Router()


@router.get("/last-played", response=LastfmTrack)
def get_last_played_track(request, skip_cache: bool = False) -> LastfmTrack | None:
    """
    Get the last track played by me as reported by Last.fm. The response from Last.fm
    is cached for a few minutes, so this endpoint does not always return the latest
    track.
    """
    if skip_cache:
        return lastfm_api.get_last_played()
    else:
        return lastfm_api.get_cached_last_played()


@router.get("/albums", response=list[AlbumSchema])
@paginate
def get_albums(request, year: int = None, rating: int = None, shuffled: bool = False):
    """
    Get the albums in my music collection.
    """
    queryset = (
        AlbumPage.objects.live()
        .order_by("-first_published_at")
        .select_related("cover_image")
    )

    if year:
        queryset = queryset.filter(year=year)
    if rating:
        queryset = queryset.filter(rating=rating)
    if shuffled:
        queryset = queryset.order_by(Random())

    return queryset


@router.get("/album/{slug}", response=AlbumSchema)
def get_album_by_slug(request, slug: str) -> AlbumPage:
    return get_object_or_404(AlbumPage.objects.live(), slug=slug)
