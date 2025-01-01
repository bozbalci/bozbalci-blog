from notcms.core.constants import SiteFeature
from notcms.core.helpers import is_feature_enabled
from notcms.music.lastfm import lastfm_api


def last_played(request):
    if is_feature_enabled(SiteFeature.LAST_PLAYED):
        track = lastfm_api.get_last_played()
        return {"last_played": track}
    return {}
