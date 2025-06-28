from django.utils.deprecation import MiddlewareMixin

class CSRFExemptionMiddleware(MiddlewareMixin):
    """Middleware that disables CSRF checks for development environments.
    WARNING: This should NOT be used in production environments.
    """
    def process_request(self, request):
        # For development purposes, disable CSRF checks completely
        # This is only for the browser preview and development testing
        request._dont_enforce_csrf_checks = True
        return None
        
    def __call__(self, request):
        response = self.get_response(request)
        return response
