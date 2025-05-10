from functools import wraps

import mistune
from django.core.cache import cache


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


markdown = mistune.create_markdown(plugins=["footnotes"], escape=False)
