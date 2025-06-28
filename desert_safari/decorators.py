from functools import wraps
from django.views.decorators.csrf import csrf_exempt

def csrf_exempt_for_development(view_func):
    """
    A decorator that wraps the view function with csrf_exempt for development environments.
    In production, this should be removed or modified to enforce CSRF protection.
    """
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    
    # Apply csrf_exempt to the view function
    return csrf_exempt(wrapped_view)
