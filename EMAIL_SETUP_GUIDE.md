# Email Setup Guide for Desert Safari Dubai Website

This guide provides detailed instructions for setting up email functionality for the Desert Safari Dubai website.

## Current Configuration

The website is currently configured to use the Django console email backend for development purposes. Emails will be printed to the console rather than actually sent.

## Email Functionality

The website sends emails in the following scenarios:

1. **Booking Confirmation Email** - Sent to the customer when they make a booking
2. **Admin Notification Email** - Sent to the admin (adullahshafiq146@gmail.com) when a new booking is made
3. **Booking Cancellation Email** - Sent to the customer when a booking is cancelled
4. **Booking Update Email** - Sent to the customer when a booking is updated

## Setting Up Email for Production

### Option 1: Gmail with App Password (Recommended for Small Volume)

Gmail SMTP can be tricky to set up due to Google's security measures. Follow these steps carefully:

1. **Enable 2-Factor Authentication (2FA)**
   - Go to your Google Account > Security > 2-Step Verification
   - Follow the prompts to enable 2FA
   - This is a required step for app passwords to work

2. **Generate a New App Password**
   - Go to your Google Account > Security > App Passwords
   - Select "Mail" as the app and "Other" as the device
   - Enter a name (e.g., "Desert Safari Website")
   - Click "Generate"
   - Google will display a 16-character app password
   - **IMPORTANT**: Copy this password immediately and keep it secure

3. **Update settings.py**
   - Open `desert_safari/settings.py`
   - Update the email settings:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'adullahshafiq146@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-new-app-password'  # Replace with the newly generated app password (no spaces)
   DEFAULT_FROM_EMAIL = 'adullahshafiq146@gmail.com'
   ```

4. **Troubleshooting Gmail SMTP Issues**
   - If you encounter authentication errors:
     - Make sure the app password is entered correctly with NO SPACES
     - Verify 2FA is enabled on your Gmail account
     - Try generating a completely new app password
     - Check if your Gmail account has security restrictions (like "Less secure app access")
     - Make sure your account doesn't have any temporary restrictions
   
   - If you still have issues, try these steps:
     - Go to https://accounts.google.com/DisplayUnlockCaptcha and complete the captcha
     - Check your Gmail account for any security alerts and approve the login attempt
     - Try using a different Gmail account
     - Check if your hosting provider blocks outgoing SMTP connections on port 587

### Option 2: SendGrid (Recommended for Production)

SendGrid is a reliable email service that offers a free tier with 100 emails per day.

1. **Sign up for SendGrid**
   - Create an account at [SendGrid](https://sendgrid.com/)
   - Verify your domain or use domain authentication

2. **Create an API Key**
   - In your SendGrid dashboard, go to Settings > API Keys
   - Create a new API key with "Mail Send" permissions
   - Copy the API key immediately (you won't be able to see it again)

3. **Install SendGrid Python Library**
   ```bash
   pip install sendgrid
   pip install django-sendgrid-v5
   ```

4. **Update requirements.txt**
   ```
   django-sendgrid-v5==1.2.0
   ```

5. **Update settings.py**
   ```python
   EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
   SENDGRID_API_KEY = 'your-sendgrid-api-key'
   SENDGRID_SANDBOX_MODE_IN_DEBUG = False
   DEFAULT_FROM_EMAIL = 'adullahshafiq146@gmail.com'
   ```

### Option 3: Amazon SES (Good for High Volume)

Amazon SES is a cost-effective solution for sending high volumes of email.

1. **Set up Amazon SES**
   - Create an AWS account if you don't have one
   - Verify your domain or email address in the SES console
   - Request production access if needed (to move out of the sandbox)

2. **Create IAM User with SES Permissions**
   - Create a new IAM user with programmatic access
   - Attach the "AmazonSESFullAccess" policy
   - Save the access key and secret key

3. **Install Django SES**
   ```bash
   pip install django-ses
   ```

4. **Update requirements.txt**
   ```
   django-ses==3.5.0
   ```

5. **Update settings.py**
   ```python
   EMAIL_BACKEND = 'django_ses.SESBackend'
   AWS_SES_ACCESS_KEY_ID = 'your-access-key'
   AWS_SES_SECRET_ACCESS_KEY = 'your-secret-key'
   AWS_SES_REGION_NAME = 'us-east-1'  # Change to your region
   DEFAULT_FROM_EMAIL = 'adullahshafiq146@gmail.com'
   ```

## Testing Email Functionality

To test if your email configuration is working:

1. **Run the test script**
   ```bash
   python test_email_direct.py
   ```

2. **Check the console output** (if using console backend) or your email inbox (if using SMTP)

3. **Create a test booking** on the website and verify that both the customer confirmation and admin notification emails are sent

## Immediate Solution for Development

For development purposes, the website is currently configured to use the Django console email backend. This means emails will be printed to the console rather than actually sent, which is a reliable way to test email functionality without actually sending emails.

To see emails in the console:

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Make a test booking on the website

3. Check the console output to see the emails that would be sent

## Email Templates

The email templates are located in the `templates/emails/` directory:

- `booking_confirmation.html` - Template for booking confirmation emails
- `booking_notification_admin.html` - Template for admin notification emails
- `booking_cancellation.html` - Template for booking cancellation emails
- `booking_update.html` - Template for booking update emails

You can customize these templates to match your branding and communication style.

## Security Best Practices

1. **Never commit sensitive information** like email passwords or API keys to version control
2. **Use environment variables** for sensitive information in production:
   ```python
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
   ```
3. **Regularly rotate credentials** (app passwords, API keys) for security
4. **Monitor your email sending limits** to avoid exceeding quotas or being flagged as spam
5. **Implement email queue** for high-volume scenarios to prevent sending delays 