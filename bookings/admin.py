from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Booking, BookingAddon


class BookingAddonInline(admin.TabularInline):
    model = BookingAddon
    extra = 0
    fields = ('addon', 'quantity', 'price')
    readonly_fields = ('addon', 'price')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'full_name', 'package', 'booking_date', 'adults', 'children', 'total_price', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'booking_date', 'created_at', 'package__category')
    search_fields = ('booking_id', 'full_name', 'email', 'phone', 'package__name')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    inlines = [BookingAddonInline]
    date_hierarchy = 'booking_date'
    
    fieldsets = (
        (_('Booking Information'), {
            'fields': ('booking_id', 'status', 'package', 'booking_date')
        }),
        (_('Customer Information'), {
            'fields': ('user', 'full_name', 'email', 'phone', 'nationality')
        }),
        (_('Group Size'), {
            'fields': ('adults', 'children')
        }),
        (_('Pickup Information'), {
            'fields': ('emirate', 'pickup_location', 'pickup_location_text', 'pickup_time', 'hotel_name', 'hotel_room', 'address_details')
        }),
        (_('Special Requests'), {
            'fields': ('special_requests',)
        }),
        (_('Payment Information'), {
            'fields': ('payment_method', 'total_price', 'payment_id', 'is_paid')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('package', 'user')


@admin.register(BookingAddon)
class BookingAddonAdmin(admin.ModelAdmin):
    list_display = ('booking', 'addon', 'quantity', 'price')
    list_filter = ('addon', 'booking__status')
    search_fields = ('booking__booking_id', 'booking__full_name', 'addon__name')
    readonly_fields = ('booking', 'addon', 'price')
    
    def has_add_permission(self, request):
        return False
