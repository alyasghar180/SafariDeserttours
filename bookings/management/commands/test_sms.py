from django.core.management.base import BaseCommand
from bookings.test_sms import test_sms_configuration, test_send_sms, test_booking_sms

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
            if phone:
                test_send_sms(phone, message)
            else:
                self.stdout.write(self.style.ERROR("Please provide a phone number with --send-test"))
        
        if options['test_booking']:
            booking_id = options['test_booking']
            if booking_id:
                test_booking_sms(booking_id)
            else:
                self.stdout.write(self.style.ERROR("Please provide a booking ID with --test-booking"))
        
        # If no options provided, show help
        if not any([options['test_config'], options['send_test'], options['test_booking']]):
            self.print_help('manage.py', 'test_sms')
