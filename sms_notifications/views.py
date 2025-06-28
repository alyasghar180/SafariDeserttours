from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import SMSConfig
from bookings.models import Booking
from bookings.sms_utils import send_sms, send_booking_confirmation_sms, send_booking_notification_sms_to_admin


@staff_member_required
def sms_test_dashboard(request):
    """
    Dashboard for testing SMS functionality
    """
    # Get SMS configuration
    config = SMSConfig.get_config()
    
    # Get recent bookings for testing
    recent_bookings = Booking.objects.filter(status__in=['pending', 'confirmed', 'paid']).order_by('-created_at')[:10]
    
    context = {
        'config': config,
        'recent_bookings': recent_bookings,
        'title': 'SMS Test Dashboard',
    }
    
    return render(request, 'sms_notifications/test_dashboard.html', context)


@staff_member_required
@require_POST
def send_test_sms(request):
    """
    Send a test SMS message
    """
    phone_number = request.POST.get('phone_number')
    message = request.POST.get('message', 'This is a test message from Desert Safari')
    
    if not phone_number:
        messages.error(request, 'Phone number is required')
        return redirect('sms_test_dashboard')
    
    # Make sure phone number has + prefix
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    # Send the SMS
    result = send_sms(phone_number, message)
    
    if result:
        messages.success(request, f'Test SMS sent successfully to {phone_number}')
    else:
        messages.error(request, f'Failed to send test SMS to {phone_number}. Check your Twilio configuration.')
    
    return redirect('sms_test_dashboard')


@staff_member_required
@require_POST
def test_booking_sms(request):
    """
    Test sending booking confirmation and admin notification SMS for a specific booking
    """
    booking_id = request.POST.get('booking_id')
    sms_type = request.POST.get('sms_type', 'both')  # 'customer', 'admin', or 'both'
    
    if not booking_id:
        messages.error(request, 'Booking ID is required')
        return redirect('sms_test_dashboard')
    
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        messages.error(request, f'Booking with ID {booking_id} not found')
        return redirect('sms_test_dashboard')
    
    success = True
    
    # Send customer SMS if requested
    if sms_type in ['customer', 'both']:
        customer_result = send_booking_confirmation_sms(booking)
        if customer_result:
            messages.success(request, f'Booking confirmation SMS sent successfully to {booking.phone}')
        else:
            messages.error(request, f'Failed to send booking confirmation SMS to {booking.phone}')
            success = False
    
    # Send admin SMS if requested
    if sms_type in ['admin', 'both']:
        admin_result = send_booking_notification_sms_to_admin(booking)
        if admin_result:
            messages.success(request, 'Admin notification SMS sent successfully')
        else:
            messages.error(request, 'Failed to send admin notification SMS')
            success = False
    
    return redirect('sms_test_dashboard')


@staff_member_required
@require_POST
def update_sms_config(request):
    """
    Update SMS configuration
    """
    config = SMSConfig.get_config()
    
    # Update configuration fields
    config.enable_customer_sms = request.POST.get('enable_customer_sms') == 'on'
    config.enable_admin_sms = request.POST.get('enable_admin_sms') == 'on'
    config.admin_phone_number = request.POST.get('admin_phone_number', '')
    config.twilio_account_sid = request.POST.get('twilio_account_sid', '')
    config.twilio_auth_token = request.POST.get('twilio_auth_token', '')
    config.twilio_phone_number = request.POST.get('twilio_phone_number', '')
    
    # Save the configuration
    config.save()
    
    messages.success(request, 'SMS configuration updated successfully')
    return redirect('sms_test_dashboard')
