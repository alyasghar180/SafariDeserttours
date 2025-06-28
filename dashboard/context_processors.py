from packages.models import PackageReview

def dashboard_context(request):
    """
    Context processor to add common dashboard data to all dashboard templates.
    This includes pending reviews count for notification badges.
    """
    context = {}
    
    # Only include data if user is authenticated and has staff privileges
    if request.user.is_authenticated and request.user.is_staff:
        # Count pending reviews for notification badge
        context['pending_reviews_count'] = PackageReview.objects.filter(is_approved=False).count()
    else:
        context['pending_reviews_count'] = 0
        
    return context
