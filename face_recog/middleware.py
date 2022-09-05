from django.conf import settings
from django import http
from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # set API URL here
        SCHEME = request.scheme
        HOST = request.get_host()
        API_URL = SCHEME + '://' + HOST
        request.api_url = API_URL
        # print('API_URL---', API_URL)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip