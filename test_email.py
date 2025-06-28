import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add Django project to path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Django settings
import django
django.setup()
from django.conf import settings

def test_smtp_connection():
    """Test SMTP connection and authentication"""
    print("Testing SMTP connection...")
    try:
        # Connect to SMTP server
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        # Login with credentials
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("✅ SMTP connection and authentication successful!")
        
        # Close connection
        server.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP connection failed: {str(e)}")
        return False

def send_test_email():
    """Send a test email"""
    if not test_smtp_connection():
        return False
    
    print("\nSending test email...")
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = settings.EMAIL_HOST_USER  # Send to yourself for testing
        msg['Subject'] = 'Desert Safari Dubai - Test Email'
        
        # Add body
        body = """
        This is a test email from Desert Safari Dubai website.
        
        If you're seeing this, the SMTP configuration is working correctly.
        
        Time: {}
        """.format(django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to server
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {settings.EMAIL_HOST_USER}!")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        return False

if __name__ == "__main__":
    print("Email settings from Django:")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print()
    
    send_test_email() 