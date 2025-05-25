from wagtail.models import Locale


def active_locale_middleware(get_response):
    def middleware(request):
        request.locale = Locale.get_active()
        response = get_response(request)
        return response

    return middleware
