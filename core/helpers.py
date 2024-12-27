from functools import wraps

import mistune
from django.core.cache import cache

from core.constants import SiteFeature
from core.models import Feature


def cache_response(cache_key, timeout):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper

    return decorator


@cache_response("core_feature_enabled", timeout=60)
def is_feature_enabled(site_feature: SiteFeature):
    try:
        feature = Feature.objects.get(slug=site_feature.value)
        return feature.enabled
    except Feature.DoesNotExist:
        return False


markdown = mistune.create_markdown(plugins=["footnotes"], escape=False)
