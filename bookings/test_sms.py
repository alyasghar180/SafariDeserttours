from django.core.management.base import BaseCommand
from django.conf import settings
from .models import SMSConfig
from .sms_utils import send_sms, send_booking_confirmation_sms, send_booking_notification_sms_to_admin
from .models import Booking

def test_sms_configuration():
    """
    Test the SMS configuration
    """
    # Get or create SMS config
    config = SMSConfig.get_config()
    
    print("SMS Configuration:")
    print(f"- Customer SMS enabled: {config.enable_customer_sms}")
    print(f"- Admin SMS enabled: {config.enable_admin_sms}")
    print(f"- Twilio Account SID: {'Configured' if config.twilio_account_sid else 'Not configured'}")
    print(f"- Twilio Auth Token: {'Configured' if config.twilio_auth_token else 'Not configured'}")
    print(f"- Twilio Phone Number: {config.twilio_phone_number or 'Not configured'}")
    print(f"- Admin Phone Number: {config.admin_phone_number or 'Not configured'}")
    
    # Check if SMS is properly configured
    if not all([config.twilio_account_sid, config.twilio_auth_token, config.twilio_phone_number]):
        print("\nWARNING: Twilio is not fully configured. Please set up your Twilio credentials in the admin panel.")
        print("Go to Admin > Bookings > SMS Configuration to configure your Twilio settings.")
        
        # Check fallback to settings
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        phone_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        if all([account_sid, auth_token, phone_number]):
            print("\nFallback to settings.py is available with the following configuration:")
            print(f"- TWILIO_ACCOUNT_SID: {'Configured' if account_sid else 'Not configured'}")
            print(f"- TWILIO_AUTH_TOKEN: {'Configured' if auth_token else 'Not configured'}")
            print(f"- TWILIO_PHONE_NUMBER: {phone_number or 'Not configured'}")
        else:
            print("\nNo fallback configuration found in settings.py.")
            print("SMS notifications will not work until you configure Twilio.")
    
    return config

def test_send_sms(phone_number, message="This is a test message from Desert Safari"):
    """
    Test sending an SMS to a specific phone number
    
    Args:
        phone_number (str): The phone number to send the test SMS to
        message (str): The message to send
    """
    # Make sure phone number has + prefix
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    print(f"\nSending test SMS to {phone_number}...")
    result = send_sms(phone_number, message)
    
    if result:
        print("✅ Test SMS sent successfully!")
    else:
        print("❌ Failed to send test SMS. Check your Twilio configuration and logs.")
    
    return result

def test_booking_sms(booking_id):
    """
    Test sending booking confirmation and admin notification SMS for a specific booking
    
    Args:
        booking_id (str): The booking ID to test with
    """
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        print(f"\n❌ Booking with ID {booking_id} not found.")
        return False
    
    print(f"\nTesting booking confirmation SMS for booking {booking_id}...")
    customer_result = send_booking_confirmation_sms(booking)
    
    if customer_result:
        print(f"✅ Booking confirmation SMS sent successfully to {booking.phone}!")
    else:
        print(f"❌ Failed to send booking confirmation SMS to {booking.phone}.")
    
    print(f"\nTesting admin notification SMS for booking {booking_id}...")
    admin_result = send_booking_notification_sms_to_admin(booking)
    
    if admin_result:
        print("✅ Admin notification SMS sent successfully!")
    else:
        print("❌ Failed to send admin notification SMS.")
    
    return customer_result and admin_result

# For command line usage
class Command(BaseCommand):
    help = 'Test SMS functionality'
    
    def add_arguments(self, parser):
        parser.add_argument('--test-config', action='store_true', help='Test SMS configuration')
        parser.add_argument('--send-test', nargs='?', const='', help='Send a test SMS to a phone number')
        parser.add_argument('--test-booking', nargs='?', const='', help='Test booking SMS for a booking ID')
        parser.add_argument('--message', nargs='?', help='Custom message for test SMS')
    
    def handle(self, *args, **options):
        if options['test_config']:
            test_sms_configuration()
        
        if options['send_test']:
            phone = options['send_test']
            message = options['message'] or "This is a test message from Desert Safari"
            test_send_sms(phone, message)
        
        if options['test_booking']:
            booking_id = options['test_booking']
            test_booking_sms(booking_id)
