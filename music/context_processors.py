from core.constants import SiteFeature
from core.helpers import is_feature_enabled
from music.lastfm import lastfm_api


def last_played(request):
    if is_feature_enabled(SiteFeature.LAST_PLAYED):
        track = lastfm_api.get_last_played()
        return {"last_played": track}
    return {}
