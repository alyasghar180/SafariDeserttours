"""
Dummy SMS utility functions that don't require Twilio.
These functions log messages instead of sending actual SMS.
"""

def send_sms(to_number, message):
    """
    Dummy function that logs the message instead of sending an SMS
    
    Args:
        to_number (str): The recipient's phone number
        message (str): The message content
        
    Returns:
        bool: Always returns True
    """
    print(f"[DUMMY SMS] To: {to_number}, Message: {message}")
    return True

def send_booking_confirmation_sms(booking):
    """
    Dummy function for booking confirmation SMS
    
    Args:
        booking: The Booking object
        
    Returns:
        bool: Always returns True
    """
    print(f"[DUMMY SMS] Booking confirmation for {booking.booking_id} would be sent to {booking.phone}")
    return True

def send_booking_notification_sms_to_admin(booking):
    """
    Dummy function for admin notification SMS
    
    Args:
        booking: The Booking object
        
    Returns:
        bool: Always returns True
    """
    print(f"[DUMMY SMS] Admin notification for booking {booking.booking_id} would be sent")
    return True
