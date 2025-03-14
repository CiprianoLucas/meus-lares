from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate

from .exceptions_translate import translate


class DomainAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        origin = (
            request.META.get("HTTP_ORIGIN", "").lstrip("https://").lstrip("http://")
        )
        if not origin:
            origin = (
                request.META.get("HTTP_HOST", None).lstrip("https://").lstrip("http://")
            )

        if origin == settings.SITE:
            if not (
                request.path.startswith("/admin/")
                or request.path.startswith("/user/f/")
            ):
                return redirect(settings.URL_FRONT)
            return None

        if origin == settings.URL_FRONT.lstrip("https://").lstrip("http://"):
            if request.path.startswith("/admin/") or request.path.startswith(
                "/user/f/"
            ):
                return redirect(settings.URL_FRONT)
            return None

        return redirect(settings.URL_FRONT)


class HeaderLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang_code = request.headers.get("Accept-Language", "").split(",")[0]
        lang_code = lang_code.lower()

        if lang_code in dict(settings.LANGUAGES):
            activate(lang_code)

        response = self.get_response(request)

        response = translate(response)

        return response
