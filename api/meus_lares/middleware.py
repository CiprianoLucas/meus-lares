from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class DomainAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        origin = request.META.get('HTTP_ORIGIN', '').lstrip('https://').lstrip('http://')
        if not origin:
            origin = request.META.get('HTTP_HOST', None).lstrip('https://').lstrip('http://')

        if origin == settings.SITE:
            if not (request.path.startswith('/admin/') or request.path.startswith('/user/f/')):
                return redirect(settings.URL_FRONT)
            return None
        
        if origin == settings.URL_FRONT.lstrip('https://').lstrip('http://'):
            if (request.path.startswith('/admin/') or request.path.startswith('/user/f/')):
                return redirect(settings.URL_FRONT)
            return None
        
        return redirect(settings.URL_FRONT)