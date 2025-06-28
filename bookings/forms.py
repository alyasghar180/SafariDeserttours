from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

from .models import Booking, BookingAddon
from packages.models import Package, PackageAddon
from locations.models import Emirate, PickupLocation


class BookingForm(forms.ModelForm):
    """
    Form for creating a new booking.
    """
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text=_('Select the date you want to book the safari for.')
    )
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_location = cleaned_data.get('pickup_location')
        pickup_location_text = cleaned_data.get('pickup_location_text')
        emirate = cleaned_data.get('emirate')
        
        # If neither pickup_location nor pickup_location_text is provided
        if not pickup_location and not pickup_location_text:
            # Instead of raising an error, we'll allow the form to be submitted
            # The view will handle creating a default pickup location
            pass
        
        # If emirate is selected but no pickup location is selected
        if emirate and not pickup_location and not pickup_location_text:
            # Instead of raising an error, we'll allow the form to be submitted
            # The view will handle creating a default pickup location
            pass
            
        return cleaned_data
    
    class Meta:
        model = Booking
        fields = [
            'package', 'booking_date', 'full_name', 'email', 'phone',
            'nationality', 'adults', 'children', 'emirate', 'pickup_location',
            'pickup_location_text', 'hotel_name', 'hotel_room', 'address_details',
            'special_requests', 'payment_method'
        ]
        widgets = {
            'package': forms.HiddenInput(),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your full name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Your email address')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('+971 58 224 0451')}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your nationality')}),
            'adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'emirate': forms.Select(attrs={'class': 'form-select', 'id': 'emirate-select'}),
            'pickup_location': forms.Select(attrs={'class': 'form-select', 'id': 'pickup-location-select'}),
            'pickup_location_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your pickup location if not listed above')}),
            'hotel_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Hotel name (if applicable)')}),
            'hotel_room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Room number (if applicable)')}),
            'address_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': _('Additional address details for pickup')}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Any special requests or dietary requirements')}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        
        if self.package:
            self.fields['package'].initial = self.package.id
            
        # Set up emirate and pickup location fields
        try:
            # Try to access the Emirate and PickupLocation models
            # This will fail if the tables don't exist yet
            self.fields['emirate'].queryset = Emirate.objects.filter(is_active=True).order_by('display_order', 'name')
            self.fields['emirate'].empty_label = _('Select Emirate')
            
            # Initially, set pickup location queryset to empty
            self.fields['pickup_location'].queryset = PickupLocation.objects.none()
            self.fields['pickup_location'].empty_label = _('Select Pickup Location')
            
            # If an emirate is already selected (e.g., in case of form errors or edit)
            if 'emirate' in self.data and self.data['emirate']:
                try:
                    emirate_id = int(self.data['emirate'])
                    self.fields['pickup_location'].queryset = PickupLocation.objects.filter(
                        emirate_id=emirate_id, is_active=True
                    ).order_by('display_order', 'name')
                except (ValueError, TypeError):
                    pass
            # If we're editing an existing booking with an emirate already set
            elif self.instance and self.instance.pk and self.instance.emirate:
                self.fields['pickup_location'].queryset = PickupLocation.objects.filter(
                    emirate=self.instance.emirate, is_active=True
                ).order_by('display_order', 'name')
        except:
            # If the tables don't exist yet, just use an empty queryset
            # This allows the form to render without errors
            from django.db.models.query import EmptyQuerySet
            self.fields['emirate'].queryset = EmptyQuerySet()
            self.fields['pickup_location'].queryset = EmptyQuerySet()
            self.fields['emirate'].empty_label = _('Select Emirate')
            self.fields['pickup_location'].empty_label = _('Select Pickup Location')
            
        # If this is an existing booking being updated
        if self.instance and self.instance.pk:
            # For existing bookings, allow the current date if it's already set
            if self.instance.booking_date:
                min_date = min(self.instance.booking_date, timezone.now().date() + timedelta(days=1))
                self.fields['booking_date'].widget.attrs['min'] = min_date.strftime('%Y-%m-%d')
        else:
            # For new bookings, set minimum date to tomorrow
            tomorrow = timezone.now().date() + timedelta(days=1)
            self.fields['booking_date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')
        
        # Set maximum date to 6 months from now
        max_date = timezone.now().date() + timedelta(days=180)
        self.fields['booking_date'].widget.attrs['max'] = max_date.strftime('%Y-%m-%d')
    
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        today = timezone.now().date()
        
        if booking_date <= today:
            raise forms.ValidationError(_('Booking date must be at least one day in advance.'))
            
        # You could add more validation here, like checking if the date is available
        # or if it's a valid operating day for the selected package
        
        return booking_date
    
    def clean(self):
        cleaned_data = super().clean()
        adults = cleaned_data.get('adults', 0)
        children = cleaned_data.get('children', 0)
        
        if adults + children <= 0:
            raise forms.ValidationError(_('You must book for at least one person.'))
            
        return cleaned_data


class BookingAddonForm(forms.Form):
    """
    Form for selecting addons during booking.
    """
    addon = forms.ModelChoiceField(
        queryset=PackageAddon.objects.filter(is_active=True),
        widget=forms.HiddenInput()
    )
    quantity = forms.IntegerField(
        min_value=0,
        max_value=20,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control addon-quantity', 'min': 0, 'max': 20})
    )
    
    def __init__(self, *args, **kwargs):
        self.addon = kwargs.pop('addon', None)
        super().__init__(*args, **kwargs)
        
        if self.addon:
            self.fields['addon'].initial = self.addon.id
