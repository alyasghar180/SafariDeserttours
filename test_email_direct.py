import os
import django
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

def test_django_email():
    """
    Test sending an email using Django's email system
    """
    print("\n=== Testing Django Email System ===")
    subject = 'Test Email from Desert Safari Dubai'
    message = 'This is a test email to verify that SMTP is working correctly.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['adullahshafiq146@gmail.com']
    
    print(f"Email settings:")
    print(f"  Backend: {settings.EMAIL_BACKEND}")
    print(f"  Host: {settings.EMAIL_HOST}")
    print(f"  Port: {settings.EMAIL_PORT}")
    print(f"  TLS: {settings.EMAIL_USE_TLS}")
    print(f"  User: {settings.EMAIL_HOST_USER}")
    print(f"  Password: {'*' * 8}")
    print(f"  Default From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"\nSending test email from {from_email} to {recipient_list}")
    
    try:
        # Create HTML content
        html_content = f"""
        <html>
        <body>
            <h2>SMTP Test Email</h2>
            <p>This is a test email to verify that SMTP is working correctly.</p>
            <p>If you're seeing this, the SMTP configuration is working!</p>
        </body>
        </html>
        """
        
        # Create the email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        result = email.send(fail_silently=False)
        
        if result:
            print("✅ Django email sent successfully!")
        else:
            print("❌ Django email failed to send.")
    except Exception as e:
        print(f"❌ Error sending Django email: {str(e)}")
        print(traceback.format_exc())

def test_direct_smtp():
    """
    Test SMTP connection directly without using Django
    """
    print("\n=== Testing Direct SMTP Connection ===")
    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_user = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD
    use_tls = settings.EMAIL_USE_TLS
    
    print(f"Connecting to {smtp_host}:{smtp_port}")
    print(f"Username: {smtp_user}")
    print(f"Password: {'*' * 8}")
    print(f"TLS: {use_tls}")
    
    try:
        # Create SMTP connection
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.set_debuglevel(1)  # Enable debug output
        
        # Start TLS if required
        if use_tls:
            print("Starting TLS...")
            server.starttls()
        
        # Login
        print("Attempting login...")
        server.login(smtp_user, smtp_password)
        print("✅ SMTP login successful!")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Direct SMTP Test'
        msg['From'] = smtp_user
        msg['To'] = 'adullahshafiq146@gmail.com'
        
        # Add plain text and HTML parts
        text_part = MIMEText('This is a direct SMTP test email.', 'plain')
        html_part = MIMEText('<html><body><h2>Direct SMTP Test</h2><p>This is a direct SMTP test email.</p></body></html>', 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send message
        print("Sending direct SMTP message...")
        server.send_message(msg)
        print("✅ Direct SMTP message sent successfully!")
        
        # Close connection
        server.quit()
        print("SMTP connection closed")
        return True
    except Exception as e:
        print(f"❌ Error in direct SMTP test: {str(e)}")
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    print("Starting email tests...")
    
    # First try direct SMTP
    smtp_success = test_direct_smtp()
    
    # Then try Django's email system
    test_django_email()
    
    if not smtp_success:
        print("\n=== SMTP Troubleshooting Tips ===")
        print("1. Verify the app password is correct and has no spaces")
        print("2. Ensure 2-Factor Authentication is enabled on your Gmail account")
        print("3. Check if your Gmail account has any security restrictions")
        print("4. Try generating a new app password")
        print("5. Check if your network blocks outgoing SMTP connections") 