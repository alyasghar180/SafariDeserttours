from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import logging

# Configure logging
logger = logging.getLogger(__name__)

# SMS utilities removed


def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email to the customer
    """
    subject = f'Booking Confirmation - {settings.COMPANY_NAME} - Ref: {booking.booking_id}'
    from_email = getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL)
    to_email = booking.email
    
    # Context for the email template
    context = {
        'booking': booking,
        'company_name': settings.COMPANY_NAME,
        'company_email': getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL),
        'company_phone': settings.COMPANY_PHONE
    }
    
    try:
        # Render HTML content
        html_content = render_to_string('emails/booking_confirmation.html', context)
        text_content = strip_tags(html_content)  # Plain text version of the email
        
        # Create the email
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email_sent = email.send()
        
        if email_sent:
            logger.info(f"✅ Booking confirmation email sent to {to_email} for booking {booking.booking_id}")
            if settings.DEBUG:
                print(f"\n{'='*80}")
                print(f"✅ BOOKING CONFIRMATION EMAIL SENT")
                print(f"To: {to_email}")
                print(f"Subject: {subject}")
                print(f"{'='*80}\n")
        else:
            logger.warning(f"❌ Failed to send booking confirmation email to {to_email} for booking {booking.booking_id}")
        
        return email_sent
    except Exception as e:
        logger.error(f"❌ Error sending booking confirmation email: {str(e)}")
        # If we're in development, print to console
        if settings.DEBUG:
            print(f"\n{'='*80}")
            print(f"❌ ERROR SENDING BOOKING CONFIRMATION EMAIL")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Error: {str(e)}")
            print(f"{'='*80}\n")
        return False


def send_booking_notification_to_admin(booking):
    """
    Send booking notification to admin via email
    """
    subject = f'New Booking Alert - {booking.booking_id}'
    from_email = getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL)
    to_email = 'thesafarideserttours@gmail.com'  # Admin email address
    
    # Context for the email template
    context = {
        'booking': booking,
        'company_name': settings.COMPANY_NAME
    }
    
    try:
        # Render HTML content
        html_content = render_to_string('emails/booking_notification_admin.html', context)
        text_content = strip_tags(html_content)  # Plain text version of the email
        
        # Create the email
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email_sent = email.send()
        
        if email_sent:
            logger.info(f"✅ Admin notification email sent to {to_email} for booking {booking.booking_id}")
            if settings.DEBUG:
                print(f"\n{'='*80}")
                print(f"✅ ADMIN NOTIFICATION EMAIL SENT")
                print(f"To: {to_email}")
                print(f"Subject: {subject}")
                print(f"{'='*80}\n")
        else:
            logger.warning(f"❌ Failed to send admin notification email for booking {booking.booking_id}")
        
        return email_sent
    except Exception as e:
        logger.error(f"❌ Error sending admin notification email: {str(e)}")
        # If we're in development, print to console
        if settings.DEBUG:
            print(f"\n{'='*80}")
            print(f"❌ ERROR SENDING ADMIN NOTIFICATION EMAIL")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Error: {str(e)}")
            print(f"{'='*80}\n")
        return False


def send_booking_cancellation_email(booking):
    """
    Send booking cancellation email to the customer
    """
    subject = f'Booking Cancellation - {settings.COMPANY_NAME} - Ref: {booking.booking_id}'
    from_email = getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL)
    to_email = booking.email
    
    # Context for the email template
    context = {
        'booking': booking,
        'company_name': settings.COMPANY_NAME,
        'company_email': getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL),
        'company_phone': settings.COMPANY_PHONE,
        'cancellation_date': timezone.now().strftime('%Y-%m-%d %H:%M')
    }
    
    try:
        # Render HTML content
        html_content = render_to_string('emails/booking_cancellation.html', context)
        text_content = strip_tags(html_content)  # Plain text version of the email
        
        # Create the email
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email_sent = email.send()
        
        if email_sent:
            logger.info(f"Booking cancellation email sent to {to_email} for booking {booking.booking_id}")
        else:
            logger.warning(f"Failed to send booking cancellation email to {to_email} for booking {booking.booking_id}")
        
        return email_sent
    except Exception as e:
        logger.error(f"Error sending booking cancellation email: {str(e)}")
        # If we're in development, print to console
        if settings.DEBUG:
            print(f"Would have sent email to {to_email} with subject: {subject}")
            print(f"From: {from_email}")
            print(f"Error: {str(e)}")
        return False


def send_booking_update_email(booking):
    """
    Send booking update email to the customer
    """
    subject = f'Booking Update - {settings.COMPANY_NAME} - Ref: {booking.booking_id}'
    from_email = getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL)
    to_email = booking.email
    
    # Context for the email template
    context = {
        'booking': booking,
        'company_name': settings.COMPANY_NAME,
        'company_email': getattr(settings, 'EMAIL_HOST_USER', settings.COMPANY_EMAIL),
        'company_phone': settings.COMPANY_PHONE,
        'update_date': timezone.now().strftime('%Y-%m-%d %H:%M')
    }
    
    try:
        # Render HTML content
        html_content = render_to_string('emails/booking_update.html', context)
        text_content = strip_tags(html_content)  # Plain text version of the email
        
        # Create the email
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email_sent = email.send()
        
        if email_sent:
            logger.info(f"Booking update email sent to {to_email} for booking {booking.booking_id}")
        else:
            logger.warning(f"Failed to send booking update email to {to_email} for booking {booking.booking_id}")
        
        return email_sent
    except Exception as e:
        logger.error(f"Error sending booking update email: {str(e)}")
        # If we're in development, print to console
        if settings.DEBUG:
            print(f"Would have sent email to {to_email} with subject: {subject}")
            print(f"From: {from_email}")
            print(f"Error: {str(e)}")
        return False
