from django.conf import settings
from django.urls import resolve
from django.http import JsonResponse
import json

# Import API_AVAILABILITY directly from settings
API_AVAILABILITY = settings.API_AVAILABILITY


class APIStatusMiddleware:
    """
    Middleware to control API access based on API_AVAILABILITY setting.
    If API_AVAILABILITY is False, only the API overview endpoint is accessible.
    
    Note: Django middleware must return HttpResponse-compatible objects,
    so we use JsonResponse with REST framework-style structure.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if API_AVAILABILITY is disabled
        if not API_AVAILABILITY:
            # Get the current URL name
            try:
                current_url = resolve(request.path_info)
                url_name = current_url.url_name
                
                # Allow access only to API overview endpoint
                if url_name != 'api-overview':
                    response_data = {
                        'error': 'Service Temporarily Limited',
                        'message': 'Due to high traffic volume, this endpoint is temporarily unavailable to ensure system stability.',
                        'code': 503,
                        'status': 'Service Unavailable',
                        'available_endpoint': {
                            'url': request.build_absolute_uri('/'),
                            'method': 'GET',
                            'description': 'API Overview - Current service status and available resources'
                        },
                        'support': {
                            'retry_suggestion': 'Please try again in a few days (or weeks) as we are currently experiencing high traffic.',
                            'contact': 'Contact support if this issue persists',
                            'contact_site': 'https://ridwaanhall.com/contact',
                        }
                    }
                    
                    # Return JsonResponse with REST framework style structure
                    response = JsonResponse(response_data, status=503)
                    response['Content-Type'] = 'application/json'
                    response['Retry-After'] = '3600'  # Suggest retry after 1 hour
                    return response
                    
            except Exception:
                # If URL resolution fails, block access when API is disabled
                response_data = {
                    'error': 'Service Temporarily Limited',
                    'message': 'Due to high traffic volume, this service is temporarily unavailable.',
                    'code': 503,
                    'status': 'Service Unavailable'
                }
                
                response = JsonResponse(response_data, status=503)
                response['Content-Type'] = 'application/json'
                response['Retry-After'] = '3600'
                return response

        response = self.get_response(request)
        return response
