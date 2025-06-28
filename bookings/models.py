from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
import uuid

from packages.models import Package, PackageAddon
from locations.models import PickupLocation, Emirate

class Booking(models.Model):
    """
    Model for storing booking information.
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('paid', _('Paid')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', _('Credit Card')),
        ('paypal', _('PayPal')),
        ('bank_transfer', _('Bank Transfer')),
        ('cash', _('Cash on Pickup')),
    )
    
    # Booking reference and status
    booking_id = models.CharField(_('booking ID'), max_length=50, unique=True, editable=False)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Package and date information
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='bookings', verbose_name=_('package'))
    booking_date = models.DateField(_('booking date'))
    
    # Customer information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings', verbose_name=_('user'))
    full_name = models.CharField(_('full name'), max_length=100)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone number'), max_length=20)
    nationality = models.CharField(_('nationality'), max_length=50, blank=True)
    
    # Group size
    adults = models.PositiveSmallIntegerField(_('number of adults'), default=1)
    children = models.PositiveSmallIntegerField(_('number of children'), default=0)
    
    # Pickup information
    pickup_location_text = models.CharField(_('pickup location text'), max_length=255, blank=True, 
                                        help_text=_('Manual entry of pickup location if not selecting from predefined locations'))
    # CRITICAL: Ensure pickup_location can be null in both the model and database
    pickup_location = models.ForeignKey(PickupLocation, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='bookings', verbose_name=_('pickup location'))
    emirate = models.ForeignKey(Emirate, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='bookings', verbose_name=_('emirate'))
    pickup_time = models.TimeField(_('pickup time'), null=True, blank=True)
    hotel_name = models.CharField(_('hotel name'), max_length=100, blank=True)
    hotel_room = models.CharField(_('hotel room'), max_length=20, blank=True)
    address_details = models.TextField(_('address details'), blank=True, 
                                    help_text=_('Additional address details for pickup'))
    
    # Special requests
    special_requests = models.TextField(_('special requests'), blank=True)
    
    # Payment information
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit_card')
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)
    payment_id = models.CharField(_('payment ID'), max_length=100, blank=True)
    is_paid = models.BooleanField(_('is paid'), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    cancelled_at = models.DateTimeField(_('cancelled at'), null=True, blank=True)
    cancellation_reason = models.TextField(_('cancellation reason'), blank=True)
    
    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        # Generate booking ID if not set
        if not self.booking_id:
            # Format: DSF-{YYMMDD}-{UUID4 first 6 chars}
            today = timezone.now().strftime('%y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.booking_id = f"DSF-{today}-{unique_id}"
            
        # Ensure pickup_location is set if pickup_location_text is provided
        if not self.pickup_location and self.pickup_location_text:
            # Import here to avoid circular imports
            from locations.models import PickupLocation, Emirate
            
            # Get or create a default emirate for custom locations
            default_emirate, _ = Emirate.objects.get_or_create(
                name="Custom",
                defaults={"is_active": True, "display_order": 999}
            )
            
            # Get or create a default pickup location
            default_pickup, _ = PickupLocation.objects.get_or_create(
                name="Custom Location",
                emirate=default_emirate,
                defaults={
                    "is_active": True,
                    "display_order": 999,
                    "additional_cost": 0
                }
            )
            
            self.pickup_location = default_pickup
            
        super().save(*args, **kwargs)
    
    def calculate_total_price(self):
        """
        Calculate the total price of the booking including addons.
        """
        # Base price calculation
        base_price = self.package.price * self.adults
        if self.package.child_price and self.children > 0:
            base_price += self.package.child_price * self.children
        else:
            # If no specific child price, use adult price with 30% discount
            base_price += (self.package.price * 0.7) * self.children
        
        # Add pickup location cost if applicable
        if self.pickup_location and self.pickup_location.additional_cost:
            # Apply pickup cost per person
            pickup_cost = self.pickup_location.additional_cost * (self.adults + self.children)
            base_price += pickup_cost
        
        # Add addon prices
        addon_price = sum(
            addon.get_total_price() for addon in self.addons.all()
        )
        
        return base_price + addon_price
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('booking_detail', args=[self.booking_id])


class BookingAddon(models.Model):
    """
    Model for storing addons selected for a booking.
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='addons', verbose_name=_('booking'))
    addon = models.ForeignKey(PackageAddon, on_delete=models.PROTECT, verbose_name=_('addon'))
    quantity = models.PositiveSmallIntegerField(_('quantity'), default=1)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, help_text=_('Price at the time of booking'))
    
    class Meta:
        verbose_name = _('booking addon')
        verbose_name_plural = _('booking addons')
        unique_together = ('booking', 'addon')
    
    def __str__(self):
        return f"{self.booking.booking_id} - {self.addon.name} x{self.quantity}"
    
    def get_total_price(self):
        """
        Calculate the total price for this addon.
        """
        if self.addon.is_per_person:
            # If addon is per person, multiply by number of people
            return self.price * self.quantity * (self.booking.adults + self.booking.children)
        else:
            # Otherwise, just multiply by quantity
            return self.price * self.quantity
