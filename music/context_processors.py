from music.lastfm import lastfm_api


def last_played(request):
    track = lastfm_api.get_last_played()

    return {"last_played": track}
