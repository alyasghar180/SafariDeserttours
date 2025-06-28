from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect

from bookings.models import Booking
from packages.models import Package, PackageCategory, PackageReview
from accounts.models import CustomUser


def is_admin(user):
    return user.is_staff or user.is_superuser


def dashboard_login(request):
    """
    Dashboard login view
    """
    # If user is already authenticated and is staff, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse('dashboard_home'))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect(reverse('dashboard_home'))
            else:
                messages.error(request, _('You do not have permission to access the admin dashboard.'))
                return redirect(reverse('home'))
        else:
            messages.error(request, _('Invalid username or password'))
    
    return render(request, 'dashboard/login.html')


@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    """
    Dashboard home view showing key metrics and recent activity
    """
    # Get date ranges for filtering
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    last_month_end = start_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    
    # Booking statistics
    total_bookings = Booking.objects.count()
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    bookings_this_month = Booking.objects.filter(created_at__date__gte=start_of_month).count()
    bookings_last_month = Booking.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    
    # Revenue statistics
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0
    revenue_this_month = Booking.objects.filter(
        created_at__date__gte=start_of_month
    ).aggregate(total=Sum('total_price'))['total'] or 0
    revenue_last_month = Booking.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Package statistics
    total_packages = Package.objects.count()
    active_packages = Package.objects.filter(is_active=True).count()
    featured_packages = Package.objects.filter(is_featured=True).count()
    
    # User statistics
    total_users = CustomUser.objects.count()
    new_users_this_month = CustomUser.objects.filter(date_joined__date__gte=start_of_month).count()
    
    # Review statistics
    total_reviews = PackageReview.objects.count()
    average_rating = PackageReview.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg'] or 0
    pending_reviews = PackageReview.objects.filter(is_approved=False).count()
    
    # Booking status breakdown
    status_counts = dict(Booking.objects.values_list('status').annotate(count=Count('status')))
    
    context = {
        'total_bookings': total_bookings,
        'recent_bookings': recent_bookings,
        'bookings_this_month': bookings_this_month,
        'bookings_last_month': bookings_last_month,
        'booking_growth': ((bookings_this_month - bookings_last_month) / max(bookings_last_month, 1)) * 100 if bookings_last_month else 100,
        
        'total_revenue': total_revenue,
        'revenue_this_month': revenue_this_month,
        'revenue_last_month': revenue_last_month,
        'revenue_growth': ((revenue_this_month - revenue_last_month) / max(revenue_last_month, 1)) * 100 if revenue_last_month else 100,
        
        'total_packages': total_packages,
        'active_packages': active_packages,
        'featured_packages': featured_packages,
        
        'total_users': total_users,
        'new_users_this_month': new_users_this_month,
        
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1),
        'pending_reviews': pending_reviews,
        
        'status_counts': status_counts,
    }
    
    return render(request, 'dashboard/dashboard_home.html', context)


@login_required
@user_passes_test(is_admin)
def booking_list(request):
    """
    View for listing and filtering bookings
    """
    # Get filter parameters from request
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search = request.GET.get('search', '')
    
    # Start with all bookings
    bookings = Booking.objects.all().select_related('package', 'user').order_by('-created_at')
    
    # Get total bookings count for statistics
    total_bookings = bookings.count()
    
    # Get status counts for dashboard statistics
    status_counts = dict(bookings.values_list('status').annotate(count=Count('status')).values_list('status', 'count'))
    
    # Apply filters
    if status:
        bookings = bookings.filter(status=status)
    
    if date_from:
        bookings = bookings.filter(booking_date__gte=date_from)
    
    if date_to:
        bookings = bookings.filter(booking_date__lte=date_to)
    
    if search:
        bookings = bookings.filter(
            Q(booking_id__icontains=search) |
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(package__name__icontains=search)
        )
    
    # Get status choices for the filter dropdown
    status_choices = Booking.STATUS_CHOICES
    
    context = {
        'bookings': bookings,
        'status_choices': status_choices,
        'selected_status': status,
        'date_from': date_from,
        'date_to': date_to,
        'search': search,
        'total_bookings': total_bookings,
        'status_counts': status_counts,
    }
    
    return render(request, 'dashboard/booking_list.html', context)


@login_required
@user_passes_test(is_admin)
def package_list(request):
    """
    View for listing and filtering packages
    """
    # Get filter parameters from request
    category = request.GET.get('category', '')
    is_active = request.GET.get('is_active', '')
    is_featured = request.GET.get('is_featured', '')
    search = request.GET.get('search', '')
    
    # Start with all packages
    packages = Package.objects.all().select_related('category').order_by('name')
    
    # Apply filters
    if category:
        packages = packages.filter(category__id=category)
    
    if is_active == 'true':
        packages = packages.filter(is_active=True)
    elif is_active == 'false':
        packages = packages.filter(is_active=False)
    
    if is_featured == 'true':
        packages = packages.filter(is_featured=True)
    elif is_featured == 'false':
        packages = packages.filter(is_featured=False)
    
    if search:
        packages = packages.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(short_description__icontains=search)
        )
    
    # Get categories for the filter dropdown
    categories = PackageCategory.objects.all()
    
    context = {
        'packages': packages,
        'categories': categories,
        'selected_category': category,
        'is_active': is_active,
        'is_featured': is_featured,
        'search': search,
    }
    
    return render(request, 'dashboard/package_list.html', context)


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """
    View for listing and filtering users
    """
    # Get filter parameters from request
    is_staff = request.GET.get('is_staff', '')
    is_active = request.GET.get('is_active', '')
    search = request.GET.get('search', '')
    
    # Start with all users
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Apply filters
    if is_staff == 'true':
        users = users.filter(is_staff=True)
    elif is_staff == 'false':
        users = users.filter(is_staff=False)
    
    if is_active == 'true':
        users = users.filter(is_active=True)
    elif is_active == 'false':
        users = users.filter(is_active=False)
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    context = {
        'users': users,
        'is_staff': is_staff,
        'is_active': is_active,
        'search': search,
    }
    
    return render(request, 'dashboard/user_list.html', context)


@login_required
@user_passes_test(is_admin)
def review_list(request):
    """
    View for listing and managing reviews
    """
    # Get filter parameters from request
    is_approved = request.GET.get('is_approved', '')
    rating = request.GET.get('rating', '')
    search = request.GET.get('search', '')
    
    # Start with all reviews
    reviews = PackageReview.objects.all().select_related('package', 'user').order_by('-created_at')
    
    # Apply filters
    if is_approved == 'true':
        reviews = reviews.filter(is_approved=True)
    elif is_approved == 'false':
        reviews = reviews.filter(is_approved=False)
    
    if rating:
        reviews = reviews.filter(rating=rating)
    
    if search:
        reviews = reviews.filter(
            Q(title__icontains=search) |
            Q(comment__icontains=search) |
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(package__name__icontains=search)
        )
    
    context = {
        'reviews': reviews,
        'is_approved': is_approved,
        'rating': rating,
        'search': search,
    }
    
    return render(request, 'dashboard/review_list.html', context)


@login_required
@user_passes_test(is_admin)
def toggle_review_approval(request, review_id):
    """
    Toggle the approval status of a review
    """
    review = get_object_or_404(PackageReview, id=review_id)
    review.is_approved = not review.is_approved
    review.save()
    
    messages.success(request, _('Review approval status updated successfully.'))
    return redirect('dashboard_review_list')


@login_required
@user_passes_test(is_admin)
def booking_detail(request, booking_id):
    """
    View for displaying and managing a single booking
    """
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    context = {
        'booking': booking,
        'status_choices': Booking.STATUS_CHOICES,
    }
    
    return render(request, 'dashboard/booking_detail.html', context)


@login_required
@user_passes_test(is_admin)
def update_booking_status(request, booking_id):
    """
    Update the status of a booking
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)
    
    booking = get_object_or_404(Booking, booking_id=booking_id)
    new_status = request.POST.get('status')
    
    if new_status not in dict(Booking.STATUS_CHOICES):
        return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
    
    # If cancelling, record the cancellation time and reason
    if new_status == 'cancelled' and booking.status != 'cancelled':
        booking.cancelled_at = timezone.now()
        booking.cancellation_reason = request.POST.get('reason', '')
    
    booking.status = new_status
    booking.save()
    
    messages.success(request, _(f'Booking status updated to {booking.get_status_display()}'))
    
    # Determine where to redirect based on the referer
    referer = request.META.get('HTTP_REFERER')
    if referer and 'booking_detail' in referer:
        return HttpResponseRedirect(reverse('dashboard_booking_detail', args=[booking_id]))
    else:
        return HttpResponseRedirect(reverse('dashboard_booking_list'))


@login_required
def dashboard_logout(request):
    """
    Dashboard logout view
    """
    logout(request)
    messages.success(request, _('You have been successfully logged out.'))
    return redirect(reverse('dashboard_login'))
