from django.db import models
from django.utils.translation import gettext_lazy as _

class SMSConfig(models.Model):
    """
    Configuration model for SMS settings
    """
    enable_customer_sms = models.BooleanField(
        _('Enable customer SMS notifications'), 
        default=True,
        help_text=_('Send SMS notifications to customers for booking confirmations')
    )
    enable_admin_sms = models.BooleanField(
        _('Enable admin SMS notifications'), 
        default=True,
        help_text=_('Send SMS notifications to admin for new bookings')
    )
    twilio_account_sid = models.CharField(
        _('Twilio Account SID'), 
        max_length=255, 
        blank=True,
        help_text=_('Your Twilio Account SID')
    )
    twilio_auth_token = models.CharField(
        _('Twilio Auth Token'), 
        max_length=255, 
        blank=True,
        help_text=_('Your Twilio Auth Token')
    )
    twilio_phone_number = models.CharField(
        _('Twilio Phone Number'), 
        max_length=20, 
        blank=True,
        help_text=_('Your Twilio phone number in E.164 format (e.g., +15005550006)')
    )
    admin_phone_number = models.CharField(
        _('Admin Phone Number'), 
        max_length=20, 
        blank=True,
        help_text=_('Admin phone number to receive booking notifications in E.164 format (e.g., +971582240451)')
    )
    
    class Meta:
        verbose_name = _('SMS Configuration')
        verbose_name_plural = _('SMS Configuration')
    
    def __str__(self):
        return _('SMS Configuration')
    
    @classmethod
    def get_config(cls):
        """
        Get the SMS configuration. Creates a default one if none exists.
        """
        config, created = cls.objects.get_or_create(pk=1)
        return config
