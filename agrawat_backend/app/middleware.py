from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class HealthCheckMiddleware(MiddlewareMixin):
    ''' AWS EB will send health checks to this url. '''

    def process_request(self, request):
        if request.META["PATH_INFO"] == "/health":
            return JsonResponse({'message': 'Service is up and running!'})
