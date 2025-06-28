from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SMSConfig

@admin.register(SMSConfig)
class SMSConfigAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'enable_customer_sms', 'enable_admin_sms')
    
    fieldsets = (
        (_('SMS Notification Settings'), {
            'fields': ('enable_customer_sms', 'enable_admin_sms', 'admin_phone_number')
        }),
        (_('Twilio Configuration'), {
            'fields': ('twilio_account_sid', 'twilio_auth_token', 'twilio_phone_number'),
            'classes': ('collapse',),
            'description': _('Enter your Twilio credentials to enable SMS notifications.')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return SMSConfig.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the configuration
        return False
